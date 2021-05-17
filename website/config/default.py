"""Flask config."""

SECRET_KEY = 'super_secret_key_for_testing_purpose'

# -------------- Flask-User -------------- #
USER_APP_NAME = "Plane Seat Booking Website"  # Shown in and email templates and page footers
USER_ENABLE_EMAIL = True  # Enable email authentication
USER_ENABLE_USERNAME = False  # Disable username authentication
USER_EMAIL_SENDER_NAME = USER_APP_NAME
USER_EMAIL_SENDER_EMAIL = "noreply@example.com"

# -------------- SQLAlchemy - DB -------------- #
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # This will be deprecated in the future
