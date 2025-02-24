import allure
import requests

from admin_data import URL


class TestGetMessages:
    @allure.title('Можно получить сообщения')
    def test_get_dialogs_success(self, dialog):
        response = requests.get(URL.DIALOGS,
                                headers={"Authorization": f"Bearer {dialog["buyer"]}"})
        assert response.status_code == 200
