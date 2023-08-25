from typing import List

from pydantic import validate_call

from adastra.sep import DOMAINS_ENDPOINT, PRODUCTS_ENDPOINT, DATAPRODUCT_API_BASE
from adastra.sep.models import Domain, UuidStr, DataProduct, SampleQuery, Tag
from adastra.sep.services.sep_service import SepService


class DataProductService(SepService):

    def list(self) -> List[DataProduct]:
        res = super()._call(method='GET', endpoint=DOMAINS_ENDPOINT)
        ids = [dp['id'] for domain in res.json() for dp in domain['assignedDataProducts']]
        data_products = [self.get(data_product_id) for data_product_id in ids]
        return data_products

    @validate_call
    def get(self, data_product_id: UuidStr) -> DataProduct:
        res = super()._call(method='GET', endpoint=f'{PRODUCTS_ENDPOINT}/{data_product_id}')
        data_product = DataProduct(**res.json()) if res.status_code == 200 else None
        return data_product

    @validate_call
    def get_samples(self, data_product_id: UuidStr):
        res = super()._call(method='GET', endpoint=f'{PRODUCTS_ENDPOINT}/{data_product_id}/sampleQueries')
        sq = [SampleQuery(**s) for s in res.json()] if res.status_code == 200 else None
        return sq

    @validate_call
    def get_tags(self, data_product_id: UuidStr):
        res = super()._call(method='GET', endpoint=f'{DATAPRODUCT_API_BASE}/tags/products/{data_product_id}')
        tags = [Tag(**t) for t in res.json()] if res.status_code == 200 else None
        return tags

    def create(self, data_product: DataProduct) -> DataProduct:
        res = super()._call('POST', endpoint=PRODUCTS_ENDPOINT, payload=data_product.model_dump(exclude_none=True))
        data_product = DataProduct(**res.json())
        return data_product

    def update(self, data_product: DataProduct) -> DataProduct:
        res = super()._call(method='PUT', endpoint=f'{PRODUCTS_ENDPOINT}/{data_product.id}', payload=data_product.model_dump(exclude_none=True))
        data_product = DataProduct(**res.json())
        return data_product

    def set_samples(self, data_product_id: UuidStr, queries: [SampleQuery]) -> bool:
        payload = [sq.model_dump(exclude_none=True) for sq in queries]
        res = super()._call(method='PUT', endpoint=f'{PRODUCTS_ENDPOINT}/{data_product_id}/sampleQueries', payload=payload)
        return res.status_code == 204

    def set_tags(self, data_product_id: UuidStr, tags: [Tag]) -> bool:
        payload = [t.model_dump(exclude_none=True) for t in tags]
        res = super()._call(method='PUT', endpoint=f'{DATAPRODUCT_API_BASE}/tags/products/{data_product_id}', payload=payload)
        return res.status_code == 204

    @validate_call
    def delete(self, data_product_id: UuidStr) -> bool:
        res = super()._call(method='DELETE', endpoint=f'{PRODUCTS_ENDPOINT}/{data_product_id}/workflows/delete')
        return res.status_code == 202

    @validate_call
    def reassign(self, data_product_id: UuidStr, domain_id: UuidStr) -> bool:
        payload = {
            'dataProductsIds': [data_product_id],
            'newDomainId': domain_id
        }
        res = super()._call(method='POST', endpoint=f'{PRODUCTS_ENDPOINT}/reassignDomain', payload=payload)
        return res.status_code == 204

    @validate_call
    def publish(self, data_product_id: UuidStr) -> bool:
        res = super()._call(method='POST', endpoint=f'{PRODUCTS_ENDPOINT}/{data_product_id}/workflows/publish')
        return res.status_code == 202
