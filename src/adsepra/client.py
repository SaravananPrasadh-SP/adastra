import requests
from pydantic import BaseModel, PrivateAttr
from requests import Session


class SepClient(BaseModel):
    host: str
    user: str
    token: str
    _client: Session = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.token,
            'X-Trino-User': self.user
        })
        self._client = session

    def get(self, endpoint: str, params=None):
        return self._client.get(self.host + endpoint, params=params)

    def post(self, endpoint: str, payload: dict):
        return self._client.post(self.host + endpoint, json=payload)

    def put(self, endpoint: str, payload: dict):
        return self._client.put(self.host + endpoint, json=payload)

    def delete(self, endpoint: str):
        return self._client.delete(self.host + endpoint)
