import allure
import pytest
import requests

from assistant_methods import return_is_favorite, generate_random_string
from data import URL, Message

ACTIVE_CARD = ""
ARCHIVE_CARD = ""
MODERATE_CARD = ""


class TestFavorites:
    @allure.title('Можно добавить карточку в избранное')
    @pytest.mark.order(1)
    def test_make_card_favorite_success(self, user_token):
        response = requests.post(URL.CARDS + ACTIVE_CARD + "/favorite/",
                                 headers={"Authorization": f"Bearer {user_token}"})
        print(response.json())
        is_favorite = return_is_favorite(response.json())
        assert (response.status_code == 200 and is_favorite is True)

    @allure.title('(400)Нельзя добавить карточку в избранное, если она уже там')
    @pytest.mark.order(2)
    def test_make_card_favorite_twice_causes_error(self, user_token):
        response = requests.post(URL.CARDS + ACTIVE_CARD + "/favorite/",
                                 headers={"Authorization": f"Bearer {user_token}"})
        assert (response.status_code == 400 and Message.ALREADY_FAVORITE in str(response.json()))

    @allure.title('Нельзя добавить в избранное карточку в архиве или на модерации')
    @pytest.mark.order(3)
    @pytest.mark.parametrize("card", [ARCHIVE_CARD, MODERATE_CARD])
    def test_make_archive_card_favorite_causes_error(self, card, user_token):
        response = requests.post(URL.CARDS + card + "/favorite/", headers={"Authorization": f"Bearer {user_token}"})
        # print(response.json())
        assert response.status_code == 400

    @allure.title('(401)Нельзя добавить в избранное с отсут./невалидным токеном')
    @pytest.mark.order(4)
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_make_card_favorite_unauthorized_causes_error(self, wrong_headers, error_message):
        response = requests.post(URL.CARDS + ACTIVE_CARD + "/favorite/", headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(404/400)Нельзя добавить в избранное карточку с несуществующим/невалидным id')
    @pytest.mark.order(5)
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_make_card_favorite_by_incorrect_id_causes_error(self, user_token, wrong_id,
                                                             status_code, error_message):
        response = requests.post(URL.CARDS + wrong_id + "/favorite/", headers={"Authorization": f"Bearer {user_token}"})
        assert (response.status_code == status_code and error_message in str(response.json()))

    @allure.title('Можно удалить карточку из избранного')
    @pytest.mark.order(6)
    def test_remove_card_from_favorites_success(self, user_token):
        response = requests.delete(URL.CARDS + ACTIVE_CARD + "/favorite/",
                                   headers={"Authorization": f"Bearer {user_token}"})
        card = requests.get(URL.CARDS + ACTIVE_CARD + "/")
        is_favorite = return_is_favorite(card.json())
        print(response.json())
        assert (response.status_code == 204 and is_favorite is False)

    @allure.title('(400)Нельзя удалить из избранного, если карточка не в избранном')
    @pytest.mark.order(7)
    def test_remove_card_from_favorites_twice(self, user_token):
        response = requests.delete(URL.CARDS + ACTIVE_CARD + "/favorite/",
                                   headers={"Authorization": f"Bearer {user_token}"})
        assert (response.status_code == 400 and Message.ALREADY_NOT_FAVORITE in str(response.json()))

    @allure.title('(404/400)Нельзя удалить из избранного карточку с несуществующим/невалидным id')
    @pytest.mark.order(8)
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_remove_card_from_favorites_by_incorrect_id_causes_error(self, user_token, wrong_id,
                                                                     status_code, error_message):
        response = requests.delete(URL.CARDS + wrong_id + "/favorite/",
                                   headers={"Authorization": f"Bearer {user_token}"})
        assert (response.status_code == status_code and error_message in str(response.json()))
