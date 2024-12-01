import allure
import pytest
import requests

from assistant_methods import return_is_favorite, generate_random_string
from data import URL, Message


class TestAddToFavoritesServices:
    @allure.title('Можно добавить карточку услуг в избранное')
    def test_add_service_card_to_favorites_success(self, user_token, active_service):
        response = requests.post(URL.SERVICE_CARDS + active_service["id"] + "/favorite/",
                                 headers={"Authorization": f"Bearer {user_token}"})
        is_favorite = return_is_favorite(response.json())
        assert (response.status_code == 200 and is_favorite is True)

    @allure.title('(400)Нельзя добавить карточку услуг в избранное, если она уже там')
    def test_add_service_card_to_favorites_again_causes_error(self, user_token, active_service):
        requests.post(URL.SERVICE_CARDS + active_service["id"] + "/favorite/",
                      headers={"Authorization": f"Bearer {user_token}"})
        response = requests.post(URL.SERVICE_CARDS + active_service["id"] + "/favorite/",
                                 headers={"Authorization": f"Bearer {user_token}"})
        assert (response.status_code == 400 and Message.ALREADY_FAVORITE in str(response.json()))

    @allure.title('Нельзя добавить в избранное архивную карточку услуги')
    def test_add_archive_service_card_to_favorites_causes_error(self, user_token, archive_service):
        response = requests.post(URL.SERVICE_CARDS + archive_service["id"] + "/favorite/",
                                 headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 400

    @allure.title('Нельзя добавить в избранное карточку услуги на модерации')
    def test_add_moderate_service_card_to_favorites_causes_error(self, user_token, new_service):
        response = requests.post(URL.SERVICE_CARDS + new_service["id"] + "/favorite/",
                                 headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 400

    @allure.title('(401)Нельзя добавить карточку услуги в избранное с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_add_service_card_to_favorites_unauthorized_causes_error(self, wrong_headers,
                                                                     error_message, active_service):
        response = requests.post(URL.SERVICE_CARDS + active_service["id"] + "/favorite/", headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(404/400)Нельзя добавить в избранное карточку услуг с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_add_service_card_to_favorites_by_incorrect_id_causes_error(self, user_token, wrong_id,
                                                                        status_code, error_message):
        response = requests.post(URL.SERVICE_CARDS + wrong_id + "/favorite/",
                                 headers={"Authorization": f"Bearer {user_token}"})
        assert (response.status_code == status_code and error_message in str(response.json()))


class TestRemoveFromFavoritesServices:
    @allure.title('Можно удалить карточку услуги из избранного')
    def test_remove_service_card_from_favorites_success(self, user_token, active_service):
        requests.post(URL.SERVICE_CARDS + active_service["id"] + "/favorite/",
                      headers={"Authorization": f"Bearer {user_token}"})
        response = requests.delete(URL.SERVICE_CARDS + active_service["id"] + "/favorite/",
                                   headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 204

    @allure.title('Можно удалить из избранного архивную карточку услуги')
    def test_remove_archive_service_card_from_favorites_success(self, user_token, active_service):
        requests.post(URL.SERVICE_CARDS + active_service["id"] + "/favorite/",
                      headers={"Authorization": f"Bearer {user_token}"})
        requests.post(URL.SERVICE_CARDS + active_service["id"] + "/archive/",
                      headers={'Authorization': f'Bearer {active_service["token"]}'})
        response = requests.delete(URL.SERVICE_CARDS + active_service["id"] + "/favorite/",
                                   headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 204

    @allure.title('Можно удалить из избранного карточку услуги на модерации')
    def test_remove_moderate_service_card_from_favorites_success(self, user_token, active_service, admin_token):
        requests.post(URL.SERVICE_CARDS + active_service["id"] + "/favorite/",
                      headers={"Authorization": f"Bearer {user_token}"})
        requests.post(URL.CARDS + active_service["id"] + "/change_status/",
                      headers={'Authorization': f'Bearer {admin_token}'})
        response = requests.delete(URL.SERVICE_CARDS + active_service["id"] + "/favorite/",
                                   headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 204

    @allure.title('(400)Нельзя удалить из избранного, если карточка услуг не в избранном')
    def test_remove_service_card_from_favorites_again_causes_error(self, user_token, active_service):
        response = requests.delete(URL.SERVICE_CARDS + active_service["id"] + "/favorite/",
                                   headers={"Authorization": f"Bearer {user_token}"})
        assert (response.status_code == 400 and Message.ALREADY_NOT_FAVORITE in str(response.json()))

    @allure.title('(401)Нельзя удалить из избранного с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_remove_service_card_from_favorites_unauthorized_causes_error(self, wrong_headers,
                                                                          error_message, active_service):
        response = requests.delete(URL.SERVICE_CARDS + active_service["id"] + "/favorite/", headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(404/400)Нельзя удалить из избранного карточку услуги с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_remove_service_card_from_favorites_by_incorrect_id_causes_error(self, user_token, wrong_id,
                                                                             status_code, error_message):
        response = requests.delete(URL.SERVICE_CARDS + wrong_id + "/favorite/",
                                   headers={"Authorization": f"Bearer {user_token}"})
        assert (response.status_code == status_code and error_message in str(response.json()))
