import pytest

from adsepra import SepClient, DataProductsApiClient


def pytest_configure(config):
    # create the dict to store custom data
    config._data = {}

@pytest.fixture
def client():
    sep_client = SepClient(host='https://starburst.ottensa.dev', user='merlin', token='Basic bWVybGluOg')
    dpc = DataProductsApiClient(client=sep_client)
    return dpc
