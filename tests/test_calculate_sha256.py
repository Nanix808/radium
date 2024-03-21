"""Test function 'calculate_sha256'."""

import hashlib

import pytest

from main import calculate_sha256


def test_small_file_sha256_checksum():
    """Calculate the SHA256 checksum of a small file for testing."""
    file_path = 'tests/test_small_file.txt'
    with open(file_path, 'w', encoding='utf-8') as file_test:
        file_test.write('This is a small file for testing')
    expected_checksum = hashlib.sha256(
        'This is a small file for testing'.encode(),
    ).hexdigest()
    assert calculate_sha256(file_path) == expected_checksum


def test_non_existent_file():
    """A test to check if the function raises a FileNotFoundError when given a non-existent file."""
    with pytest.raises(FileNotFoundError):
        calculate_sha256('non_existent_file.txt')


# def test_consistent_checksum():
#     fake_file = MagicMock()
#     fake_file.read.return_value = b"hello"
#     checksum1 = calculate_sha256(fake_file)
#     checksum2 = calculate_sha256(fake_file)
#     assert checksum1 == checksum2
