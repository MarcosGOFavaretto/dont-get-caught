import requests

from ..config import API_BASE_URL

GLOBAL_SESSION = requests.Session()
GLOBAL_SESSION.headers.update({'Content-Type': 'application/json'})

from .service_utils import REQUEST

def create(name: str, email: str, password: str) -> dict:
    json_data = {
        'name': name,
        'email': email,
        'password': password,
    }

    response = REQUEST(GLOBAL_SESSION, 'POST', '/v1/users', json_data)

    return response

def login(email: str, password: str) -> dict:
    json_data = {
        'email': email,
        'password': password,
    }

    response = REQUEST(GLOBAL_SESSION, 'POST', '/v1/auth/login', json_data)

    return response

def profile_me() -> dict:
    response = REQUEST(GLOBAL_SESSION, 'GET', '/v1/profile/me', use_access_token=True)

    return response