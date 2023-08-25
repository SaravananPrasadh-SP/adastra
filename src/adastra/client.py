from adastra.galaxy.services.catalog_service import CatalogService
from adastra.galaxy.services.cluster_service import ClusterService
from adastra.galaxy.services.data_product_service import DataProductService as GalaxyDataProductService
from adastra.galaxy.services.discovery_service import DiscoveryService
from adastra.galaxy.services.galaxy_service import GalaxySession
from adastra.galaxy.services.tag_service import TagService
from adastra.galaxy.services.user_service import UserService
from adastra.sep.services.data_product_service import DataProductService as SepDataProductService
from adastra.sep.services.domain_service import DomainService
from adastra.sep.services.sep_service import SepSession


class GalaxyClient:
    def __init__(self, host: str, client_id: str, client_secret: str):
        self._session = GalaxySession(host, client_id, client_secret)

    def catalog_service(self) -> CatalogService:
        return CatalogService(self._session)

    def cluster_service(self) -> ClusterService:
        return ClusterService(self._session)

    def data_product_service(self) -> GalaxyDataProductService:
        return GalaxyDataProductService(self._session)

    def discovery_service(self) -> DiscoveryService:
        return DiscoveryService(self._session)

    def tag_service(self) -> TagService:
        return TagService(self._session)

    def user_service(self) -> UserService:
        return UserService(self._session)


class SepClient:
    def __init__(self, host: str, user: str, token: str):
        self._session = SepSession(host=host, user=user, token=token)

    def domain_service(self) -> DomainService:
        return DomainService(self._session)

    def data_product_service(self) -> SepDataProductService:
        return SepDataProductService(self._session)
