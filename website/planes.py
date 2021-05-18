from flask import Blueprint, render_template, flash, request, redirect, url_for, flash
import json

from datetime import date

from website import redis, redlock, redis_lock
from website.static.constants import RESOURCE_TTL

# Planes blueprint
planes = Blueprint('planes', __name__)

locks = []

# -------------- Planes -------------- #
@planes.route('/show_planes')
def show_planes():
    """
    Retrieve basic statistics as number of devices in some time intervals

    Returns:
        Redirect to the statistics page
    """
    try:

        locks = []

        planes_data = get_all_planes()
        locks_data = get_all_locks()

        for k, v in locks_data.items():
            lock_plane = 'planes:'+k[0]
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

        json_data = get_all_planes()

        # Get selected allowed places type by user
        selected_results = parse_results(request.form.getlist("seats"))

        selected_plane = json_data[selected_results['plane_name']]

        # Get selected elements by intersect
        selected_seats = ['seat_'+item for item in selected_plane['seats'].keys() if item in selected_results['plane_seats']]

        details = dict()
        details['seats'] = selected_seats
        details['name'] = selected_plane['name']
        details['day'] = selected_plane['days']
        details['hour'] = selected_plane['hour']
        details['price'] = float(selected_plane['price'])*len(selected_seats)

        for seat in selected_seats:
            resource_seat = selected_plane['name'][-1]+':'+seat
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

        today = date.today()

        # Get user name
        details = request.form.getlist("details")

        for lock in locks:
            if lock:
                resource = lock.resource
                print(resource)
                redis.update(name="planes:"+resource[0], key=resource[2:], value='Purchased by ' + details[0] + " on " + today.strftime("%d/%m/%Y"))
                redlock.unlock(lock)

        flash('Congratulations! You ordered your seats', 'bg-green')  # Message
        return redirect(url_for('main.index'))

    except Exception as e:
        print(e)
        # Exception -> show message
        flash('Error, the planes could not be loaded')
        return render_template('planes.html')

def get_all_planes():
    keys = redis.get_all_keys()

    json_data = {}

    for key in keys:
        json_data[key] = redis.get(key)

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
    keys = redis_lock.get_all_keys()

    json_data = {}

    for key in keys:
        json_data[key] = redis.get(key)

    return json_data

def parse_results(results):
    parsed_result = dict()
    if results is not None:
        parsed_result['plane_name'] = results[0].split('_')[0]
        parsed_result['plane_seats'] = [item.replace(parsed_result['plane_name']+'_', '') for item in results]
    return parsed_result
