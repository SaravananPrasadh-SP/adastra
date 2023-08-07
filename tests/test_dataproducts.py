from unittest import TestCase

from adsepra import DataProductsApiClient, SepClient


class TestDataProductsApiClient(TestCase):
    def test_list_domains(self):
        sep = SepClient(host='http://localhost:9999', user='merlin', token='Basic bWVybGluOg')
        dpc = DataProductsApiClient(client=sep)
        domains = dpc.list_domains()
        assert len(domains) > 0
