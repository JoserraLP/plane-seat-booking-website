from flask import Blueprint, render_template, request, redirect, url_for, flash

from datetime import date

from website import redis, redlock, redlock_dbs
from website.static.constants import RESOURCE_TTL

# Planes blueprint
planes = Blueprint('planes', __name__)

locks = []


# -------------- Planes -------------- #
@planes.route('/show_planes')
def show_planes():
    try:
        # Clean locks list
        locks = []

        # Get all the planes and the locks from the DBs
        planes_data = get_all_planes()
        locks_data = get_all_locks()

        # Iterate in order to define the seats that are locked
        for k, v in locks_data.items():
            lock_plane = 'planes:' + k[0]
            lock_seat = k[2:].replace('seat_', '')
            planes_data[lock_plane]['seats'][lock_seat] = 'locked'

        return render_template('planes.html', planes=planes_data)

    except Exception as e:
        print(e)
        # Exception -> show message
        flash('Error, the planes could not be loaded')
        return render_template('planes.html')


# -------------- Planes -------------- #
@planes.route('/book_details', methods=['POST'])
def book_details():
    try:

        # Get all planes from the DB
        json_data = get_all_planes()

        # Get selected seats by user
        selected_results = parse_results(request.form.getlist("seats"))

        # Get selected plane by user
        selected_plane = json_data[selected_results['plane_name']]

        # Get selected elements by intersect
        selected_seats = ['seat_' + item for item in selected_plane['seats'].keys() if
                          item in selected_results['plane_seats']]

        # Create dict for purchase summary
        details = dict()
        details['seats'] = [item.split('_')[-1] for item in selected_seats]
        details['name'] = selected_plane['name']
        details['day'] = selected_plane['days']
        details['hour'] = selected_plane['hour']
        details['price'] = float(selected_plane['price']) * len(selected_seats)

        # Lock all the seats that are reserved
        for seat in selected_seats:
            resource_seat = selected_plane['name'][-1] + ':' + seat
            lock = redlock.lock(resource_seat, RESOURCE_TTL)
            locks.append(lock)

        return render_template('details.html', details=details)

    except Exception as e:
        print(e)
        # Exception -> show message
        flash('Error, the planes could not be loaded')
        return render_template('planes.html')


@planes.route('/book_seats', methods=['POST'])
def book_seats():
    try:

        # Get today day
        today = date.today()

        # Get user name
        details = request.form.getlist("details")

        # Update data on DB and unlock the locks of the reserved seats
        for lock in locks:
            if lock:
                resource = lock.resource
                print(resource)
                redis.update(name="planes:" + resource[0], key=resource[2:],
                             value='Purchased by ' + details[0] + " on " + today.strftime("%d/%m/%Y"))
                redlock.unlock(lock)

        # Clean up locks list
        locks.clear()

        flash('Congratulations! You ordered your seats', 'bg-light-green')  # Message
        return redirect(url_for('main.index'))

    except Exception as e:
        print(e)
        # Exception -> show message
        flash('Error, the planes could not be loaded')
        return render_template('planes.html')


def get_all_planes():
    # Get all keys from DB
    keys = redis.get_all_keys()

    json_data = {}

    # Store data into a dict
    for key in keys:
        json_data[key] = redis.get(key)

    # Iterate over the planes in order to create the seats dict and check they are full or not
    for plane_id, plane_values in json_data.items():
        num_seats = plane_values['num_seats']
        total_seats_reserved = [v for k, v in plane_values.items() if 'seat_' in k and v != '' and v != 'locked']
        json_data[plane_id]['full'] = len(total_seats_reserved) == int(num_seats)

        seats = dict()
        for k, v in plane_values.items():
            if 'seat_' in k:
                seats[k.replace('seat_', '')] = v
        json_data[plane_id]['seats'] = seats
    return json_data


def get_all_locks():
    all_locks = []

    # Retrieve all the data from the Redlock Databases
    for redlock_db in redlock_dbs:
        all_locks.append(redlock_db.get_all_keys())

    # Check if all the locks retrieved from the DB are the same
    all_keys_equals = all([locks[i] == all_locks[0][i] for i in range(len(locks))] for locks in all_locks)

    json_data = {}

    # Store the locks from the database
    if all_keys_equals:
        for key in all_locks[0]:
            json_data[key] = redis.get(key)

    return json_data


def parse_results(results):
    parsed_result = dict()

    # Parse name of the plane and the seats of the plane
    if results is not None:
        parsed_result['plane_name'] = results[0].split('_')[0]
        parsed_result['plane_seats'] = [item.replace(parsed_result['plane_name'] + '_', '') for item in results]
    return parsed_result
