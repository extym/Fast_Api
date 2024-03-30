import flask_login


def roles_required(role):
    if flask_login.current_user.roles == role:
        return True
    else:
        return False