from flask import Blueprint, render_template, flash
from flask_user import roles_required

from website.redis_db.utils.fill_db import fill_db as fill
from website.redis_db.utils.flush_db import flush_db as flush

# Admin blueprint
admin = Blueprint('admin', __name__)


@admin.route('/fill_db', methods=['POST'])
@roles_required(['admin'])
def fill_db():
    try:
        # Fill database
        fill()
        flash('Successfully filled DB', 'bg-light-green')
        return render_template('index.html')

    except Exception as e:
        print(e)
        # Exception -> show message
        flash('Error, the db could not be filled', 'bg-error')
        return render_template('index.html')


@admin.route('/flush_db', methods=['POST'])
@roles_required(['admin'])
def flush_db():
    try:
        # Flush database
        flush()
        flash('Successfully flushed DB', 'bg-light-green')
        return render_template('index.html')

    except Exception as e:
        print(e)
        # Exception -> show message
        flash('Error, the db could not be flushed', 'bg-error')
        return render_template('index.html')