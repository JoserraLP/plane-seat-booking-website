from flask import Blueprint, render_template, flash, request, redirect, url_for, flash
from flask_user import roles_required
import json

from datetime import date

from website import redis, redlock, redis_lock
from website.static.constants import RESOURCE_TTL

from website.redis.utils.fill_db import fill_db as fill
from website.redis.utils.flush_db import flush_db as flush
# Admin blueprint
admin = Blueprint('admin', __name__)

# -------------- Planes -------------- #
@admin.route('/fill_db', methods=['POST'])
@roles_required(['admin'])
def fill_db():
    try:

        fill()
        flash('Successfully filled DB', 'bg-success')
        return render_template('index.html')

    except Exception as e:
        print(e)
        # Exception -> show message
        flash('Error, the db could not be filled', 'bg-error')
        return render_template('index.html')


# -------------- Planes -------------- #
@admin.route('/flush_db', methods=['POST'])
@roles_required(['admin'])
def flush_db():
    try:
        flush()
        flash('Successfully flushed DB', 'bg-success')
        return render_template('index.html')

    except Exception as e:
        print(e)
        # Exception -> show message
        flash('Error, the db could not be flushed', 'bg-error')
        return render_template('index.html')

