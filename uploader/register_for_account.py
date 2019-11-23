import requests
import bcrypt

base_url = 'http://127.0.0.1:5000'


def sign_up(username: str, password: str, email: str):
    register_url = base_url + '/v1/auth/sign_up'
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    data = {'username': username, 'password': hashed_password, 'email': email}

    r = requests.post(register_url, data)
    return r.json()['jwt']


def sign_up_accept(auth_code):
    register_accept_url = base_url + '/v1/auth/sign_up_accept'
    r = requests.get(register_accept_url, params={'auth_code': auth_code})
    print(r.json())


def login(username, password):
    login_url = base_url + '/v1/auth/login'
    r = requests.post(login_url, data={'username': username, 'password': password})
    print(r.json())
    return r.json()['jwt']


if __name__ == '__main__':
    username = 'zjdavid'
    password = 'torsan89'
    auth_code = sign_up(username, password, 'a@ddavid.net')
    sign_up_accept(auth_code)
    login(username, password)