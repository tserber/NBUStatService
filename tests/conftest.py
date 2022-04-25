import pytest
import server

pytest_plugins = 'aiohttp.pytest_plugin'


@pytest.fixture
def cli(loop, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(server.create_app()))
