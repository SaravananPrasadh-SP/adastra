from typing import Optional, List

from pydantic import BaseModel

from adsepra.client import SepClient

DATAPRODUCT_API_BASE = '/api/v1/dataProduct'
PRODUCTS_ENDPOINT = f'{DATAPRODUCT_API_BASE}/products'
DOMAINS_ENDPOINT = f'{DATAPRODUCT_API_BASE}/domains'


class Owner(BaseModel):
    name: str
    email: str


class Column(BaseModel):
    name: str
    type: str
    description: Optional[str] = ''


class View(BaseModel):
    name: str
    description: Optional[str] = None
    definitionQuery: str
    columns: Optional[List[Column]] = None


class DefinitionProperties(BaseModel):
    refresh_interval: str
    incremental_column: Optional[str] = None


class MaterializedView(BaseModel):
    definitionProperties: Optional[DefinitionProperties] = None


class Link(BaseModel):
    label: str
    url: str


class DataProduct(BaseModel):
    id: Optional[str] = None
    name: str
    catalogName: str
    dataDomainId: str
    summary: str
    description: str
    owners: Optional[list[Owner]] = None
    views: Optional[list[View]] = None
    materializedViews: Optional[list[MaterializedView]] = None
    relevantLinks: Optional[list[Link]] = None


class Domain(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    schemaLocation: Optional[str] = None


class SampleQuery(BaseModel):
    name: str
    query: str


class Tag(BaseModel):
    id: Optional[str] = None
    value: str


class DataProductsApiClient(BaseModel):
    client: SepClient

    def list_data_products(self) -> List[DataProduct]:
        res = self.client.get(DOMAINS_ENDPOINT)
        ids = [dp['id'] for domain in res.json() for dp in domain['assignedDataProducts']]
        data_products = [self.get_data_product(uuid) for uuid in ids]
        return data_products

    def list_domains(self):
        res = self.client.get(DOMAINS_ENDPOINT)
        domains = [Domain(**data) for data in res.json()]
        return domains

    def create_data_product(self, data_product: DataProduct):
        res = self.client.post(PRODUCTS_ENDPOINT, data_product.model_dump(exclude_none=True))
        data_product = DataProduct(**res.json())
        return data_product

    def create_domain(self, domain: Domain):
        res = self.client.post(DOMAINS_ENDPOINT, domain.model_dump(exclude_none=True))
        domain = Domain(**res.json())
        return domain

    def get_data_product(self, uuid: str):
        res = self.client.get(f'{PRODUCTS_ENDPOINT}/{uuid}')
        data_product = DataProduct(**res.json())
        return data_product

    def get_data_product_samples(self, uuid: str):
        res = self.client.get(f'{PRODUCTS_ENDPOINT}/{uuid}/sampleQueries')
        sq = [SampleQuery(**s) for s in res.json()]
        return sq

    def get_data_product_tags(self, uuid: str):
        res = self.client.get(f'{DATAPRODUCT_API_BASE}/tags/products/{uuid}')
        tags = [Tag(**t) for t in res.json()]
        return tags

    def get_domain(self, uuid: str):
        res = self.client.get(f'{DOMAINS_ENDPOINT}/{uuid}')
        domain = Domain(**res.json())
        return domain

    def update_data_product(self, data_product: DataProduct):
        res = self.client.put(f'{PRODUCTS_ENDPOINT}/{data_product.id}', data_product.model_dump(exclude_none=True))
        data_product = DataProduct(**res.json())
        return data_product

    def set_data_product_samples(self, uuid: str, queries: [SampleQuery]):
        payload = [sq.model_dump(exclude_none=True) for sq in queries]
        res = self.client.put(f'{PRODUCTS_ENDPOINT}/{uuid}/sampleQueries', payload)
        return res.status_code == 204

    def set_data_product_tags(self, uuid: str, tags: [Tag]):
        payload = [t.model_dump(exclude_none=True) for t in tags]
        res = self.client.put(f'{PRODUCTS_ENDPOINT}/tags/products/{uuid}', payload)
        return res.status_code == 204

    def reassign_data_product_domain(self, product_uuid: str, domain_uuid: str):
        res = self.client.post(f'{PRODUCTS_ENDPOINT}/reassignDomain', {
            'dataProductsIds': [product_uuid],
            'newDomainId': domain_uuid
        })
        return res.status_code == 204

    def update_domain(self, domain: Domain):
        res = self.client.put(f'{DOMAINS_ENDPOINT}/{domain.id}', domain.model_dump(exclude_none=True))
        domain = Domain(**res.json())
        return domain

    def delete_data_product(self, uuid: str) -> bool:
        res = self.client.post(f'{PRODUCTS_ENDPOINT}/{uuid}/workflows/delete', None)
        # warten, bis es tatsächlich gelöscht wurde?
        return res.status_code == 202

    def delete_domain(self, uuid: str) -> bool:
        res = self.client.delete(f'{DOMAINS_ENDPOINT}/{uuid}')
        return res.status_code == 204

    def publish_data_product(self, uuid: str):
        res = self.client.post(f'{PRODUCTS_ENDPOINT}/{uuid}/workflows/publish', None)
        return res.status_code == 202