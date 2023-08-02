import requests
from pydantic import BaseModel


class SepClient(BaseModel):
    host: str
    user: str
    token: str

    def __int__(self, **data):
        super().__init__(**data)
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.token,
            'X-Trino-User': self.user
        })
        self.client = session

    def get(self, endpoint: str, params=None):
        return self.client.get(self.base_url + endpoint, params=params)

    def post(self, endpoint: str, payload: dict):
        return self.client.post(self.base_url + endpoint, json=payload)

    def put(self, endpoint: str, payload: dict):
        return self.client.put(self.base_url + endpoint, json=payload)

    def delete(self, endpoint: str):
        return self.client.delete(self.base_url + endpoint)
