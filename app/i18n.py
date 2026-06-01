"""Internacjonalizacja (i18n): obsługiwane języki, etykiety, słowniki tłumaczeń
oraz pomocnicze funkcje do budowania URL-i z prefiksem języka.

Strategia URL: każdy język ma własny prefiks (/uk/..., /ru/...).
Język domyślny: ukraiński. Korzeń "/" przekierowuje na "/uk/".
"""

LANGUAGES: tuple[str, ...] = ("uk", "ru")
DEFAULT_LANG: str = "uk"

# Etykiety w przełączniku języków
LANG_LABELS: dict[str, str] = {
    "uk": "УКР",
    "ru": "РУС",
}

# Kody regionalne dla hreflang (oba języki targetują Ukrainę)
HREFLANG: dict[str, str] = {
    "uk": "uk-UA",
    "ru": "ru-UA",
}

# Wartości og:locale (Open Graph)
OG_LOCALE: dict[str, str] = {
    "uk": "uk_UA",
    "ru": "ru_UA",
}

# Tłumaczenia interfejsu (UI). Treść (kasyna, artykuły) będzie w bazie danych — krok 2.
TRANSLATIONS: dict[str, dict[str, str]] = {
    "uk": {
        "lang_name": "Українська",
        "breadcrumb_home": "Головна",
        "nav_casinos": "Казино",
        "nav_bonuses": "Бонуси",
        "nav_payments": "Методи оплати",
        "nav_bookmakers": "Букмекери",
        "nav_blog": "Блог",
        "nav_about": "Про нас",
        "footer_tagline": "Незалежні огляди та рейтинги онлайн-казино.",
        "footer_responsible": "Відповідальна гра (18+)",
        "footer_privacy": "Політика конфіденційності",
        "footer_about": "Про нас",
        "footer_18plus": "Азартні ігри пов’язані з ризиком. Грайте відповідально.",
        "footer_affiliate": (
            "Сайт містить афілейт-посилання. Ми можемо отримувати комісію за "
            "реєстрації, здійснені за ними — це не впливає на оцінку казино."
        ),
        "footer_rights": "Усі права захищено.",
        "home_title": "Огляди та рейтинги онлайн-казино",
        "home_description": (
            "Найкращі онлайн-казино в одному місці: оцінки, бонуси без депозиту, "
            "фріспіни та чесні огляди."
        ),
        "home_h1": "Рейтинг онлайн-казино",
        "home_intro": (
            "Обирайте перевірені онлайн-казино з найкращими бонусами та чесними "
            "оцінками. Рейтинг оновлюється регулярно."
        ),
        "card_bonus": "Бонус",
        "card_license": "Ліцензія",
        "card_review": "Детальніше",
        "card_play": "Грати",
        "card_18plus": "18+ Грайте відповідально",
        "card_no_casinos": "Поки що немає казино.",
        "detail_back": "← Назад до рейтингу",
        "detail_about": "Про казино",
        "detail_bonuses": "Бонуси",
        "detail_terms": "Умови",
        "detail_rating": "Рейтинг",
        "detail_license_number": "Номер ліцензії",
        "detail_payment": "Методи оплати",
        "detail_review": "огляд",
        "detail_pros": "Переваги",
        "detail_cons": "Недоліки",
        "detail_ratings": "Оцінки за критеріями",
        "detail_games": "Ігри",
        "detail_payouts": "Виплати",
        "detail_support": "Підтримка",
        "detail_security": "Ліцензія та безпека",
        "detail_verdict": "Підсумок",
        "detail_faq": "Часті запитання",
        "detail_compare": "Порівняння з популярними казино України",
        "detail_established": "Рік заснування",
        "detail_min_deposit": "Мін. депозит",
        "detail_withdrawal": "Час виплат",
        "detail_overall": "Загальна оцінка",
        "detail_verified_editor": "Перевірено редактором",
        "detail_verified_license": "Ліцензія КРАІЛ підтверджена",
        "detail_verified_deposit": "Тестовий депозит здійснено",
        "detail_methodology": "Як ми оцінюємо казино",
        "detail_methodology_intro": "Кожне казино проходить перевірку за 4 критеріями з рівною вагою (по 25%). Підсумкова оцінка — середнє з усіх балів.",
        "detail_method_bonuses": "Бонуси (25%) — розмір, вейджер, прозорість умов, відсутність прихованих обмежень.",
        "detail_method_games": "Ігри (25%) — кількість провайдерів, наявність live-казино, демо-режим.",
        "detail_method_payments": "Виплати (25%) — швидкість, методи (зокрема гривня), ліміти та комісії.",
        "detail_method_support": "Підтримка (25%) — україномовний чат, час відповіді, канали зв’язку.",
        "detail_similar": "Схожі казино",
        "badge_top": "ТОП-вибір",
        "badge_editor": "Вибір редакції",
        "badge_fast": "Швидкі виплати",
        "badge_exclusive": "Ексклюзив",
        "badge_new": "Новинка",
        "badge_popular": "Популярне",
        "badge_bonus": "Великий бонус",
        "badge_mobile": "Мобільне",
        "bonus_no_deposit": "Без депозиту",
        "bonus_registration": "За реєстрацію",
        "bonus_first_deposit": "За перший депозит",
        "bonus_free_spins": "Фріспіни",
        "bonus_birthday": "На день народження",
        "bonus_match": "Матч-бонус",
        "bonus_all": "Усі бонуси",
        "casino_all": "Усі казино",
        "bookmaker_all": "Всі огляди букмекерів",
        "bookmaker_all_h1": "Огляди букмекерів",
        "bookmaker_all_intro": "Рейтинг легальних букмекерів України: ліцензія КРАІЛ, прозорі виплати, широка лінія спортивних подій.",
        "bookmaker_bet": "Зробити ставку",
        "bookmaker_none": "Поки що немає букмекерів.",
        "bookmaker_compare_h2": "Порівняння букмекерів",
        "bookmaker_compare_intro": "Швидке порівняння ключових параметрів. Сортуйте за ліцензією, бонусом або мінімальним депозитом.",
        "bookmaker_col_rank": "#",
        "bookmaker_col_name": "Букмекер",
        "bookmaker_col_rating": "Рейтинг",
        "bookmaker_col_bonus": "Бонус",
        "bookmaker_col_license": "Ліцензія",
        "bookmaker_col_min_deposit": "Мін. депозит",
        "bookmaker_col_cta": "Дія",
        "nav_slots": "Ігрові автомати",
        "slot_free": "Ігрові автомати безкоштовно",
        "slot_item_prefix": "Ігровий автомат",
        "slot_play_free": "Грати безкоштовно",
        "slot_provider": "Провайдер",
        "slot_volatility": "Волатильність",
        "slot_paylines": "Лінії виплат",
        "slot_where": "Де грати на реальні гроші",
        "slot_about": "Опис гри",
        "slot_none": "Поки що немає ігрових автоматів.",
        "slot_index_intro": "Найкращі ігрові автомати для українських гравців: рейтинг, RTP, волатильність, провайдери. Усі слоти доступні у демо-режимі без реєстрації.",
        "slot_free_intro": "Грайте у популярні ігрові автомати безкоштовно — без реєстрації, без депозиту, без обмежень. Демо-режим відтворює реальну гру з тими самими RTP і бонус-функціями.",
        "slot_compare_h2": "Порівняння ігрових автоматів",
        "slot_compare_intro": "Швидке порівняння ключових параметрів. Сортуйте за RTP, провайдером або волатильністю.",
        "slot_col_rank": "#",
        "slot_col_name": "Слот",
        "slot_col_provider": "Провайдер",
        "slot_col_rtp": "RTP",
        "slot_col_paylines": "Лінії",
        "slot_col_volatility": "Волатильність",
        "slot_col_action": "Дія",
        "bonus_index_h1": "Бонуси казино",
        "bonus_index_intro": "Найкращі бонусні пропозиції від легальних казино України: рейтинг, порівняння умов, типи бонусів.",
        "bonus_list_prefix": "Бонуси:",
        "bonus_list_intro": "Найкращі бонуси цього типу від легальних казино України. Сортування за рейтингом казино.",
        "bonus_back": "← Усі бонуси",
        "bonus_top_h2": "ТОП-10 бонусів казино",
        "bonus_top_intro": "Рейтинг бонусних пропозицій від легальних казино України. Сортування за оцінкою казино.",
        "bonus_compare_h2": "Порівняння умов бонусів",
        "bonus_compare_intro": "Швидке порівняння ключових параметрів топ-бонусів — обирайте за вейджером і мінімальним депозитом.",
        "bonus_types_h2": "Типи бонусів",
        "bonus_types_intro": "Оберіть тип бонусу, щоб побачити всі казино, які його пропонують.",
        "bonus_col_rank": "#",
        "bonus_col_casino": "Казино",
        "bonus_col_type": "Тип бонусу",
        "bonus_col_amount": "Розмір",
        "bonus_col_wager": "Вейджер",
        "bonus_col_min_deposit": "Мін. депозит",
        "bonus_col_cta": "Дія",
        "bonus_card_at": "у казино",
        "bonus_card_wager": "Вейджер",
        "bonus_card_min_deposit": "Мін. депозит",
        "bonus_none_yet": "Поки що немає бонусів.",
        "blog_index_h1": "Блог",
        "blog_index_intro": "Гайди, новини та поради про онлайн-казино.",
        "blog_back": "← Усі статті",
        "blog_no_posts": "Поки що немає статей.",
        "blog_read": "Читати",
        "author_block_title": "Про автора",
        "author_profile": "Переглянути профіль",
        "author_bio_heading": "Біографія",
        "payment_list_prefix": "Казино з",
        "payment_how_to": "Як здійснити оплату",
        "payment_top": "Найкращі казино",
    },
    "ru": {
        "lang_name": "Русский",
        "breadcrumb_home": "Главная",
        "nav_casinos": "Казино",
        "nav_bonuses": "Бонусы",
        "nav_payments": "Методы оплаты",
        "nav_bookmakers": "Букмекеры",
        "nav_blog": "Блог",
        "nav_about": "О нас",
        "footer_tagline": "Независимые обзоры и рейтинги онлайн-казино.",
        "footer_responsible": "Ответственная игра (18+)",
        "footer_privacy": "Политика конфиденциальности",
        "footer_about": "О нас",
        "footer_18plus": "Азартные игры связаны с риском. Играйте ответственно.",
        "footer_affiliate": (
            "Сайт содержит аффилейт-ссылки. Мы можем получать комиссию за "
            "регистрации по ним — это не влияет на оценку казино."
        ),
        "footer_rights": "Все права защищены.",
        "home_title": "Обзоры и рейтинги онлайн-казино",
        "home_description": (
            "Лучшие онлайн-казино в одном месте: оценки, бонусы без депозита, "
            "фриспины и честные обзоры."
        ),
        "home_h1": "Рейтинг онлайн-казино",
        "home_intro": (
            "Выбирайте проверенные онлайн-казино с лучшими бонусами и честными "
            "оценками. Рейтинг обновляется регулярно."
        ),
        "card_bonus": "Бонус",
        "card_license": "Лицензия",
        "card_review": "Подробнее",
        "card_play": "Играть",
        "card_18plus": "18+ Играйте ответственно",
        "card_no_casinos": "Пока нет казино.",
        "detail_back": "← Назад к рейтингу",
        "detail_about": "О казино",
        "detail_bonuses": "Бонусы",
        "detail_terms": "Условия",
        "detail_rating": "Рейтинг",
        "detail_license_number": "Номер лицензии",
        "detail_payment": "Методы оплаты",
        "detail_review": "обзор",
        "detail_pros": "Преимущества",
        "detail_cons": "Недостатки",
        "detail_ratings": "Оценки по критериям",
        "detail_games": "Игры",
        "detail_payouts": "Выплаты",
        "detail_support": "Поддержка",
        "detail_security": "Лицензия и безопасность",
        "detail_verdict": "Итог",
        "detail_faq": "Частые вопросы",
        "detail_compare": "Сравнение с популярными казино Украины",
        "detail_established": "Год основания",
        "detail_min_deposit": "Мин. депозит",
        "detail_withdrawal": "Время выплат",
        "detail_overall": "Общая оценка",
        "detail_verified_editor": "Проверено редактором",
        "detail_verified_license": "Лицензия КРАИЛ подтверждена",
        "detail_verified_deposit": "Тестовый депозит совершён",
        "detail_methodology": "Как мы оцениваем казино",
        "detail_methodology_intro": "Каждое казино проходит проверку по 4 критериям с равным весом (по 25%). Итоговая оценка — среднее из всех баллов.",
        "detail_method_bonuses": "Бонусы (25%) — размер, вейджер, прозрачность условий, отсутствие скрытых ограничений.",
        "detail_method_games": "Игры (25%) — количество провайдеров, наличие live-казино, демо-режим.",
        "detail_method_payments": "Выплаты (25%) — скорость, методы (в т.ч. гривна), лимиты и комиссии.",
        "detail_method_support": "Поддержка (25%) — украиноязычный чат, время ответа, каналы связи.",
        "detail_similar": "Похожие казино",
        "badge_top": "ТОП-выбор",
        "badge_editor": "Выбор редакции",
        "badge_fast": "Быстрые выплаты",
        "badge_exclusive": "Эксклюзив",
        "badge_new": "Новинка",
        "badge_popular": "Популярное",
        "badge_bonus": "Большой бонус",
        "badge_mobile": "Мобильное",
        "bonus_no_deposit": "Без депозита",
        "bonus_registration": "За регистрацию",
        "bonus_first_deposit": "За первый депозит",
        "bonus_free_spins": "Фриспины",
        "bonus_birthday": "На день рождения",
        "bonus_match": "Матч-бонус",
        "bonus_all": "Все бонусы",
        "casino_all": "Все казино",
        "bookmaker_all": "Все обзоры букмекеров",
        "bookmaker_all_h1": "Обзоры букмекеров",
        "bookmaker_all_intro": "Рейтинг легальных букмекеров Украины: лицензия КРАИЛ, прозрачные выплаты, широкая линия спортивных событий.",
        "bookmaker_bet": "Сделать ставку",
        "bookmaker_none": "Пока нет букмекеров.",
        "bookmaker_compare_h2": "Сравнение букмекеров",
        "bookmaker_compare_intro": "Быстрое сравнение ключевых параметров. Сортируйте по лицензии, бонусу или минимальному депозиту.",
        "bookmaker_col_rank": "#",
        "bookmaker_col_name": "Букмекер",
        "bookmaker_col_rating": "Рейтинг",
        "bookmaker_col_bonus": "Бонус",
        "bookmaker_col_license": "Лицензия",
        "bookmaker_col_min_deposit": "Мин. депозит",
        "bookmaker_col_cta": "Действие",
        "nav_slots": "Игровые автоматы",
        "slot_free": "Игровые автоматы бесплатно",
        "slot_item_prefix": "Игровой автомат",
        "slot_play_free": "Играть бесплатно",
        "slot_provider": "Провайдер",
        "slot_volatility": "Волатильность",
        "slot_paylines": "Линии выплат",
        "slot_where": "Где играть на реальные деньги",
        "slot_about": "Описание игры",
        "slot_none": "Пока нет игровых автоматов.",
        "slot_index_intro": "Лучшие игровые автоматы для украинских игроков: рейтинг, RTP, волатильность, провайдеры. Все слоты доступны в демо-режиме без регистрации.",
        "slot_free_intro": "Играйте в популярные игровые автоматы бесплатно — без регистрации, без депозита, без ограничений. Демо-режим воспроизводит реальную игру с теми же RTP и бонус-функциями.",
        "slot_compare_h2": "Сравнение игровых автоматов",
        "slot_compare_intro": "Быстрое сравнение ключевых параметров. Сортируйте по RTP, провайдеру или волатильности.",
        "slot_col_rank": "#",
        "slot_col_name": "Слот",
        "slot_col_provider": "Провайдер",
        "slot_col_rtp": "RTP",
        "slot_col_paylines": "Линии",
        "slot_col_volatility": "Волатильность",
        "slot_col_action": "Действие",
        "bonus_index_h1": "Бонусы казино",
        "bonus_index_intro": "Лучшие бонусные предложения от легальных казино Украины: рейтинг, сравнение условий, типы бонусов.",
        "bonus_list_prefix": "Бонусы:",
        "bonus_list_intro": "Лучшие бонусы этого типа от легальных казино Украины. Сортировка по рейтингу казино.",
        "bonus_back": "← Все бонусы",
        "bonus_top_h2": "ТОП-10 бонусов казино",
        "bonus_top_intro": "Рейтинг бонусных предложений от легальных казино Украины. Сортировка по оценке казино.",
        "bonus_compare_h2": "Сравнение условий бонусов",
        "bonus_compare_intro": "Быстрое сравнение ключевых параметров топ-бонусов — выбирайте по вейджеру и минимальному депозиту.",
        "bonus_types_h2": "Типы бонусов",
        "bonus_types_intro": "Выберите тип бонуса, чтобы увидеть все казино, которые его предлагают.",
        "bonus_col_rank": "#",
        "bonus_col_casino": "Казино",
        "bonus_col_type": "Тип бонуса",
        "bonus_col_amount": "Размер",
        "bonus_col_wager": "Вейджер",
        "bonus_col_min_deposit": "Мин. депозит",
        "bonus_col_cta": "Действие",
        "bonus_card_at": "в казино",
        "bonus_card_wager": "Вейджер",
        "bonus_card_min_deposit": "Мин. депозит",
        "bonus_none_yet": "Пока нет бонусов.",
        "blog_index_h1": "Блог",
        "blog_index_intro": "Гайды, новости и советы об онлайн-казино.",
        "blog_back": "← Все статьи",
        "blog_no_posts": "Пока нет статей.",
        "blog_read": "Читать",
        "author_block_title": "Об авторе",
        "author_profile": "Посмотреть профиль",
        "author_bio_heading": "Биография",
        "payment_list_prefix": "Казино с",
        "payment_how_to": "Как совершить оплату",
        "payment_top": "Лучшие казино",
    },
}


def is_supported(lang: str) -> bool:
    return lang in LANGUAGES


def get_translations(lang: str) -> dict[str, str]:
    return TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANG])


def strip_lang_prefix(path: str) -> str:
    """Usuwa prefiks języka ze ścieżki.

    '/uk/casino/x/' -> '/casino/x/'
    '/uk/'          -> '/'
    """
    for lang in LANGUAGES:
        if path == f"/{lang}" or path == f"/{lang}/":
            return "/"
        if path.startswith(f"/{lang}/"):
            return path[len(lang) + 1:]  # zostawia wiodący '/'
    return path


def alternate_urls(path: str) -> dict[str, str]:
    """Dla bieżącej ścieżki zwraca URL tej samej strony w każdym języku.

    Używane do przełącznika języków oraz tagów hreflang.
    """
    rest = strip_lang_prefix(path)
    return {lang: f"/{lang}{rest}" for lang in LANGUAGES}
