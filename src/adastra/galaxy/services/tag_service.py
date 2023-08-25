from typing import List

from adastra.galaxy.services.galaxy_service import GalaxyService
from adastra.galaxy.models import Tag


class TagService(GalaxyService):
    API_ENDPOINT = '/tag'

    def list(self) -> List[Tag]:
        res = super()._get_list(type(self).API_ENDPOINT)
        tags = [Tag(**tag) for tag in res]
        return tags

    def get(self, tag_id: str) -> Tag:
        res = super()._get_single(type(self).API_ENDPOINT, tag_id)
        tag = Tag(**res)
        return tag

    def create(self, tag: Tag) -> Tag:
        res = super()._post(type(self).API_ENDPOINT, payload=tag.model_dump(exclude_none=True))
        tag = Tag(**res)
        return tag

    def update(self, tag: Tag) -> Tag:
        res = super()._patch(type(self).API_ENDPOINT, tag.tag_id, payload=tag.model_dump(exclude_none=True))
        tag = Tag(**res)
        return tag

    def delete(self, tag_id: str) -> bool:
        res = super()._delete(type(self).API_ENDPOINT, tag_id)
        return res

    def apply_tag_to_catalog(self, tag_id: str, catalog_id: str):
        res = super()._put(type(self).API_ENDPOINT, f'{tag_id}/catalog/{catalog_id}')
        return res

    def remove_tag_from_catalog(self, tag_id: str, catalog_id: str):
        res = super()._delete(type(self).API_ENDPOINT, f'{tag_id}/catalog/{catalog_id}')
        return res

    def apply_tag_to_schema(self, tag_id: str, catalog_id: str, schema_id: str):
        res = super()._put(type(self).API_ENDPOINT, f'{tag_id}/catalog/{catalog_id}/schema/{schema_id}')
        return res

    def remove_tag_from_schema(self, tag_id: str, catalog_id: str, schema_id: str):
        res = super()._delete(type(self).API_ENDPOINT, f'{tag_id}/catalog/{catalog_id}/schema/{schema_id}')
        return res

    def apply_tag_to_table(self, tag_id: str, catalog_id: str, schema_id: str, table_id: str):
        entities = f'{tag_id}/catalog/{catalog_id}/schema/{schema_id}/table/{table_id}'
        res = super()._put(type(self).API_ENDPOINT, entities)
        return res

    def remove_tag_from_table(self, tag_id: str, catalog_id: str, schema_id: str, table_id: str):
        entities = f'{tag_id}/catalog/{catalog_id}/schema/{schema_id}/table/{table_id}'
        res = super()._delete(type(self).API_ENDPOINT, entities)
        return res

    def apply_tag_to_column(self, tag_id: str, catalog_id: str, schema_id: str, table_id: str, column_id: str):
        entities = f'{tag_id}/catalog/{catalog_id}/schema/{schema_id}/table/{table_id}/column/{column_id}'
        res = super()._put(type(self).API_ENDPOINT, entities)
        return res

    def remove_tag_from_column(self, tag_id: str, catalog_id: str, schema_id: str, table_id: str, column_id: str):
        entities = f'{tag_id}/catalog/{catalog_id}/schema/{schema_id}/table/{table_id}/column/{column_id}'
        res = super()._delete(type(self).API_ENDPOINT, entities)
        return res
