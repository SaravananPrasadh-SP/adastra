import pytest
from pydantic import ValidationError
from requests import HTTPError

from adsepra.dataproducts import Domain


@pytest.mark.vcr
def test_list_domains(client):
    domains = client.list_domains()
    assert len(domains) == 4


@pytest.mark.vcr
def test_create_domain(request, client):
    domain = client.create_domain(Domain(name='Test Domain'))
    assert domain.id is not None
    assert domain.name == 'Test Domain'
    assert domain.description is None
    assert domain.schemaLocation is None
    request.config._data['domain'] = domain


@pytest.mark.vcr
@pytest.mark.parametrize('name', [
    None,
    '',
    'Test Domain'  # Duplicate
])
def test_create_invalid_domain(client, name):
    with pytest.raises(HTTPError):
        client.create_domain(Domain.model_construct(name=name))


@pytest.mark.vcr
def test_get_domain(request, client):
    domain_id = request.config._data['domain'].id
    domain = client.get_domain(domain_id)
    assert domain.id == domain_id
    assert domain.name == 'Test Domain'
    assert domain.description is None
    assert domain.schemaLocation is None
    request.config._data['domain'] = domain


@pytest.mark.vcr
@pytest.mark.parametrize('uuid', [
    None,
    '',
    'abc'
])
def test_get_invalid_domain(client, uuid):
    with pytest.raises(ValidationError):
        client.get_domain(uuid)


@pytest.mark.vcr
def test_update_domain(request, client):
    domain = request.config._data['domain']
    domain_id = domain.id
    domain.description = 'Lorem Ipsum'
    domain = client.update_domain(domain)
    assert domain.id == domain_id
    assert domain.name == 'Test Domain'
    assert domain.description == 'Lorem Ipsum'
    assert domain.schemaLocation is None
    request.config._data['domain'] = domain


@pytest.mark.vcr
def test_delete_valid_domain(request, client):
    domain = request.config._data['domain']
    assert domain in client.list_domains()

    client.delete_domain(domain.id)
    assert domain not in client.list_domains()


@pytest.mark.vcr
@pytest.mark.parametrize('uuid', [
    None,
    '',
    'abc'
])
def test_delete_invalid_domain(client, uuid):
    """The HTTP Response should be 404 / 405 and the wrapper shall return None"""
    assert not client.delete_domain(uuid)
