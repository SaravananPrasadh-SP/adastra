from typing import List

from adastra.galaxy.services.galaxy_service import GalaxyService
from adastra.galaxy.models import BaseCatalog


class CatalogService(GalaxyService):
    API_ENDPOINT = '/catalog'

    def list(self) -> List[BaseCatalog]:
        res = super()._get_list(type(self).API_ENDPOINT)
        catalogs = [BaseCatalog(**catalog) for catalog in res]
        return catalogs
