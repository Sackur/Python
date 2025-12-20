import pytest
import main

def test_auto_add_user():

    result = main.add_user("test_bot", "pass123", "Robot")
    assert result is True

def test_hashing():
    assert main.hash_password("123") == main.hash_password("123")