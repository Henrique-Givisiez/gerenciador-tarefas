from flask import g, render_template
from functools import wraps

def requires_login():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'user') or g.user is None:
                return render_template("login.html", msg="Usuário não logado!")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

