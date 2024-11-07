### Ad Service API tests

Документация: https://disk.yandex.ru/edit/disk/disk%2F%D0%A1%D0%B5%D1%80%D0%B2%D0%B8%D1%81%20%D0%BE%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9%2FAPI%202%20%D0%B0%D0%B2%D1%82%D0%BE%D1%82%D0%B5%D1%81%D1%82%D1%8B.xlsx?sk=y6a9ec7c51243ee954f2bdd65db8168b4

**tests** - папка с тестами

**assistant_methods.py** - вспомогательные методы (генераторы и тд)

**check_response.py** - парсинг ответов

**conftest.py** - фикстуры 

**data.py** - внешние данные

**payloads.py** - методы, возвр. тело запроса

**requirements.txt** - внешние зависимости

**response_samples.py** - образцы ответов

#### Тестируемые запросы:
Список категорий: GET /api/categories/ 

Получение категории по id: GET /api/categories/{id}/ 

Получить список объявлений: GET /api/cards/ 

Создание объявления: POST /api/cards/ 

Получение объявления: по id GET /api/cards/{id}/ 

Архивировать объявление: POST /api/cards/{id}/archive/ 

Восстановить из архива: POST /api/cards/{id}/active/ 

Добавить в избранное: POST /api/cards/{id}/favorite/ 

Удалить из избранного: DELETE /api/cards/{id}/favorite/ 

Получить список объявлений (услуги): GET /api/cards/services/ 

Создание объявления (услуги): POST /api/cards/services/ 

Получение объявления (услуги) по id: GET /api/cards/services/{id}/ 

Архивировать (услуги): POST /api/cards/services/ {id}/archive/ 

Восстановить из архива (услуги): POST /api/cards/services/{id}/active/ 

Добавить в избранное (услуги): POST /api/cards/services/{id}/favorite/ 

Удалить из избранного (услуги): DELETE /api/cards/{id}/favorite/ 

Получение пользователя по id: GET /api/users/{id}/ 

Профиль пользователя: GET /api/users/me/ 

Список городов: GET /api/cities/ 

Получение города по id: GET /api/cities/ 

Создание диалога: POST /api/dialogs/dialogs/create/ 

Получение диалога: GET /api/dialogs/dialogs/{id}/

Отправка сообщения: POST /api/dialogs/messages/send/

Получить список уведомлений: GET /api/notifications/ 

Создание уведомления: POST /api/notifications/ 

Получение уведомления по id: GET /api/notifications/{id}/ 

Прочитать уведомление: PATCH /api/notifications/{id}/

