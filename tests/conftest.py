"""Main conftest."""

import json
from unittest import mock

import aiohttp
import pytest


@pytest.fixture
def main_reresponse():
    """Fixture the get response from file."""
    with open(r'tests\\real_response.json', 'r', encoding='utf-8') as flr:
        response_json = json.load(flr)
        yield response_json


@pytest.fixture
def mock_requests_get():
    """Mock the 'requests.get' method."""
    with mock.patch('main.requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_aiohttp():
    """Mock the 'aiohttp.ClientResponse' method."""

    mock_response = mock.MagicMock(spec=aiohttp.ClientResponse)
    mock_response.status = 200
    mock_response.text.return_value = 'Mocked file data'

    mock_session = mock.MagicMock(spec=aiohttp.ClientSession)
    mock_session.get.return_value.__aenter__.return_value = mock_response
    yield mock_session
