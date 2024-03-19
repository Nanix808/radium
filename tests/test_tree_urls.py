import os
import pytest
from unittest.mock import MagicMock, patch
import aiohttp
import asyncio
from pathlib import Path
from main import main, tree_urls, download_file, calculate_sha256
from requests.exceptions import Timeout


def test_valid_url_and_folder_name():

    with patch("requests.get") as mock_get:
        mock_response = [{"type": "file", "url": "file_url", "name": "file_name"}]
        mock_get.return_value.json.return_value = mock_response
        expected_result = [{"folder": "", "url": "file_url", "name": "file_name"}]
        assert tree_urls("valid_url", "folder_name") == expected_result


# def test_invalid_url():
#     with patch("requests.get") as mock_get:
#         mock_get.side_effect = Timeout
#         with pytest.raises(Timeout):
#             tree_urls("invalid_url")


# def test_empty_folder_name():
#     with patch("requests.get") as mock_get:
#         mock_response = [{"type": "file", "url": "file_url", "name": "file_name"}]
#         mock_get.return_value.json.return_value = mock_response
#         expected_result = [{"folder": "", "url": "file_url", "name": "file_name"}]
#         assert tree_urls("valid_url") == expected_result


# @pytest.mark.asyncio
# async def test_main_repository_folder_creation():
#     with patch("aiohttp.ClientSession") as mock_session:
#         mock_session.return_value = MagicMock()
#         with patch("pathlib.Path.mkdir") as mock_mkdir:
#             await main()
#             mock_mkdir.assert_called_once_with(exist_ok=True)


# @pytest.mark.asyncio
# async def test_main_tree_urls_retrieval():
#     with patch("aiohttp.ClientSession") as mock_session:
#         mock_session.return_value = MagicMock()
#         with patch("pathlib.Path.mkdir"):
#             with patch("main_module.tree_urls") as mock_tree_urls:
#                 await main()
#                 mock_tree_urls.assert_called_once_with(
#                     "https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents"
#                 )


# @pytest.mark.asyncio
# async def test_main_file_downloading():
#     url_list = [{"url": "url1"}, {"url": "url2"}, {"url": "url3"}]
#     with patch("aiohttp.ClientSession") as mock_session:
#         mock_session.return_value = MagicMock()
#         with patch("pathlib.Path.mkdir"):
#             with patch("main_module.tree_urls") as mock_tree_urls:
#                 mock_tree_urls.return_value = url_list
#                 with patch("main_module.download_file") as mock_download_file:
#                     await main()
#                     mock_download_file.assert_has_calls(
#                         [
#                             unittest.mock.call(mock_session, "url1", Path("repo")),
#                             unittest.mock.call(mock_session, "url2", Path("repo")),
#                             unittest.mock.call(mock_session, "url3", Path("repo")),
#                         ]
#                     )


# @pytest.mark.asyncio
# async def test_main_sha256_calculation():
#     url_list = [
#         {"folder": "folder1", "name": "file1"},
#         {"folder": "folder2", "name": "file2"},
#     ]
#     with patch("aiohttp.ClientSession") as mock_session:
#         mock_session.return_value = MagicMock()
#         with patch("pathlib.Path.mkdir"):
#             with patch("main_module.tree_urls") as mock_tree_urls:
#                 mock_tree_urls.return_value = url_list
#                 with patch("main_module.download_file"):
#                     with patch("main_module.calculate_sha256") as mock_calculate_sha256:
#                         await main()
#                         mock_calculate_sha256.assert_has_calls(
#                             [
#                                 unittest.mock.call(
#                                     os.path.join(Path("repo"), "folder1", "file1")
#                                 ),
#                                 unittest.mock.call(
#                                     os.path.join(Path("repo"), "folder2", "file2")
#                                 ),
#                             ]
#                         )
