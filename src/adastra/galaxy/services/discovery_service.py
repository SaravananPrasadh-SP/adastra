from typing import List

from adastra.galaxy.services.galaxy_service import GalaxyService
from adastra.galaxy.models import Schema, CatalogMetadata, Table, Column


class DiscoveryService(GalaxyService):
    API_ENDPOINT = '/catalog'

    def list_schemas(self, catalog_id: str) -> List[Schema]:
        res = super()._get_list(f'{type(self).API_ENDPOINT}/{catalog_id}/schema')
        schemas = [Schema(**schema) for schema in res]
        return schemas

    def get_catalog_metadata(self, catalog_id: str) -> CatalogMetadata:
        res = super()._get_single(type(self).API_ENDPOINT, f'{catalog_id}/catalogMetadata')
        catalog_metadata = CatalogMetadata(**res)
        return catalog_metadata

    def list_tables(self, catalog_id: str, schema_id: str) -> List[Table]:
        endpoint = f'{type(self).API_ENDPOINT}/{catalog_id}/schema/{schema_id}/table'
        res = super()._get_list(endpoint)
        tables = [Table(**table) for table in res]
        return tables

    def list_columns(self, catalog_id: str, schema_id: str, table_id) -> List[Column]:
        endpoint = f'{type(self).API_ENDPOINT}/{catalog_id}/schema/{schema_id}/table/{table_id}/column'
        res = super()._get_list(endpoint)
        columns = [Column(**column) for column in res]
        return columns
