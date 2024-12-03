from abc import ABC

from requests import Session


class SepSession(Session):

    def __init__(self, host: str, user: str, token: str, roles = str, verify: bool = True):
        super().__init__()        
        self.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': token,
            'X-Trino-User': user,
            'X-Trino-Role': f"system:{roles}"
        })
        self.sep_host = host
        self.verify = verify

    def request(self, method, url, **kwargs):
        res = super().request(method, self.sep_host + url, **kwargs)
        if res.status_code not in [200, 404, 405]:
            res.raise_for_status()
        return res


class SepService(ABC):
    def __init__(self, client: SepSession):
        self._client = client

    def _call(self, method: str, endpoint: str, params: dict = None, payload: dict = None):
        res = self._client.request(method=method, url=endpoint, params=params, json=payload)
        return res
