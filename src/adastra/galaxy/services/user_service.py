from typing import List

from adastra.galaxy.services.galaxy_service import GalaxyService
from adastra.galaxy.models import User


class UserService(GalaxyService):
    API_ENDPOINT = '/user'

    def list(self) -> List[User]:
        res = super()._get_list(type(self).API_ENDPOINT)
        users = [User(**user) for user in res]
        return users

    def get(self, user_id: str) -> User:
        res = super()._get_single(type(self).API_ENDPOINT, user_id)
        user = User(**res)
        return user

    def update(self, user: User) -> User:
        res = super()._patch(type(self).API_ENDPOINT, user.user_id, payload=user.model_dump(exclude_none=True))
        user = User(**res)
        return user
