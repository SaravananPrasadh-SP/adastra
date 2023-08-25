from abc import ABC
from typing import Dict, List

from pydantic import validate_call, constr

from adastra.galaxy import API_BASE_URL, ID_PATTERN
from adastra.galaxy.models import Page

from requests import Session
from requests.auth import HTTPBasicAuth


class GalaxySession(Session):

    def __init__(self, host: str, client_id: str, client_secret: str):
        super().__init__()
        self.initialized = False
        self.galaxy_host = host
        basic = HTTPBasicAuth(client_id, client_secret)
        payload = {'grant_type': 'client_credentials'}
        auth_response = self.post('/oauth/v2/token', data=payload, auth=basic)

        if auth_response.status_code == 200:
            token = auth_response.json()['access_token']
            self.headers.update({
                'Authorization': f'Bearer {token}',
            })
        else:
            auth_response.raise_for_status()

        self.initialized = True

    def request(self, method, url, **kwargs):
        return super().request(method, self.galaxy_host + url, **kwargs)


class GalaxyService(ABC):
    def __init__(self, client: GalaxySession):
        self._client = client

    def _call(self, method: str, endpoint: str, params: dict = None, payload: dict = None):
        url = API_BASE_URL + endpoint
        res = self._client.request(method=method, url=url, params=params, json=payload)
        res.raise_for_status()
        return res.json() if res.status_code == 200 else None

    @validate_call
    def _get_single(self, endpoint: str, entity_id: constr(pattern=ID_PATTERN)) -> Dict:
        res = self._call('GET', f'{endpoint}/{entity_id}')
        return res

    def _get_list(self, endpoint: str) -> List[Dict]:
        results = []
        page_token = None

        while True:
            res = self._call('GET', endpoint, params={'pageToken': page_token})
            page = Page(**res)
            page_token = page.nextPageToken

            results.extend(page.result)

            if not page_token:
                break

        return results

    def _post(self, endpoint: str, payload: Dict = None) -> Dict:
        res = self._call('POST', f'{endpoint}', payload=payload)
        return res

    def _patch(self, endpoint: str, entity_id: str, payload: Dict = None) -> Dict:
        res = self._call('PATCH', f'{endpoint}/{entity_id}', payload=payload)
        return res

    def _delete(self, endpoint: str, entity_id: str) -> bool:
        res = self._call('DELETE', f'{endpoint}/{entity_id}')
        return True

    # TODO: Ich weiß nicht, ob das hinhaut
    def _put(self, endpoint: str, entity_id: str) -> bool:
        res = self._call('PUT', f'{endpoint}/{entity_id}')
        return True
