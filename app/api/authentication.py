from flask_ext import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(id_or_token, password):
    if password == '':
        g.current_user = User.verify_auth_token(id_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(id=id_or_token).first()
    if not user:
        return False

    g.current_user = user
    g.token_used = False
    return user.verify_password(password)
