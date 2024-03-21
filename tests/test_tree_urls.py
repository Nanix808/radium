"""Test function 'tree_urls'."""

from unittest.mock import MagicMock

import pytest
from requests.exceptions import Timeout
from requests.exceptions import RequestException
from unittest.mock import AsyncMock

from main import tree_urls


@pytest.mark.parametrize(
    'folder_name, extected_result',
    [
        (
            '',
            [
                {
                    'folder': '',
                    'url': 'https://gitea.radium.group/api/v1/repos/radium/'
                    'project-configuration/contents/LICENSE?ref=master',
                    'name': 'LICENSE',
                },
                {
                    'folder': '',
                    'url': 'https://gitea.radium.group/api/v1/repos/radium/'
                    'project-configuration/contents/README.md?ref=master',
                    'name': 'README.md',
                },
            ],
        ),
        (
            'test',
            [
                {
                    'folder': 'test',
                    'url': 'https://gitea.radium.group/api/v1/repos/radium/'
                    'project-configuration/contents/LICENSE?ref=master',
                    'name': 'LICENSE',
                },
                {
                    'folder': 'test',
                    'url': 'https://gitea.radium.group/api/v1/repos/radium/'
                    'project-configuration/contents/README.md?ref=master',
                    'name': 'README.md',
                },
            ],
        ),
    ],
)
def test_valid_url_and_valid_folder(
    mock_requests_get, main_reresponse, folder_name, extected_result,
):
    """
    Test valid url with real response.

    Args:
        mock_requests_get: Mock the 'requests.get' method.
        main_reresponse: Fixture the get response from file.
        folder_name: Name of the folder.
        extected_result: Expected result.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = main_reresponse
    mock_requests_get.return_value = mock_response
    tree_list = tree_urls('http://valid_url.com', folder_name)
    assert tree_list == extected_result


def test_expected_params():
    """A test function to check the expected parameters of the tree_urls function."""
    with pytest.raises(TypeError):
        tree_urls()


def test_invalid_url(mock_requests_get):
    """
    Function to test the behavior of the tree_urls function with an invalid URL.

    Args:
        mock_requests_get: Mock the 'requests.get' method.
    """
    mock_requests_get.side_effect = Timeout
    with pytest.raises(Timeout):
        tree_urls('invalid_url')
