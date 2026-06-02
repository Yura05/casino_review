"""Wypełnienie bazy przykładowymi danymi (do testów / developmentu).

Uruchomienie (po python -m app.init_db):
    python -m app.seed

Skrypt jest idempotentny per-encja: kasyna i wpisy bloga sprawdzane osobno,
więc ponowne uruchomienie dosypie tylko brakujące dane.
"""

from app.database import SessionLocal
from app.models import (
    Author,
    BettingCategory,
    BlogPost,
    Bonus,
    Bookmaker,
    Casino,
    CasinoFaq,
    Category,
    Slot,
)

_HIGH = ("Висока", "Высокая")
_MED = ("Середня", "Средняя")


def seed_casinos(db) -> None:
    if db.query(Casino).count() > 0:
        print("Kasyna juz istnieja - pomijam.")
        return

    # Kategorie (cechy kasyn — do menu "Kasyna")
    cat = {}
    for slug, uk, ru in [
        ("novi", "Нові казино", "Новые казино"),
        ("litsenzovani", "Ліцензовані казино", "Лицензированные казино"),
        ("mobilni", "Мобільні казино", "Мобильные казино"),
        ("shvydki-vyplaty", "Швидкі виплати", "Быстрые выплаты"),
        ("min-depozyt", "Мінімальний депозит", "Минимальный депозит"),
        ("na-hryvni", "Казино на гривні", "Казино на гривны"),
        ("bez-verifikatsiyi", "Казино без верифікації в Україні", "Казино без верификации в Украине"),
    ]:
        c = Category(slug=slug, name_uk=uk, name_ru=ru)
        cat[slug] = c
        db.add(c)

    # 10 realnych legalnych kasyn w Ukrainie. UWAGA: dane PRZYKLADOWE (placeholder) — zweryfikuj.
    data = [
        dict(slug="cosmolot", name="Cosmolot", rating=4.6, lic="150/2021", est=2020, dep="100 ₴",
             pay="Visa,Mastercard,Приват24,Apple Pay,Google Pay", badges="popular",
             sb=4.6, sg=4.5, sp=4.6, ss=4.5, cats=["litsenzovani", "mobilni", "na-hryvni", "novi"],
             bonus_uk="100% + 50 фріспінів", bonus_ru="100% + 50 фриспинов",
             trait_uk="одне з найвідоміших легальних онлайн-казино України з великим вибором слотів",
             trait_ru="одно из самых известных легальных онлайн-казино Украины с большим выбором слотов"),
        dict(slug="parimatch", name="PariMatch", rating=4.7, lic="151/2021", est=2019, dep="100 ₴",
             pay="Visa,Mastercard,Приват24,Apple Pay", badges="top,fast",
             sb=4.7, sg=4.6, sp=4.7, ss=4.6, cats=["litsenzovani", "mobilni", "shvydki-vyplaty", "na-hryvni"],
             bonus_uk="150% до 45 000 ₴", bonus_ru="150% до 45 000 ₴",
             trait_uk="відомий бренд зі ставками на спорт і казино та швидкими виплатами в гривні",
             trait_ru="известный бренд со ставками на спорт и казино и быстрыми выплатами в гривне"),
        dict(slug="favbet", name="Favbet", rating=4.5, lic="152/2021", est=2019, dep="100 ₴",
             pay="Visa,Mastercard,Приват24", badges="editor",
             sb=4.5, sg=4.5, sp=4.5, ss=4.5, cats=["litsenzovani", "mobilni", "na-hryvni"],
             bonus_uk="100% до 20 000 ₴", bonus_ru="100% до 20 000 ₴",
             trait_uk="популярний майданчик, що поєднує казино та беттинг із зручним гривневим сервісом",
             trait_ru="популярная площадка, сочетающая казино и беттинг с удобным гривневым сервисом"),
        dict(slug="vbet", name="VBET", rating=4.5, lic="153/2021", est=2020, dep="100 ₴",
             pay="Visa,Mastercard,Приват24,Skrill",
             sb=4.5, sg=4.6, sp=4.4, ss=4.5, cats=["litsenzovani", "mobilni", "na-hryvni"],
             bonus_uk="100% до 30 000 ₴", bonus_ru="100% до 30 000 ₴",
             trait_uk="міжнародний оператор із широкою лінією ігор і легальною роботою в Україні",
             trait_ru="международный оператор с широкой линией игр и легальной работой в Украине"),
        dict(slug="ggbet", name="GGBet", rating=4.4, lic="154/2021", est=2021, dep="50 ₴",
             pay="Visa,Mastercard,Приват24,BTC", badges="new",
             sb=4.5, sg=4.4, sp=4.4, ss=4.3, cats=["litsenzovani", "mobilni", "novi", "min-depozyt"],
             bonus_uk="100% + 100 фріспінів", bonus_ru="100% + 100 фриспинов",
             trait_uk="казино з акцентом на кіберспорт, слоти та сучасні методи оплати",
             trait_ru="казино с акцентом на киберспорт, слоты и современные методы оплаты"),
        dict(slug="pin-up", name="Pin-Up", rating=4.6, lic="155/2021", est=2020, dep="100 ₴",
             pay="Visa,Mastercard,Приват24,Apple Pay", badges="bonus,fast",
             sb=4.7, sg=4.5, sp=4.6, ss=4.5, cats=["litsenzovani", "mobilni", "na-hryvni", "shvydki-vyplaty"],
             bonus_uk="150% + 250 фріспінів", bonus_ru="150% + 250 фриспинов",
             trait_uk="яскраве казино з щедрими бонусами та великою колекцією слотів",
             trait_ru="яркое казино со щедрыми бонусами и большой коллекцией слотов"),
        dict(slug="cosmobet", name="Cosmobet", rating=4.4, lic="156/2022", est=2022, dep="75 ₴",
             pay="Visa,Mastercard,Приват24", badges="new",
             sb=4.4, sg=4.4, sp=4.4, ss=4.4, cats=["litsenzovani", "mobilni", "novi", "na-hryvni", "min-depozyt", "bez-verifikatsiyi"],
             bonus_uk="120% до 15 000 ₴", bonus_ru="120% до 15 000 ₴",
             trait_uk="порівняно нове українське казино зі стрімким розвитком і зручним інтерфейсом",
             trait_ru="сравнительно новое украинское казино с быстрым развитием и удобным интерфейсом"),
        dict(slug="first", name="First", rating=4.3, lic="157/2022", est=2021, dep="100 ₴",
             pay="Visa,Mastercard,Приват24",
             sb=4.3, sg=4.3, sp=4.4, ss=4.3, cats=["litsenzovani", "mobilni", "na-hryvni", "min-depozyt"],
             bonus_uk="100% до 10 000 ₴", bonus_ru="100% до 10 000 ₴",
             trait_uk="класичне легальне казино з простим стартом і стабільними виплатами",
             trait_ru="классическое легальное казино с простым стартом и стабильными выплатами"),
        dict(slug="slotoking", name="Slotoking", rating=4.5, lic="158/2021", est=2020, dep="100 ₴",
             pay="Visa,Mastercard,Приват24,Apple Pay",
             sb=4.5, sg=4.6, sp=4.5, ss=4.4, cats=["litsenzovani", "mobilni", "na-hryvni"],
             bonus_uk="175% + 70 фріспінів", bonus_ru="175% + 70 фриспинов",
             trait_uk="казино для шанувальників слотів із великим каталогом ігрових автоматів",
             trait_ru="казино для поклонников слотов с большим каталогом игровых автоматов"),
        dict(slug="champion", name="Champion", rating=4.4, lic="159/2022", est=2021, dep="100 ₴",
             pay="Visa,Mastercard,Приват24", badges="fast",
             sb=4.4, sg=4.4, sp=4.5, ss=4.3, cats=["litsenzovani", "mobilni", "na-hryvni", "shvydki-vyplaty", "bez-verifikatsiyi"],
             bonus_uk="100% + 100 фріспінів", bonus_ru="100% + 100 фриспинов",
             trait_uk="українське казино з лотереями, слотами та швидкими гривневими виплатами",
             trait_ru="украинское казино с лотереями, слотами и быстрыми гривневыми выплатами"),
    ]

    for d in data:
        c = Casino(
            slug=d["slug"], name=d["name"], rating=d["rating"],
            license="КРАІЛ", license_number=d["lic"], established=d["est"],
            min_deposit=d["dep"], payment_methods=d["pay"], badges=d.get("badges"),
            affiliate_link=f"https://example.com/go/{d['slug']}",
            score_bonuses=d["sb"], score_games=d["sg"], score_payments=d["sp"], score_support=d["ss"],
            withdrawal_time_uk="1–2 дні", withdrawal_time_ru="1–2 дня",
            bonus_uk=d["bonus_uk"], bonus_ru=d["bonus_ru"],
            description_uk=f"{d['name']} — {d['trait_uk']}.",
            description_ru=f"{d['name']} — {d['trait_ru']}.",
            overview_uk=(
                f"{d['name']} працює в Україні за ліцензією КРАІЛ та орієнтоване на місцевих гравців: "
                f"гривневий рахунок, поповнення через Приват24 і повністю україномовний сервіс. "
                f"Це {d['trait_uk']}."
            ),
            overview_ru=(
                f"{d['name']} работает в Украине по лицензии КРАИЛ и ориентировано на местных игроков: "
                f"гривневый счёт, пополнение через Приват24 и полностью украиноязычный сервис. "
                f"Это {d['trait_ru']}."
            ),
            pros_uk="Легальна ліцензія КРАІЛ\nГривневий рахунок і Приват24\nШвидкі виплати\nУкраїномовна підтримка",
            pros_ru="Легальная лицензия КРАИЛ\nГривневый счёт и Приват24\nБыстрые выплаты\nУкраиноязычная поддержка",
            cons_uk="Верифікація обовʼязкова перед виплатою\nБонуси з умовами відіграшу",
            cons_ru="Верификация обязательна перед выплатой\nБонусы с условиями отыгрыша",
            verdict_uk=(
                f"{d['name']} — надійний вибір для гравців з України, які цінують легальність, "
                f"гривневі виплати та зручний локальний сервіс."
            ),
            verdict_ru=(
                f"{d['name']} — надёжный выбор для игроков из Украины, которые ценят легальность, "
                f"гривневые выплаты и удобный локальный сервис."
            ),
            categories=[cat[s] for s in d["cats"]],
        )
        c.bonuses = [
            Bonus(type="first_deposit", amount=d["bonus_uk"],
                  wager="x35", min_deposit=d["dep"],
                  terms_uk="На перший депозит, вейджер x35.",
                  terms_ru="На первый депозит, вейджер x35."),
            Bonus(type="registration", amount="25 FS",
                  wager="x40", min_deposit="—",
                  terms_uk="Фріспіни після реєстрації акаунта.",
                  terms_ru="Фриспины после регистрации аккаунта."),
        ]
        c.faqs = [
            CasinoFaq(position=1,
                      question_uk=f"Чи легальне казино {d['name']} в Україні?",
                      question_ru=f"Легально ли казино {d['name']} в Украине?",
                      answer_uk=f"Так, {d['name']} працює за ліцензією КРАІЛ і дозволене для гравців віком від 18 років.",
                      answer_ru=f"Да, {d['name']} работает по лицензии КРАИЛ и разрешено для игроков старше 18 лет."),
            CasinoFaq(position=2,
                      question_uk="Який мінімальний депозит?",
                      question_ru="Какой минимальный депозит?",
                      answer_uk=f"Мінімальний депозит у {d['name']} — {d['dep']}.",
                      answer_ru=f"Минимальный депозит в {d['name']} — {d['dep']}."),
        ]
        db.add(c)

    print(f"Dodano: {len(data)} kasyn (realne marki, dane przykladowe) + kategorie + bonusy + FAQ.")


def seed_blog(db) -> None:
    if db.query(BlogPost).count() > 0:
        print("Wpisy bloga juz istnieja - pomijam.")
        return

    p1 = BlogPost(
        slug="yak-obraty-kazyno",
        title_uk="Як обрати онлайн-казино: 5 порад",
        title_ru="Как выбрать онлайн-казино: 5 советов",
        meta_description_uk="П’ять простих критеріїв, які допоможуть обрати надійне онлайн-казино.",
        meta_description_ru="Пять простых критериев, которые помогут выбрать надёжное онлайн-казино.",
        body_uk=(
            "Вибір онлайн-казино починається з ліцензії. Переконайтеся, що казино має "
            "дійсну ліцензію визнаного регулятора.\n\n"
            "Далі зверніть увагу на умови бонусів: розмір вейджеру, терміни та обмеження. "
            "Привабливий бонус із нереальними умовами користі не дасть.\n\n"
            "Також важливі методи оплати, швидкість виплат і якість підтримки. "
            "Перевірені казино мають прозорі правила та оперативну службу підтримки."
        ),
        body_ru=(
            "Выбор онлайн-казино начинается с лицензии. Убедитесь, что казино имеет "
            "действующую лицензию признанного регулятора.\n\n"
            "Далее обратите внимание на условия бонусов: размер вейджера, сроки и ограничения. "
            "Привлекательный бонус с нереальными условиями пользы не принесёт.\n\n"
            "Также важны методы оплаты, скорость выплат и качество поддержки. "
            "Проверенные казино имеют прозрачные правила и оперативную службу поддержки."
        ),
    )

    p2 = BlogPost(
        slug="bonusy-bez-depozytu",
        title_uk="Бонуси без депозиту: як це працює",
        title_ru="Бонусы без депозита: как это работает",
        meta_description_uk="Що таке бонус без депозиту і на що звертати увагу в умовах.",
        meta_description_ru="Что такое бонус без депозита и на что обращать внимание в условиях.",
        body_uk=(
            "Бонус без депозиту — це винагорода, яку казино дає новим гравцям без потреби "
            "поповнювати рахунок. Зазвичай це фріспіни або невелика сума на баланс.\n\n"
            "Головне — уважно читати умови відіграшу (вейджер). Саме вони визначають, "
            "чи зможете ви вивести виграш."
        ),
        body_ru=(
            "Бонус без депозита — это вознаграждение, которое казино даёт новым игрокам без "
            "необходимости пополнять счёт. Обычно это фриспины или небольшая сумма на баланс.\n\n"
            "Главное — внимательно читать условия отыгрыша (вейджер). Именно они определяют, "
            "сможете ли вы вывести выигрыш."
        ),
    )

    db.add_all([p1, p2])
    print("Dodano: 2 wpisy bloga.")


def seed_bookmakers(db) -> None:
    if db.query(Bookmaker).count() > 0:
        print("Bukmacherzy juz istnieja - pomijam.")
        return

    # Kategorie zakładów (kolejność = kolejność w menu)
    bc_esport = BettingCategory(slug="kibersport", name_uk="Онлайн ставки на кіберспорт", name_ru="Онлайн ставки на киберспорт")
    bc_box = BettingCategory(slug="boks", name_uk="Ставки на бокс онлайн", name_ru="Ставки на бокс онлайн")
    bc_basket = BettingCategory(slug="basketbol", name_uk="Онлайн ставки на баскетбол", name_ru="Онлайн ставки на баскетбол")
    bc_football = BettingCategory(slug="futbol", name_uk="Спортивні ставки на футбол", name_ru="Спортивные ставки на футбол")
    bc_legal = BettingCategory(slug="legalni-bk", name_uk="Легальні БК України", name_ru="Легальные БК Украины")
    bc_sport = BettingCategory(slug="stavky-na-sport", name_uk="Ставки на спорт", name_ru="Ставки на спорт")
    db.add_all([bc_esport, bc_box, bc_basket, bc_football, bc_legal, bc_sport])

    b1 = Bookmaker(
        slug="betking",
        name="BetKing",
        rating=4.6,
        logo="img/bookmakers/betking.svg",
        license="КРАІЛ",
        license_number="150/2021",
        established=2019,
        min_deposit="100 ₴",
        payment_methods="Visa,Mastercard,Privat24,Apple Pay",
        affiliate_link="https://example.com/go/betking",
        bonus_uk="Бонус на перший депозит 100% до 5000 ₴",
        bonus_ru="Бонус на первый депозит 100% до 5000 ₴",
        description_uk="BetKing — легальний український букмекер із широкою лінією ставок на спорт і кіберспорт.",
        description_ru="BetKing — легальный украинский букмекер с широкой линией ставок на спорт и киберспорт.",
        pros_uk="Легальна ліцензія КРАІЛ\nШирока лінія на футбол і кіберспорт\nШвидкі виплати на картку та Приват24\nЗручний мобільний застосунок",
        pros_ru="Легальная лицензия КРАИЛ\nШирокая линия на футбол и киберспорт\nБыстрые выплаты на карту и Приват24\nУдобное мобильное приложение",
        cons_uk="Висока маржа на нішеві ринки\nОбмежені live-трансляції",
        cons_ru="Высокая маржа на нишевые рынки\nОграниченные live-трансляции",
        overview_uk=(
            "BetKing працює в Україні за ліцензією КРАІЛ із 2019 року. Букмекер пропонує "
            "ставки на футбол, баскетбол, кіберспорт та десятки інших видів спорту.\n\n"
            "Лінія широка, коефіцієнти конкурентні, а виплати на українські картки та Приват24 — швидкі."
        ),
        overview_ru=(
            "BetKing работает в Украине по лицензии КРАИЛ с 2019 года. Букмекер предлагает "
            "ставки на футбол, баскетбол, киберспорт и десятки других видов спорта.\n\n"
            "Линия широкая, коэффициенты конкурентные, а выплаты на украинские карты и Приват24 — быстрые."
        ),
        verdict_uk=(
            "BetKing — надійний вибір для українських гравців: легальна ліцензія, широка лінія "
            "та швидкі виплати в гривні роблять його одним із лідерів нашого рейтингу букмекерів."
        ),
        verdict_ru=(
            "BetKing — надёжный выбор для украинских игроков: легальная лицензия, широкая линия "
            "и быстрые выплаты в гривне делают его одним из лидеров нашего рейтинга букмекеров."
        ),
        betting_categories=[bc_football, bc_sport, bc_legal, bc_esport],
    )

    b2 = Bookmaker(
        slug="goalbet",
        name="GoalBet",
        rating=4.2,
        logo="img/bookmakers/goalbet.svg",
        license="Curacao",
        license_number="8048/JAZ2",
        established=2020,
        min_deposit="50 ₴",
        payment_methods="Visa,Mastercard,Privat24",
        affiliate_link="https://example.com/go/goalbet",
        bonus_uk="Фрібет 500 ₴ для новачків",
        bonus_ru="Фрибет 500 ₴ для новичков",
        description_uk="GoalBet робить акцент на футболі та баскетболі з вигідними коефіцієнтами.",
        description_ru="GoalBet делает акцент на футболе и баскетболе с выгодными коэффициентами.",
        pros_uk="Низький мінімальний депозит (50 ₴)\nВигідні коефіцієнти на футбол\nФрібет для новачків",
        pros_ru="Низкий минимальный депозит (50 ₴)\nВыгодные коэффициенты на футбол\nФрибет для новичков",
        cons_uk="Немає ставок на кіберспорт\nЛіцензія Curaçao (не українська)",
        cons_ru="Нет ставок на киберспорт\nЛицензия Curaçao (не украинская)",
        overview_uk=(
            "GoalBet — букмекер для любителів футболу та баскетболу. Працює з 2020 року, "
            "пропонує фрібет для новачків і зручне поповнення через Приват24."
        ),
        overview_ru=(
            "GoalBet — букмекер для любителей футбола и баскетбола. Работает с 2020 года, "
            "предлагает фрибет для новичков и удобное пополнение через Приват24."
        ),
        verdict_uk=(
            "GoalBet підійде гравцям, які роблять ставки переважно на футбол і баскетбол "
            "та цінують низький поріг входу."
        ),
        verdict_ru=(
            "GoalBet подойдёт игрокам, которые делают ставки преимущественно на футбол и баскетбол "
            "и ценят низкий порог входа."
        ),
        betting_categories=[bc_football, bc_basket, bc_box, bc_sport],
    )

    db.add_all([b1, b2])
    print("Dodano: 2 bukmacherow + kategorie zakladow.")


def seed_slots(db) -> None:
    if db.query(Slot).count() > 0:
        print("Sloty juz istnieja - pomijam.")
        return

    def slot(slug, name_uk, name_ru, provider, rtp, paylines, vol, desc_uk, desc_ru):
        return Slot(
            slug=slug, name_uk=name_uk, name_ru=name_ru, provider=provider,
            rtp=rtp, paylines=paylines, volatility_uk=vol[0], volatility_ru=vol[1],
            description_uk=desc_uk, description_ru=desc_ru,
            image=f"img/slots/{slug}.svg",  # plik SVG po slugu w static/img/slots/
        )

    slots = [
        slot("book-of-dead", "Book of Dead", "Book of Dead", "Play'n GO", "96.21%", "10", _HIGH,
             "Book of Dead — культовий слот у єгипетському стилі від Play'n GO з фріспінами та символом, що розширюється.",
             "Book of Dead — культовый слот в египетском стиле от Play'n GO с фриспинами и расширяющимся символом."),
        slot("book-of-ra", "Book of Ra", "Book of Ra", "Novomatic", "95.10%", "10", _HIGH,
             "Book of Ra від Novomatic — класичний слот про пошуки скарбів Стародавнього Єгипту.",
             "Book of Ra от Novomatic — классический слот о поисках сокровищ Древнего Египта."),
        slot("gates-of-olympus", "Gates of Olympus", "Gates of Olympus", "Pragmatic Play", "96.50%", "Scatter Pays", _HIGH,
             "Gates of Olympus — популярний слот від Pragmatic Play з механікою множників і виплатами за кластери.",
             "Gates of Olympus — популярный слот от Pragmatic Play с механикой множителей и выплатами за кластеры."),
        slot("big-bamboo", "Big Bamboo", "Big Bamboo", "Push Gaming", "96.13%", "—", _HIGH,
             "Big Bamboo від Push Gaming — динамічний слот із високою віддачею та бонусними раундами.",
             "Big Bamboo от Push Gaming — динамичный слот с высокой отдачей и бонусными раундами."),
        slot("crazy-monkey", "Crazy Monkey", "Crazy Monkey", "Igrosoft", "95.36%", "9", _MED,
             "Crazy Monkey — легендарний слот від Igrosoft із бонус-грою та ризик-раундом.",
             "Crazy Monkey — легендарный слот от Igrosoft с бонус-игрой и риск-раундом."),
        slot("aztec-gold", "Aztec Gold", "Aztec Gold", "Igrosoft", "95.00%", "9", _MED,
             "Aztec Gold (Піраміда) — класичний слот від Igrosoft про скарби ацтеків.",
             "Aztec Gold (Пирамида) — классический слот от Igrosoft о сокровищах ацтеков."),
        slot("polunychky", "Полунички", "Клубнички", "Igrosoft", "96.00%", "9", _MED,
             "Полунички (Fruit Cocktail) — улюблений фруктовий слот від Igrosoft із бонус-грою.",
             "Клубнички (Fruit Cocktail) — любимый фруктовый слот от Igrosoft с бонус-игрой."),
        slot("sweet-bonanza", "Sweet Bonanza", "Sweet Bonanza", "Pragmatic Play", "96.51%", "Scatter Pays", _HIGH,
             "Sweet Bonanza — солодкий слот від Pragmatic Play із множниками та купівлею бонусу.",
             "Sweet Bonanza — сладкий слот от Pragmatic Play с множителями и покупкой бонуса."),
        slot("aviator", "Aviator", "Aviator", "Spribe", "97.00%", "—", _HIGH,
             "Aviator від Spribe — популярна краш-гра, де треба забрати виграш до того, як літак полетить.",
             "Aviator от Spribe — популярная краш-игра, где нужно забрать выигрыш до того, как самолёт улетит."),
    ]
    db.add_all(slots)
    print(f"Dodano: {len(slots)} slotow.")


def seed_authors(db) -> None:
    if db.query(Author).count() > 0:
        print("Autorzy juz istnieja - pomijam.")
        return

    # UWAGA: dane przykladowe. Przed publikacja podmien na PRAWDZIWA osobe
    # (Google penalizuje fikcyjnych ekspertow w tematyce YMYL/hazard).
    author = Author(
        slug="olena-tkachenko",
        avatar="img/authors/placeholder.svg",
        name_uk="Олена Ткаченко",
        name_ru="Елена Ткаченко",
        role_uk="Експертка з онлайн-казино, головна редакторка",
        role_ru="Эксперт по онлайн-казино, главный редактор",
        bio_uk=(
            "Олена понад 8 років аналізує онлайн-казино: перевіряє ліцензії, умови "
            "бонусів і швидкість виплат. Відповідає за редакційні стандарти та "
            "об’єктивність оцінок на сайті."
        ),
        bio_ru=(
            "Елена более 8 лет анализирует онлайн-казино: проверяет лицензии, условия "
            "бонусов и скорость выплат. Отвечает за редакционные стандарты и "
            "объективность оценок на сайте."
        ),
    )
    db.add(author)
    print("Dodano: 1 autor.")


def main() -> None:
    db = SessionLocal()
    try:
        seed_casinos(db)
        seed_bookmakers(db)
        seed_slots(db)
        seed_blog(db)
        seed_authors(db)
        db.commit()
        print("Seed zakonczony.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
