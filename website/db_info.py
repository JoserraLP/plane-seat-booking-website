from flask import Blueprint, render_template, flash, request, redirect, url_for, flash
from flask_user import roles_required

from planes import get_all_planes, get_all_locks

# Admin blueprint
db_info = Blueprint('db_info', __name__)


@db_info.route('/db', methods=['GET'])
@roles_required(['admin'])
def db():
    # Show db info html
    return render_template('db_info.html')


@db_info.route('/show_db_info', methods=['GET'])
@roles_required(['admin'])
def show_db_info():
    try:
        # Retrieve all planes and remove unused keys (seats)
        planes = get_all_planes()
        for k, v in planes.items():
            planes[k].pop('seats')

        return render_template('db_info.html', info=planes)

    except Exception as e:
        print(e)
        # Exception -> show message
        flash('Error with the db', 'bg-error')
        return render_template('index.html')


@db_info.route('/show_locks_info', methods=['GET'])
@roles_required(['admin'])
def show_locks_info():
    try:
        return render_template('db_info.html', info=get_all_locks())

    except Exception as e:
        print(e)
        # Exception -> show message
        flash('Error with the db', 'bg-error')
        return render_template('index.html')
