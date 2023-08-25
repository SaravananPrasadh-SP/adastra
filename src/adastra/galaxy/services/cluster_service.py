from typing import List

from adastra.galaxy.services.galaxy_service import GalaxyService
from adastra.galaxy.models import Cluster


class ClusterService(GalaxyService):
    API_ENDPOINT = '/cluster'

    def list(self) -> List[Cluster]:
        res = super()._get_list(type(self).API_ENDPOINT)
        clusters = [Cluster(**cluster) for cluster in res]
        return clusters

    def get(self, cluster_id: str) -> Cluster:
        res = super()._get_single(type(self).API_ENDPOINT, cluster_id)
        cluster = Cluster(**res)
        return cluster

    def create(self, cluster: Cluster) -> Cluster:
        res = super()._post(type(self).API_ENDPOINT, payload=cluster.model_dump(exclude_none=True))
        cluster = Cluster(**res)
        return cluster

    def update(self, cluster: Cluster) -> Cluster:
        res = super()._patch(type(self).API_ENDPOINT, cluster.cluster_id, payload=cluster.model_dump(exclude_none=True))
        cluster = Cluster(**res)
        return cluster

    def delete(self, cluster_id: str) -> bool:
        res = super()._delete(type(self).API_ENDPOINT, cluster_id)
        return res
