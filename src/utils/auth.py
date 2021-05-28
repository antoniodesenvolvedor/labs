from settings import app_autentication


def auth_user(request):
    try:
        username = request.authorization.username
        password = request.authorization.password

        if username != app_autentication['username'] or password != app_autentication['password']:
            return False
        else:
            return True
    except Exception as e:
        return False
