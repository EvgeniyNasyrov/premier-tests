import pytest

# JSONPlaceholder — бесплатный API без ключа (reqres.in теперь требует x-api-key)
DOMAIN_URL = "https://jsonplaceholder.typicode.com"
USERS_API = "/users"


@pytest.fixture()
def base_endpoint():
    users_url = DOMAIN_URL + USERS_API
    return users_url
