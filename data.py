class TestData:
    CARD_ID = 6
    SERVICE_CARD_ID = 24
    VEHICLE_CARD_ID = 13
    CATEGORY_ID = 7   # "Всё для сада"
    USER = {
        "id": 1,
        "email": "admin@localhost",
        "first_name": "admin",
        "last_name": None,
        "phone_number": "admin@localhost",
        "avatar": None,
        "date_joined": "2024-08-20 16:07:08",
        "count_cards": 240
    }
    CITY = {
        "id": 2,
        "name": "Санкт-Петербург",
        "country": "Россия",
        "region": "Санкт-Петербург"
    }


class Data:
    CATEGORIES_LIST = [
        # "Всякое",
        "Транспорт",
        "Услуги",
        "Недвижимость",
        "Строительство",
        "Личные вещи",
        "Товары для дома",
        "Всё для сада",
        "Бытовая техника и электроника",
        "Животные",
        "Оборудование и запчасти",
        "Легковые авто",
        "Ремонт и обслуживание техники"
        "Обучение и курсы",
        "Красота и здоровье",
        "Аренда техники",
        "Пассажирские перевозки",
        "Мастер на час",
        "Грузовые перевозки",
        "Бытовые услуги",
        "Деловые услуги",
        "Строительство домов под ключ",
        "Строительство гаражей, бань и веранд",
        "Отделка деревянных домов, бань, саун",
        "Кладочные работы",
        "Кровельные работы",
        "Сварочные работы",
        "Бетонные работы",
        "Фундаментные работы",
        "Алмазное сверление и резка",
        "Снос и демонтаж",
        "Фасадные работы",
        "Проектирование и сметы",
        "Изыскательные работы",
        "Лестницы",
        "Газификация",
        "Другое",
        "Телевизоры",
        "Кондиционеры и вентиляция",
        "Мобильные устройства",
        "Фото, аудио и видеотехника",
        "Посудомоечные машины",
        "Стиральные и сушильные машины",
        "Холодильники и морозильные камеры",
        "Варочные панели и духовые шкафы",
        "Газовые котлы и водонагреватели",
        "Кофемашины",
        "Швейные машины и оверлоки",
        "Мототехника"]

    SUBCATEGORIES_TRANSPORT = [
        # "Что-то ещё",
        "Авто",
        "Мототехника"
    ]
    SUBCATEGORIES_SERVICES = [
        "Аренда техники",
        "Красота и здоровье",
        "Обучение и курсы",
        # "Что-то ещё",
        "Пассажирские перевозки",
        "Ремонт и обслуживание техники"
    ]
    SUBCATEGORIES_CONSTRUCTION = [
        "Алмазное сверление и резка",
        "Бетонные работы",
        "Газификация",
        "Другое",
        "Изыскательные работы",
        "Кладочные работы",
        "Кровельные работы",
        "Лестницы",
        "Отделка деревянных домов, бань, саун",
        "Проектирование и сметы",
        "Сварочные работы",
        "Снос и демонтаж",
        "Строительство гаражей, бань и веранд",
        "Строительство домов под ключ",
        "Фасадные работы",
        "Фундаментные работы",
    ]


class URL:
    BASE = "http://api.dev.ads.ktsf.ru/"  # бэк 2
    CATEGORIES = BASE + "/api/categories/"  # получить все категории, получить по id
    CARDS = BASE + "/api/cards/"  # получить все объявления, получить по id
    SERVICES = CARDS + "services/"  # получить все услуги, получить по id
    VEHICLES = CARDS + "vehicles/"  # получить все авто, получить по id
    USERS = BASE + "/api/users/"  # получить всех юзеров, получить по id
    FAVORITES = BASE + "/api/favorites/"
    NOTIFICATIONS = BASE + "/api/notifications/"
    CITIES = BASE + "/api/cities/"  # получить все города, получить по id


class Message:
    NON_EXISTENT_CATEGORY = "No Category matches the given query."
    NON_EXISTENT_CARD = "No Card matches the given query."
    NON_EXISTENT_SERVICE_CARD = "No CardService matches the given query."
    NON_EXISTENT_VEHICLE_CARD = "No CardVehicle matches the given query."
    NON_EXISTENT_USER = "No CustomUser matches the given query."
    NON_EXISTENT_CITY = "No City matches the given query."
    PAGE_NOT_FOUND = "Страница не найдена."
