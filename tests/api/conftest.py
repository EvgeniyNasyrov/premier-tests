import pytest

# JSONPlaceholder — бесплатный API без ключа (reqres.in теперь требует x-api-key)
DOMAIN_URL = "https://jsonplaceholder.typicode.com"
USERS_API = "/users"
POSTS_API = "/posts"


@pytest.fixture()
def base_endpoint():
    users_url = DOMAIN_URL + USERS_API
    return users_url


@pytest.fixture()
def search_endpoint():
    return DOMAIN_URL + POSTS_API
