import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message
from response_samples import Sample
from check_response import check_list_structure, check_structure


class TestGetDialogs:

    @allure.title('С корректным токеном можно получить список диалогов')
    def test_get_dialogs_success(self, dialog):
        response = requests.get(URL.DIALOGS,
                                headers={"Authorization": f"Bearer {dialog["buyer"]}"})
        response_structure = check_list_structure(response.json(), check_structure, Sample.DIALOG_STRUCTURE)
        assert (response.status_code == 200 and response_structure == "Correct")

    @allure.title('(401)Нельзя получить список диалогов с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_get_dialogs_unauthorized_causes_error(self, wrong_headers, error_message):
        response = requests.get(URL.DIALOGS, headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))


