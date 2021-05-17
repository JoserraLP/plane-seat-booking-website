import datetime

from models import User, Role
from werkzeug.security import generate_password_hash


def insert_user_data(db):
    """
    Insert data in the database

        Parameters:
            db (object): database instance

    """

    try:
        # ------- User ------- #

        user = User(
            email="admin@admin.com",
            password=generate_password_hash("admin", method='sha256'),
            name="admin",
            # Necessary to redirect to authorized views
            email_confirmed_at=datetime.datetime.utcnow()
        )

        user.roles.append(Role(name='admin'))

        db.session.add(user)

        user = User(
            email="p_country_spain@gmail.com",
            password=generate_password_hash("admin", method='sha256'),
            name="Country politician",
            # Necessary to redirect to authorized views
            email_confirmed_at=datetime.datetime.utcnow()
        )

        user.roles.append(Role(name='politician_country'))

        db.session.add(user)

        user = User(
            email="p_country_france@gmail.com",
            password=generate_password_hash("admin", method='sha256'),
            name="Country politician",
            # Necessary to redirect to authorized views
            email_confirmed_at=datetime.datetime.utcnow()
        )

        # Search the role
        politician_country_role = db.session.query(Role).filter_by(name="politician_country").first()

        user.roles.append(politician_country_role)

        db.session.add(user)

        user = User(
            email="p_admin_area_extremadura@gmail.com",
            password=generate_password_hash("admin", method='sha256'),
            name="Admin area politician",
            # Necessary to redirect to authorized views
            email_confirmed_at=datetime.datetime.utcnow()
        )

        user.roles.append(Role(name='politician_admin_area'))

        db.session.add(user)

        user = User(
            email="p_admin_area_andalucia@gmail.com",
            password=generate_password_hash("admin", method='sha256'),
            name="Admin area politician",
            # Necessary to redirect to authorized views
            email_confirmed_at=datetime.datetime.utcnow()
        )

        # Search the role
        politician_admin_area_role = db.session.query(Role).filter_by(name="politician_admin_area").first()

        user.roles.append(politician_admin_area_role)

        db.session.add(user)

        user = User(
            email="p_locality_badajoz@gmail.com",
            password=generate_password_hash("admin", method='sha256'),
            name="Locality politician",
            # Necessary to redirect to authorized views
            email_confirmed_at=datetime.datetime.utcnow()
        )

        user.roles.append(Role(name='politician_locality'))

        db.session.add(user)

        user = User(
            email="p_locality_caceres@gmail.com",
            password=generate_password_hash("admin", method='sha256'),
            name="Locality politician",
            # Necessary to redirect to authorized views
            email_confirmed_at=datetime.datetime.utcnow()
        )

        # Search the role
        politician_locality_role = db.session.query(Role).filter_by(name="politician_locality").first()

        user.roles.append(politician_locality_role)

        db.session.add(user)

        user = User(
            email="police_badajoz@gmail.com",
            password=generate_password_hash("admin", method='sha256'),
            name="Police",
            # Necessary to redirect to authorized views
            email_confirmed_at=datetime.datetime.utcnow()
        )

        user.roles.append(Role(name='police'))

        db.session.add(user)

        user = User(
            email="police_caceres@gmail.com",
            password=generate_password_hash("admin", method='sha256'),
            name="Police",
            # Necessary to redirect to authorized views
            email_confirmed_at=datetime.datetime.utcnow()
        )

        # Search the role
        police_role = db.session.query(Role).filter_by(name="police").first()

        user.roles.append(police_role)

        db.session.add(user)

        db.session.commit()
    except Exception as e:
        print(e)
