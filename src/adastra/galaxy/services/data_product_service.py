from typing import List

from adastra.galaxy.services.galaxy_service import GalaxyService
from adastra.galaxy.models import DataProduct


class DataProductService(GalaxyService):
    API_ENDPOINT = '/dataProduct'

    def list(self) -> List[DataProduct]:
        res = super()._get_list(type(self).API_ENDPOINT)
        products = [DataProduct(**product) for product in res]
        return products

    def get(self, product_id: str) -> DataProduct:
        res = super()._get_single(type(self).API_ENDPOINT, product_id)
        product = DataProduct(**res)
        return product

    def create(self, product: DataProduct) -> DataProduct:
        payload = product.model_dump(exclude_none=True, by_alias=True)
        res = super()._post(type(self).API_ENDPOINT, payload=payload)
        product = DataProduct(**res)
        return product

    def update(self, product: DataProduct) -> DataProduct:
        payload = product.model_dump(exclude_none=True, by_alias=True)
        res = super()._patch(type(self).API_ENDPOINT, product.data_product_id, payload=payload)
        product = DataProduct(**res)
        return product

    def delete(self, product_id: str) -> bool:
        res = super()._delete(type(self).API_ENDPOINT, product_id)
        return res
