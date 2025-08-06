from ..config import ACCESS_TOKEN_FILE_PATH, API_BASE_URL, TRANSLATIONS_FILES_FOLDER
from requests import Session
import os
import json

def store_access_token(token: str):
    with open(ACCESS_TOKEN_FILE_PATH, "w") as f:
        f.write(token)
        
def get_access_token() -> str:
    with open(ACCESS_TOKEN_FILE_PATH, "r") as f:
        return f.read()


class ServiceError(Exception):
    def __init__(self, error: str, message: str):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def get_translated_message(self, lang='pt-BR') -> str:
        with open(os.path.join(TRANSLATIONS_FILES_FOLDER, f'{lang}.json'), 'r', encoding='utf-8') as f:
            translations = json.loads(f.read())
            return translations[self.error]

def REQUEST(session: Session, method: str, path: str, json: dict | None = None):
    response = session.request(method, f'{API_BASE_URL}{path}', json=json)
    response_json = response.json()
    if not response.ok:
        raise ServiceError(error=response_json['error'], message=response_json['message'])
    return response_json