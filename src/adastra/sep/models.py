from typing import Annotated, Optional, List
from uuid import UUID

from pydantic import AfterValidator, PlainSerializer, WithJsonSchema, TypeAdapter, BaseModel

UuidStr = Annotated[
    UUID,
    AfterValidator(lambda x: str(x)),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]
UuidStrValidator = TypeAdapter(UuidStr)


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


class MaterializedView(View):
    definitionProperties: Optional[DefinitionProperties] = None


class Link(BaseModel):
    label: str
    url: str


class DataProduct(BaseModel):
    id: Optional[UuidStr] = None
    name: str
    catalogName: str
    dataDomainId: UuidStr
    summary: str
    status: Optional[str] = None
    description: Optional[str] = ''
    owners: Optional[list[Owner]] = None
    views: Optional[list[View]] = None
    materializedViews: Optional[list[MaterializedView]] = None
    relevantLinks: Optional[list[Link]] = None


class Domain(BaseModel):
    id: Optional[UuidStr] = None
    name: str
    description: Optional[str] = None
    schemaLocation: Optional[str] = None


class SampleQuery(BaseModel):
    name: str
    query: str


class Tag(BaseModel):
    id: Optional[UuidStr] = None
    value: str
