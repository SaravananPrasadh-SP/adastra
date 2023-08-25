import pytest
from pydantic import ValidationError
from requests import HTTPError

from adsepra.dataproducts import DataProduct, Owner, View
import utils


@pytest.mark.vcr
def test_list_products(client):
    products = client.list_data_products()
    assert len(products) == 4


@pytest.mark.vcr
def test_create_product(request, client):
    product = utils.valid_product
    new_product = client.create_data_product(product)
    assert new_product.id is not None
    assert new_product.name == product.name
    request.config._data['product'] = [new_product]


@pytest.mark.vcr
@pytest.mark.parametrize('product', [
    utils.invalid_product_missing_name,
    utils.invalid_product_empty_name,
    utils.invalid_product_missing_catalog,
    utils.invalid_product_empty_catalog,
    # utils.invalid_product_wrong_catalog,  # the API itself allows this -> Todo: open a bug?
    utils.invalid_product_missing_domain,
    utils.invalid_product_empty_domain,
    utils.invalid_product_wrong_domain,
    utils.invalid_product_missing_summary,
    utils.invalid_product_empty_summary
])
def test_create_invalid_product(client, product):
    with pytest.raises(HTTPError):
        client.create_data_product(product)


@pytest.mark.vcr
@pytest.mark.parametrize('product', [
    utils.product_without_owner,
    utils.product_without_datasets
])
def test_create_incomplete_product(request, client, product):
    new_product = client.create_data_product(product)
    product.id = new_product.id
    assert new_product.id is not None
    assert new_product.name == product.name
    #request.config._data['product'].append(new_product)


@pytest.mark.vcr
@pytest.mark.parametrize('product', [
    utils.product_without_owner,
    utils.product_without_datasets
])
def test_get_product(client, product):
    candidate = client.get_data_product(product.id)
    assert candidate.id == product.id
    assert candidate.name == product.name


@pytest.mark.vcr
@pytest.mark.parametrize('uuid', [
    None,
    '',
    'abc'
])
def test_get_product_with_invalid_id(client, uuid):
    with pytest.raises(ValidationError):
        client.get_data_product(uuid)


@pytest.mark.vcr
def test_get_product_with_non_existing_id(client):
    assert client.get_data_product('11111111-1111-1111-111111111111') is None


@pytest.mark.vcr
@pytest.mark.parametrize('uuid', 'expected', [
    ('17597f6e-4b52-4505-bf3b-3544a026ae52', 0),  # Environmental
    ('ae5d81d8-bda3-4cfc-9354-ad2d26f74591', 2)   # Federation Sample Product
])
def test_get_samples(client, uuid, expected):
    samples = client.get_data_product_samples(uuid)
    assert samples is not None
    assert len(samples) == expected


@pytest.mark.vcr
@pytest.mark.parametrize('uuid', [
    None,
    '',
    'abc'
])
def test_get_samples_with_invalid_id(client, uuid):
    with pytest.raises(ValidationError):
        client.get_data_product_samples(uuid)


@pytest.mark.vcr
def test_get_samples_with_non_existing_id(client):
    assert client.get_data_product_samples('11111111-1111-1111-111111111111') is None


@pytest.mark.vcr
@pytest.mark.parametrize('uuid', 'expected', [
    ('17597f6e-4b52-4505-bf3b-3544a026ae52', 0),  # Environmental
    ('ae5d81d8-bda3-4cfc-9354-ad2d26f74591', 2)   # Federation Sample Product
])
def test_get_tags(client, uuid, expected):
    tags = client.get_data_product_tags(uuid)
    assert tags is not None
    assert len(tags) == expected


@pytest.mark.vcr
@pytest.mark.parametrize('uuid', [
    None,
    '',
    'abc'
])
def test_get_tags_with_invalid_id(client, uuid):
    with pytest.raises(ValidationError):
        client.get_data_product_tags(uuid)


@pytest.mark.vcr
def test_get_tags_with_non_existing_id(client):
    assert client.get_data_product_tags('11111111-1111-1111-111111111111') is None


def test_update_product():
    pass


def test_update_product_without_id():
    pass


def test_update_invalid_product():
    pass


def test_update_incomplete_product():
    pass


def test_set_product_samples():
    pass


def test_set_product_samples_invalid_uuid():
    pass


def test_set_product_samples_non_existing_uuid():
    pass


def test_set_product_invalid_samples():
    """Expect HTTP 400"""
    pass


def test_set_product_tags():
    pass


def test_set_product_tags_invalid_uuid():
    pass


def test_set_product_tags_non_existing_uuid():
    pass


def test_set_product_invalid_tags():
    """Expect HTTP 400"""
    pass


def test_reassign_product_domain():
    pass


def test_reassign_product_domain_invalid_uuids():
    pass


def test_reassign_product_domain_wrong_uuids():
    pass


def test_publish_product():
    pass


def test_publish_product_with_invalid_id():
    pass


def test_publish_product_with_non_existing_id():
    pass


def test_publish_incomplete_product():
    with pytest.raises(Exception):
        pass


def test_delete_product():
    pass


def test_delete_product_with_invalid_id():
    pass


def test_delete_product_with_non_existing_id():
    pass
