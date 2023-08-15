import pytest
from pydantic import ValidationError
from requests import HTTPError

from adsepra import DataProductsApiClient, SepClient
from adsepra.dataproducts import Domain


# Todo: mock away SepClient
# Todo: create test cases for the client itself

@pytest.mark.vcr
def test_list_products(client):
    products = client.list_data_products()
    assert len(products) == 4


def test_create_product():
    pass


def test_create_invalid_product():
    pass


def test_create_incomplete_product():
    pass


def test_get_product():
    pass


def test_get_product_with_invalid_id():
    pass


def test_get_product_with_non_existing_id():
    pass


def test_get_samples():
    pass


def test_get_samples_with_invalid_id():
    pass


def test_get_samples_with_non_existing_id():
    pass


def test_get_tags():
    pass


def test_get_tags_with_invalid_id():
    pass


def test_get_tags_with_non_existing_id():
    pass


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
    pass


def test_delete_product():
    pass


def test_delete_product_with_invalid_id():
    pass


def test_delete_product_with_non_existing_id():
    pass
