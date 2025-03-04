TEST_CITY_ID = "2"  # тестовый город - Санкт-Петербург


class Message:
    NON_EXISTENT_CATEGORY = "No Category matches the given query."
    NON_EXISTENT_CARD = "No Card matches the given query."
    NON_EXISTENT_SERVICE_CARD = "No CardService matches the given query."
    NON_EXISTENT_USER = "No CustomUser matches the given query."
    NON_EXISTENT_CITY = "No City matches the given query."
    NON_EXISTENT_NOTIFICATION = "No UserNotification matches the given query."
    PAGE_NOT_FOUND = "Страница не найдена."
    INVALID_ID = "ID is invalid."
    CREDENTIALS_NOT_FOUND = "Учетные данные не были предоставлены"
    INVALID_TOKEN = "Токен не верный. Проверьте ввод или заново авторизуйтесь."
    NOT_SUFFICIENT_RIGHTS = "У вас недостаточно прав для выполнения данного действия."
    EMPTY_USERS_LIST = "Users list is empty"
    EMPTY_FIELD = "Это поле не может быть пустым."
    MUST_BE_BOOLEAN = "Must be a valid boolean."
    TITLE_AND_DSCR_REQUIRED = "Title and description are required"
    REQUIRED_FIELD = "Обязательное поле."
    CARD_NOT_ARCHIVE = "Card is not archive"
    CARD_NOT_ACTIVE = "Card is not active"
    ALREADY_FAVORITE = "Объявление уже добавлено!"
    ALREADY_NOT_FAVORITE = "Advertisement has already been removed!"


class CATEGORY:
    MAIN = {
        "Транспорт": "1",
        "Услуги": "2",
        "Недвижимость": "3",
        "Строительство": "4",
        "Личные вещи": "5",
        "Товары для дома": "6",
        "Всё для сада": "7",
        "Электроника и бытовая техника": "8",
        "Животные": "9",
        "Оборудование и запчасти": "10"
    }
