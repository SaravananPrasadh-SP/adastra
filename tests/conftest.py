import os

import pytest

from adastra.client import SepClient


def pytest_configure(config):
    # create the dict to store custom data
    config._data = {}


@pytest.fixture
def sep_client():
    host = os.environ['sep_host']
    user = os.environ['sep_user']
    token = os.environ['sep_token']
    sep_client = SepClient(host=host, user=user, token=token)
    return sep_client


@pytest.fixture
def sep_data_product_service(sep_client):
    return sep_client.data_product_service()


@pytest.fixture
def sep_domain_service(sep_client):
    return sep_client.domain_service()

