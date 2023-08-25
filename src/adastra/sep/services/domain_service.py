from typing import List

from pydantic import validate_call

from adastra.sep import DOMAINS_ENDPOINT
from adastra.sep.models import Domain, UuidStr, UuidStrValidator
from adastra.sep.services.sep_service import SepService


class DomainService(SepService):

    def list(self) -> List[Domain]:
        res = super()._call('GET', DOMAINS_ENDPOINT)
        domains = [Domain(**data) for data in res.json()]
        return domains

    @validate_call
    def get(self, domain_id: UuidStr) -> Domain:
        res = super()._call(method='GET', endpoint=f'{DOMAINS_ENDPOINT}/{domain_id}')
        domain = Domain(**res.json()) if res.status_code == 200 else None
        return domain

    def create(self, domain: Domain) -> Domain:
        res = super()._call(method='POST', endpoint=DOMAINS_ENDPOINT, payload=domain.model_dump(exclude_none=True))
        domain = Domain(**res.json())
        return domain

    def update(self, domain: Domain) -> Domain:
        UuidStrValidator.validate_python(domain.id)
        res = super()._call(method='PUT', endpoint=f'{DOMAINS_ENDPOINT}/{domain.id}', payload=domain.model_dump(exclude_none=True))
        domain = Domain(**res.json()) if res.status_code == 200 else None
        return domain

    @validate_call
    def delete(self, domain_id: UuidStr) -> bool:
        res = super()._call(method='DELETE', endpoint=f'{DOMAINS_ENDPOINT}/{domain_id}')
        return res.status_code == 204
