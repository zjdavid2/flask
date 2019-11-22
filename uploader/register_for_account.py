import requests


def sign_up(username: str, password: str, email: str):
    base_url = 'http://127.0.0.1:5000'
    register_url = base_url + '/v1/auth/sign_up'

    data = {'username': username, 'password': password, 'email': email}

    requests.post(register_url, data)


if __name__ == '__main__':
    sign_up('zjdavid', 'torsan89', 'a@ddavid.net')
