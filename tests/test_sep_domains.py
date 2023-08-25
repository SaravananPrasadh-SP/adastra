import pytest
from pydantic import ValidationError
from requests import HTTPError

from adastra.sep.models import Domain


@pytest.mark.vcr
def test_list_domains(sep_domain_service):
    domains = sep_domain_service.list()
    assert len(domains) == 4


@pytest.mark.vcr
def test_create_domain(request, sep_domain_service):
    domain = sep_domain_service.create(Domain(name='Test Domain'))
    assert domain.id is not None
    assert domain.name == 'Test Domain'
    assert domain.description is None
    assert domain.schemaLocation is None
    request.config._data['domain'] = domain


@pytest.mark.vcr
@pytest.mark.parametrize('name', [
    None,
    ''
])
def test_create_invalid_domain(sep_domain_service, name):
    with pytest.raises(HTTPError):
        sep_domain_service.create(Domain.model_construct(name=name))


@pytest.mark.vcr
def test_create_duplicate_domain(sep_domain_service):
    with pytest.raises(HTTPError):
        sep_domain_service.create(Domain.model_construct(name='Test Domain'))


@pytest.mark.vcr
def test_get_domain(request, sep_domain_service):
    domain_id = request.config._data['domain'].id
    domain = sep_domain_service.get(domain_id)
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
def test_get_domain_with_invalid_id(sep_domain_service, uuid):
    with pytest.raises(ValidationError):
        sep_domain_service.get(uuid)


@pytest.mark.vcr
def test_get_domain_with_non_existing_id(sep_domain_service):
    domain = sep_domain_service.get('11111111-1111-1111-1111-111111111111')
    assert domain is None


@pytest.mark.vcr
def test_update_domain(request, sep_domain_service):
    domain = request.config._data['domain']
    domain_id = domain.id
    domain.description = 'Lorem Ipsum'
    domain = sep_domain_service.update(domain)
    assert domain.id == domain_id
    assert domain.name == 'Test Domain'
    assert domain.description == 'Lorem Ipsum'
    assert domain.schemaLocation is None
    request.config._data['domain'] = domain


@pytest.mark.vcr
@pytest.mark.parametrize('uuid', [
    None,
    '',
    'abc'
])
def test_update_domain_with_invalid_id(request, sep_domain_service, uuid):
    domain = request.config._data['domain'].model_copy(update={'id': uuid})
    with pytest.raises(ValidationError):
        sep_domain_service.update(domain)


@pytest.mark.vcr
def test_update_domain_with_non_existing_id(request, sep_domain_service):
    domain = request.config._data['domain'].model_copy(update={'id': '11111111-1111-1111-1111-111111111111'})
    assert not sep_domain_service.update(domain)


@pytest.mark.vcr
def test_update_domain_name(request, sep_domain_service):
    """Changed name should be ignored"""
    domain = request.config._data['domain'].model_copy(update={'name': 'Name Changed'})
    domain = sep_domain_service.update(domain)
    assert domain.name == 'Test Domain'


@pytest.mark.vcr
def test_delete_domain(request, sep_domain_service):
    domain = request.config._data['domain']
    assert domain in sep_domain_service.list()

    sep_domain_service.delete(domain.id)
    assert domain not in sep_domain_service.list()


@pytest.mark.vcr
@pytest.mark.parametrize('uuid', [
    None,
    '',
    'abc'
])
def test_delete_domain_with_invalid_id(sep_domain_service, uuid):
    with pytest.raises(ValidationError):
        sep_domain_service.delete(uuid)


@pytest.mark.vcr
def test_delete_with_non_existing_id(sep_domain_service):
    assert not sep_domain_service.delete('11111111-1111-1111-1111-111111111111')
