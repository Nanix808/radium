"""Test function 'download_file'."""

import os

import pytest

from main import download_file


@pytest.mark.asyncio
async def test_download_file(mock_aiohttp):
    """
    Asynchronous test for downloading a file to simulate an HTTP response and session.

    Args:
        mock_aiohttp: aiohttp ClientSession object for making HTTP requests.
    """
    url = 'http://example.com/file1'
    file_name = 'test.txt'
    folder = 'test_folder'
    file_path = os.path.join(folder, file_name)

    await download_file(
        mock_aiohttp, [{'url': url, 'folder': folder, 'name': file_name}], '',
    )

    with open(file_path, 'r', encoding='utf-8') as test_file:
        read_line = test_file.read()
    assert read_line == 'Mocked file data', f'File {file_path} does not contain "Mocked file data"'
    assert os.path.exists(file_path), f'File {file_path} does not exist'


@pytest.mark.asyncio
async def test_download_files(mock_aiohttp):
    """Asynchronous test for downloading a file to simulate an HTTP response and session.

    Args:
        mock_aiohttp: aiohttp ClientSession object for making HTTP requests.
    """
    url_list = [
        {'url': 'http://example.com/file1', 'folder': 'folder1', 'name': 'file1.txt'},
        {'url': 'http://example.com/file2', 'folder': 'folder2', 'name': 'file2.txt'},
    ]

    await download_file(mock_aiohttp, url_list, '')

    for file_info in url_list:
        file_path = os.path.join(file_info['folder'], file_info['name'])
        with open(file_path, 'r', encoding='utf-8') as test_file:
            read_line = test_file.read()
        assert read_line == 'Mocked file data', f'{file_path} does not contain "Mocked file data"'
        assert os.path.exists(file_path), f'File {file_path} does not exist'


@pytest.mark.asyncio
async def test_expected_params():
    """A test function to check the expected parameters of the download_file function."""
    with pytest.raises(TypeError):
        await download_file()
