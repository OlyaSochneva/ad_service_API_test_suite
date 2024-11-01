Сервис объявлений автотестирование API
Запросы, тестируемые автоматически:
Список категорий              GET /api/categories/
Получение категории по id     GET /api/categories/{id}/
Получить список объявлений    GET /api/cards/
Создание объявления           POST /api/cards/
Получение объявления по id    GET /api/cards/{id}/
Архивировать объявление       POST /api/cards/{id}/archive/
Восстановить из архива        POST /api/cards/{id}/active/
Добавить в избранное          POST /api/cards/{id}/favorite/
Удалить из избранного         DELETE /api/cards/{id}/favorite/
Получить список объявлений (услуги)  GET /api/cards/services/
Создание объявления (услуги)         POST /api/cards/services/
Получение объявления (услуги) по id  GET /api/cards/services/{id}/
Архивировать (услуги)                POST /api/cards/services/ {id}/archive/
Восстановить из архива (услуги)      POST /api/cards/services/{id}/active/
Добавить в избранное (услуги)        POST /api/cards/services/{id}/favorite/
Удалить из избранного (услуги)       DELETE /api/cards/{id}/favorite/
Получение пользователя по id  GET /api/users/{id}/
Профиль пользователя          GET /api/users/me/
Список городов                GET /api/cities/
Получение города по id        GET /api/cities/
Создание диалога
Получение диалога
Отправка сообщения
Получить список уведомлений   GET /api/notifications/
Создание уведомления          POST /api/notifications/
Получение уведомления по id   GET /api/notifications/{id}/
Прочитать уведомление         PATCH /api/notifications/{id}/





