import os
import pytest
from unittest.mock import MagicMock, patch
import aiohttp
import asyncio
from pathlib import Path
from main import main, tree_urls, download_file, calculate_sha256
from requests.exceptions import Timeout
from requests.exceptions import RequestException
from unittest.mock import AsyncMock


@patch("main.requests.get")
def test_valid_url_and_folder_name(mock_get):
    mock_response = [{"type": "file", "url": "file_url", "name": "file_name"}]
    mock_get.return_value.json.return_value = mock_response
    expected_result = [
        {"folder": "folder_name", "url": "file_url", "name": "file_name"}
    ]
    assert tree_urls("valid_url", "folder_name") == expected_result


@patch("main.requests.get")
def test_invalid_url(mock_get):
    mock_get.side_effect = Timeout
    with pytest.raises(Timeout):
        tree_urls("invalid_url")


@patch("main.requests.get")
def test_empty_folder_name(mock_get):
    mock_response = [{"type": "file", "url": "file_url", "name": "file_name"}]
    mock_get.return_value.json.return_value = mock_response
    expected_result = [{"folder": "", "url": "file_url", "name": "file_name"}]
    assert tree_urls("valid_url") == expected_result


def test_expected_params():
    with pytest.raises(TypeError):
        tree_urls()


@pytest.mark.asyncio
async def test_download_file_success():
    mock_response = AsyncMock()
    mock_response.status = 200

    mock_session = AsyncMock()
    mock_session.get.return_value.__aenter__.return_value = mock_response

    url_info = {"url": "https://example.com", "folder": "folder", "name": "file.txt"}
    url_list = [url_info]
    repo_dir = "repo"

    await download_file(mock_session, url_list, repo_dir)

    file_path = os.path.join(repo_dir, url_info["folder"], url_info["name"])
    assert os.path.exists(file_path)


# @pytest.mark.asyncio
# async def test_download_file_404():
#     mock_response = AsyncMock()
#     mock_response.status = 404

#     mock_session = AsyncMock()
#     mock_session.get.return_value.__aenter__.return_value = mock_response

#     url_info = {'url': 'https://example.com', 'folder': 'folder', 'name': 'file.txt'}
#     url_list = [url_info]
#     repo_dir = '/path/to/repo'

#     await download_file(mock_session, url_list, repo_dir)

#     file_path = os.path.join(repo_dir, url_info['folder'], url_info['name'])
#     assert not os.path.exists(file_path)

# @pytest.mark.asyncio
# async def test_download_file_save_to_correct_directory():
#     mock_response = AsyncMock()
#     mock_response.status = 200

#     mock_session = AsyncMock()
#     mock_session.get.return_value.__aenter__.return_value = mock_response

#     url_info = {'url': 'https://example.com', 'folder': 'folder', 'name': 'file.txt'}
#     url_list = [url_info]
#     repo_dir = '/path/to/repo'

#     await download_file(mock_session, url_list, repo_dir)

#     file_path = os.path.join(repo_dir, url_info['folder'], url_info['name'])
#     assert os.path.exists(file_path)
#     assert os.path.dirname(file_path) == os.path.join(repo_dir, url_info['folder'])
