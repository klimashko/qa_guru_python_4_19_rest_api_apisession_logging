import pytest

from utils.helper import BaseSession


@pytest.fixture(scope="session")
def reqres():
    with BaseSession(base_url="https://reqres.in/api") as session:
        yield session