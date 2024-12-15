from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if 'user_id' is in the session
        if 'user_id' not in session:
            return redirect("/")  # Redirect to the login page if not logged in
        return f(*args, **kwargs)
    return decorated_function
