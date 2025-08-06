import requests

from ..config import API_BASE_URL

GLOBAL_SESSION = requests.Session()
GLOBAL_SESSION.headers.update({'Content-Type': 'application/json'})

from .service_utils import REQUEST

def user_create(name: str, email: str, password: str) -> dict:
    json_data = {
        'name': name,
        'email': email,
        'password': password,
    }

    response = REQUEST(GLOBAL_SESSION, 'POST', '/v1/users', json_data)

    return response

def user_login(email: str, password: str) -> dict:
    json_data = {
        'email': email,
        'password': password,
    }

    response = REQUEST(GLOBAL_SESSION, 'POST', '/v1/auth/login', json_data)

    return response