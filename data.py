class TestData:

    USER_ADMIN = {"email": "admin@localhost"}

    CATEGORY_ID = 7  # тестовая категория - "Всё для сада"

    CITY_ID = 2      # тестовый город - Санкт-Петербург


class URL:
    BASE = "https://api.dev.ads.ktsf.ru"
    CATEGORIES = BASE + "/api/categories/"  # получить все категории, получить по id
    CARDS = BASE + "/api/cards/"            # получить все объявления, получить по id
    SERVICE_CARDS = CARDS + "services/"     # получить все услуги, получить по id
    VEHICLE_CARDS = CARDS + "vehicles/"     # получить все авто, получить по id
    USERS = BASE + "/api/users/"            # получить всех юзеров, получить по id
    USER_ME = USERS + "/me/"
    REGISTRATION = BASE + "/api/registration/"
    SEND_CODE = BASE + "/api/send_code/"
    LOGIN = BASE + "/api/login/"
    #FAVORITES = BASE + "/api/favorites/"
    NOTIFICATIONS = BASE + "/api/notifications/"
    CITIES = BASE + "/api/cities/"         # получить все города, получить по id
    DIALOGS = BASE + "/api/dialogs/dialogs/"
    MESSAGE = BASE + "/api/dialogs/messages/send/"


class Message:
    NON_EXISTENT_CATEGORY = "No Category matches the given query."
    NON_EXISTENT_CARD = "No Card matches the given query."
    NON_EXISTENT_SERVICE_CARD = "No CardService matches the given query."
    NON_EXISTENT_VEHICLE_CARD = "No CardVehicle matches the given query."
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
    ALREADY_NOT_FAVORITE = "Объявление уже удалено!"


class Data:
    CATEGORIES_LIST = [
        "Транспорт",                       # 1
        "Услуги",                          # 1
        "Недвижимость",                    # 1
        "Строительство",                   # 1
        "Личные вещи",                     # 1
        "Товары для дома",                 # 1
        "Всё для сада",                    # 1
        "Электроника и бытовая техника",   # 1
        "Животные",                        # 1
        "Оборудование и запчасти",         # 1
        "Легковые авто",                   # 2 Транспорт
        "Грузовики и автобусы",            # 2 Транспорт
        "Мотоциклы и мототехника",         # 2 Транспорт
        "Водный транспорт",                # 2 Транспорт
        "Спецтехника",                     # 2 Транспорт
        "Запчасти и аксессуары",           # 2 Транспорт
        "Жилая недвижимость",              # 2 Недвижимость
        "Коммерческая недвижимость",       # 2 Недвижимость
        "Ремонт и обслуживание техники",   # 2 Услуги
        "Обучение и курсы",                # 2 Услуги
        "Красота и здоровье",              # 2 Услуги
        "Аренда техники",                  # 2 Услуги
        "Пассажирские перевозки",          # 2 Услуги
        "Мастер на час",                   # 2 Услуги
        "Грузовые перевозки",              # 2 Услуги
        "Бытовые услуги",                  # 2 Услуги
        "Деловые услуги",                  # 2 Услуги
        "Одежда, обувь, аксессуары",  # 2 Личные вещи
        "Часы и украшения",           # 2 Личные вещи
        "Хобби и развлечения",        # 2 Личные вещи
        "Красота и здоровье",         # 2 Личные вещи
        "Спорт и отдых",              # 2 Личные вещи
        "Детские товары",             # 2 Личные вещи
        "Мебель и интерьер",          # 2 Личные вещи
        "Ремонт и строительство",     # 2 Товары для дома
        "Посуда и товары для кухни",  # 2 Товары для дома
        "Растения",                   # 2 Товары для дома
        "Телефоны",                   # 2 Товары для дома
        "Строительство домов под ключ",          # 2 Строительство
        "Строительство гаражей, бань и веранд",  # 2 Строительство
        "Отделка деревянных домов, бань, саун",  # 2 Строительство
        "Кладочные работы",                      # 2 Строительство
        "Кровельные работы",                     # 2 Строительство
        "Сварочные работы",                      # 2 Строительство
        "Бетонные работы",                       # 2 Строительство
        "Фундаментные работы",                   # 2 Строительство
        "Алмазное сверление и резка",            # 2 Строительство
        "Снос и демонтаж",                       # 2 Строительство
        "Фасадные работы",                       # 2 Строительство
        "Проектирование и сметы",                # 2 Строительство
        "Изыскательные работы",                  # 2 Строительство
        "Лестницы",                              # 2 Строительство
        "Газификация",                           # 2 Строительство
        "Другое",                                # 2 Строительство
        "Телевизоры",                         # 3 Услуги - Ремонт и обслуживание техники
        "Кондиционеры и вентиляция",          # 3 Услуги - Ремонт и обслуживание техники
        "Мобильные устройства",               # 3 Услуги - Ремонт и обслуживание техники
        "Фото, аудио и видеотехника",         # 3 Услуги - Ремонт и обслуживание техники
        "Посудомоечные машины",               # 3 Услуги - Ремонт и обслуживание техники
        "Стиральные и сушильные машины",      # 3 Услуги - Ремонт и обслуживание техники
        "Холодильники и морозильные камеры",  # 3 Услуги - Ремонт и обслуживание техники
        "Варочные панели и духовые шкафы",    # 3 Услуги - Ремонт и обслуживание техники
        "Газовые котлы и водонагреватели",    # 3 Услуги - Ремонт и обслуживание техники
        "Кофемашины",                         # 3 Услуги - Ремонт и обслуживание техники
        "Швейные машины и оверлоки",          # 3 Услуги - Ремонт и обслуживание техники
        "Другое",                             # 3 Услуги - Ремонт и обслуживание техники
        "Маникюр и педикюр",    # 3 Услуги - Красота и здоровье
        "Услуги парикмахера",   # 3 Услуги - Красота и здоровье
        "Ресницы и брови",      # 3 Услуги - Красота и здоровье
        "Косметология",         # 3 Услуги - Красота и здоровье
        "Эпиляция",             # 3 Услуги - Красота и здоровье
        "Макияж",               # 3 Услуги - Красота и здоровье
        "СПА-услуги и массаж",  # 3 Услуги - Красота и здоровье
        "Тату и пирсинг",       # 3 Услуги - Красота и здоровье
        "Психология",           # 3 Услуги - Красота и здоровье
        "Диетология",           # 3 Услуги - Красота и здоровье
        "Фитнес и йога",        # 3 Услуги - Красота и здоровье
        "Другое",               # 3 Услуги - Красота и здоровье
        "Предметы школы и вуза",        # 3 Услуги - Обучение и курсы
        "Иностранные языки",            # 3 Услуги - Обучение и курсы
        "Детское развитие и логопеды",  # 3 Услуги - Обучение и курсы
        "IT и бизнес",                  # 3 Услуги - Обучение и курсы
        "Дизайн и рисование",           # 3 Услуги - Обучение и курсы
        "Красота и здоровье",           # 3 Услуги - Обучение и курсы
        "Спорт и танцы",                # 3 Услуги - Обучение и курсы
        "Вождение",                     # 3 Услуги - Обучение и курсы
        "Музыка и театр",               # 3 Услуги - Обучение и курсы
        "Профессиональная подготовка",  # 3 Услуги - Обучение и курсы
        "Другое",                       # 3 Услуги - Обучение и курсы
        "Аренда легкового транспорта и мототранспорта",   # 3 Услуги - Аренда техники
        "Аренда грузового транспорта",                    # 3 Услуги - Аренда техники
        "Трансфер"]    # 3 Услуги - Пассажирские перевозки

    TRANSPORT_SUBCATEGORIES = [
        "Легковые авто"
    ]
    SERVICES_SUBCATEGORIES = [
        "Ремонт и обслуживание техники",
        "Обучение и курсы",
        "Красота и здоровье",
        "Аренда техники",
        "Пассажирские перевозки",
        "Мастер на час",
        "Грузовые перевозки",
        "Бытовые услуги",
        "Деловые услуги"
    ]
    CONSTRUCTION_SUBCATEGORIES = [
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
        "Другое"
    ]
    REPAIR_SERVICE_SUBCATEGORIES = [
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
        "Другое"
    ]
    BEAUTY_HEALTH_SUBCATEGORIES = [
        "Маникюр и педикюр",
        "Услуги парикмахера",
        "Ресницы и брови",
        "Косметология",
        "Эпиляция",
        "Макияж",
        "СПА-услуги и массаж",
        "Тату и пирсинг",
        "Психология",
        "Диетология",
        "Фитнес и йога",
        "Другое"
    ]
    STUDYING_SUBCATEGORIES = [
        "Предметы школы и вуза",
        "Иностранные языки",
        "Детское развитие и логопеды",
        "IT и бизнес",
        "Дизайн и рисование",
        "Красота и здоровье",
        "Спорт и танцы",
        "Вождение",
        "Музыка и театр",
        "Профессиональная подготовка",
        "Другое"
    ]
    TRANSPORT_RENTAL_SUBCATEGORIES = [
        "Аренда легкового транспорта и мототранспорта",
        "Аренда грузового транспорта"
    ]
    TRANSPORTATION_SUBCATEGORIES = [
        "Трансфер"
    ]

