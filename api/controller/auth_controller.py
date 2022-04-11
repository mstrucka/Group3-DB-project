from bottle import route, get, post, put, auth_basic

def check_auth(user, password):
    print(user, password)

get('/authenticate')
@auth_basic(check_auth)
def authenticate():
    pass