"""Module gets files from repository on Gitea."""

import asyncio
import hashlib
import os
from pathlib import Path
from typing import TypedDict

import aiohttp
import requests


class FileObject(TypedDict):
    """Represents a file object with specific attributes.

    Attributes:
        folder_name (str): The name of the folder.
        url (str): The URL of the file.
        name (str): The name of the file.
        sha256 (str): The SHA256 hash of the file.
    """

    folder_name: str
    url: str
    name: str
    sha256: str


def tree_urls(url: str, folder_name: str = '') -> list[FileObject]:
    """Retrieve a list of URLs from the specified repository on Gitea.

    Args:
        url (str): The URL of the repository on Gitea.
        folder_name (str): The name of the folder to start from.

    Returns:
        List[str]: A list of URLs.
    """
    response = requests.get(url, timeout=10)
    tree_list: list[str] = []
    response = response.json()
    for file_folder_info in response:
        if file_folder_info['type'] == 'file':
            tree_list.append(
                {
                    'folder': folder_name,
                    'url': file_folder_info['url'],
                    'name': file_folder_info['name'],
                },
            )
        else:
            if folder_name == '':
                new_folder_name = f"{file_folder_info['name']}/"
            else:
                new_folder_name = f"{folder_name}{file_folder_info['name']}/"
            for link in tree_urls(
                url=f"{url}/{file_folder_info['name']}",
                folder_name=new_folder_name,
            ):
                tree_list.append(link)
    return tree_list


async def download_file(
    session: aiohttp.ClientSession, url_list: list[FileObject], repo_dir: str,
) -> None:
    """
    Download files from a list of URLs asynchronously.

    Args:
        session: aiohttp ClientSession object for making HTTP requests.
        url_list: List of dictionaries containing URL information.
        repo_dir: Directory where the files will be saved.
    """
    status_code = 200
    for url_info in url_list:
        url_base = 'https://gitea.radium.group/api/v1/repos/radium/project-configuration/raw/'
        file_path = f"{url_info['folder']}{url_info['name']}"
        async with session.get(url_base + file_path) as response:
            if response.status == status_code:
                file_data = await response.text()
                file_path = os.path.join(
                    repo_dir,
                    url_info['folder'],
                    url_info['name'],
                )
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as file_w:
                    file_w.write(file_data)


def calculate_sha256(file_path: FileObject) -> str:
    """Calculate the SHA-256 checksum of a file.

    Parameters:
        file_path (FileObject): The path to the file.

    Returns:
        str: The SHA-256 checksum of the file.
    """
    hash_ = hashlib.sha256()
    byte_size = 4096
    with open(file_path, 'rb') as fb:
        for chunk in iter(lambda: fb.read(byte_size), b''):
            hash_.update(chunk)
    return hash_.hexdigest()


async def main() -> None:
    """
    Download files from repository.

    Args:
       None
    """
    repository_url: str = (
        'https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents'
    )
    repository_folder: Path = Path('repo')
    repository_folder.mkdir(exist_ok=True)
    url_list: list[FileObject] = tree_urls(repository_url)
    num_async_theads: int = 3

    async with aiohttp.ClientSession() as session:
        tasks: list[asyncio.Task] = [
            download_file(
                session,
                url_list[num::num_async_theads],
                repository_folder,
            )
            for num in range(num_async_theads)
        ]
        await asyncio.gather(*tasks)

    for file_item in url_list:
        file_path: str = os.path.join(
            repository_folder, file_item['folder'], file_item['name'],
        )
        file_hash: str = calculate_sha256(file_path)
        file_item['sha256'] = file_hash


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
