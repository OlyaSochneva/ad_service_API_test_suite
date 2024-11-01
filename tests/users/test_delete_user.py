import allure
import pytest
import requests

from data import URL, Message
from response_samples import Sample

class TestDeleteUser:
    def test_delete_user_success(self):
        response = requests.delete(URL.USER_ME)