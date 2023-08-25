from enum import Enum
from typing import List, Any, Optional

from pydantic import BaseModel, Field, constr, NonNegativeInt, HttpUrl

from adastra.galaxy import ID_PATTERN


class Page(BaseModel):
    nextPageToken: str
    result: List[Any]


class BaseCatalog(BaseModel):
    catalog_id: Optional[str] = Field(default=None, pattern=ID_PATTERN, alias='catalogId')
    name: str = Field(alias='catalogName')


class Cluster(BaseModel):
    cluster_id: str = Field(pattern=ID_PATTERN, alias='clusterId')
    name: str
    cloud_region: str = Field(alias='cloudRegionId')
    catalogs: List[constr(pattern=ID_PATTERN)] = Field(default_factory=list, alias='catalogRefs')
    idle_stop_minutes: Optional[int] = Field(default=-1, alias='idleStopMinutes')
    batch: bool = Field(alias='batchCluster')
    warp: bool = Field(alias='warpSpeedCluster')
    warp_resiliency: bool = Field(alias='warpResiliencyEnabled')
    min_workers: NonNegativeInt = Field(alias='minWorkers')
    max_workers: NonNegativeInt = Field(alias='maxWorkers')
    state: Optional[str] = None
    trinoUri: Optional[HttpUrl]


class BaseUser(BaseModel):
    user_id: str = Field(pattern=ID_PATTERN, alias='userId')
    email: str


class Link(BaseModel):
    name: str
    uri: str


class Catalog(BaseCatalog):
    kind: str = Field(alias='catalogKind')
    local_regions: List[str] = Field(default_factory=list, alias='localRegions')


class DataProduct(BaseModel):
    data_product_id: Optional[str] = Field(default=None, pattern=ID_PATTERN, alias='dataProductId')
    name: str
    summary: str
    description: Optional[str] = None
    catalog: Optional[Catalog] = None  # read model
    catalog_id: Optional[str] = Field(default=None, pattern=ID_PATTERN, alias='catalogId')  # write model
    schema_name: str = Field(alias='schemaName')
    contacts: List[BaseUser]
    links: Optional[List[Link]] = None
    default_cluster_id: Optional[str] = Field(default=None, alias='defaultClusterId')


class Role(BaseModel):
    role_id: str = Field(pattern=ID_PATTERN, alias='roleId')
    name: str = Field(alias='roleName')


class BaseTag(BaseModel):
    tag_id: Optional[str] = Field(default=None, pattern=ID_PATTERN, alias='tagId')
    name: str


class Schema(BaseModel):
    schema_id: str = Field(alias='schemaId')
    description: Optional[str] = None
    owner: Optional[Role] = None
    tags: List[BaseTag]
    contacts: List[BaseUser]
    links: List[Link]


class CatalogMetadata(BaseModel):
    catalog_id: str = Field(pattern=ID_PATTERN, alias='catalogId')
    name: str = Field(alias='catalogName')
    description: Optional[str] = None
    owner: Optional[Role] = None
    tags: List[BaseTag]
    contacts: List[BaseUser]


class Table(BaseModel):
    table_id: str = Field(pattern=ID_PATTERN, alias='tableId')
    type: str = Field(alias='tableType')
    description: Optional[str] = None
    owner: Optional[Role] = None
    tags: List[BaseTag]
    contacts: List[BaseUser]


class Column(BaseModel):
    column_id: str = Field(pattern=ID_PATTERN, alias='columnId')
    data_type: Optional[str] = Field(default=None, alias='dataType')
    default: Optional[str] = Field(default=None, alias='columnDefault')
    nullable: bool
    description: Optional[str] = None
    tags: List[BaseTag]


class Tag(BaseTag):
    color: str
    description: Optional[str] = None


class PrincipalEnum(str, Enum):
    user = 'User'
    role = 'Role'
    group = 'Group'


class Principal(BaseModel):
    principal_id: str = Field(pattern=ID_PATTERN, alias='id')
    type: PrincipalEnum


class RoleGrant(Role):
    principal: Principal
    admin_option: bool = Field(alias='adminOption')


class User(BaseModel):
    user_id: str = Field(pattern=ID_PATTERN, alias='userId')
    email: str
    default_role: Optional[str] = Field(default=None, alias='defaultRoleId')
    created_on: str = Field(alias='createdOn')
    scim_managed: bool = Field(alias='scimManaged')
    directly_granted_roles: List[RoleGrant] = Field(default_factory=list, alias='directlyGrantedRoles')
    all_roles: List[RoleGrant] = Field(default_factory=list, alias='allRoles')
