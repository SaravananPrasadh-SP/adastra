import requests
from pydantic import BaseModel, PrivateAttr
from requests import Session


class SepSession(Session):

    def __init__(self, user: str, token: str):
        super().__init__()
        self.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': token,
            'X-Trino-User': user
        })

    def request(self, method, url, **kwargs):
        res = super().request(method, url, **kwargs)
        if res.status_code not in [200, 404, 405]:
            res.raise_for_status()
        return res


class SepClient(BaseModel):
    host: str
    user: str
    token: str
    _client: SepSession = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._client = SepSession(self.user, self.token)

    def get(self, endpoint: str, params=None):
        return self._client.get(self.host + endpoint, params=params)

    def post(self, endpoint: str, payload: dict):
        return self._client.post(self.host + endpoint, json=payload)

    def put(self, endpoint: str, payload: dict):
        return self._client.put(self.host + endpoint, json=payload)

    def delete(self, endpoint: str):
        return self._client.delete(self.host + endpoint)
