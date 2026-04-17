#!/usr/bin/env python3
import os
from pathlib import Path

BASE = '''Ты — senior Python-разработчик, специализирующийся на создании Telegram-ботов с использованием библиотеки aiogram 3.x. Твоя задача — написать полноценного, готового к развёртыванию на сервере Telegram-бота «{name}».

**Контекст проекта:**
{context}

**Функциональные требования:**

1. **Стартовое сообщение и меню:**
   - При команде `/start` бот отправляет приветственное сообщение {greeting}.
   - Под сообщением — клавиатура с кнопками ({keyboard}):
{buttons}

2. **Обработка кнопок и команд:**
{handlers}

3. **Администрирование:**
{admin}

4. **Технические детали:**
   - **Стек:** Python 3.10+, aiogram 3.x, python-dotenv для конфигурации, aiofiles для работы с файлами, asyncio, {libs}
   - **Структура проекта:**
```
/bot
├── main.py              # точка входа
├── config.py            # загрузка настроек из .env и JSON
├── handlers/
│   ├── user.py          # обработчики пользовательских команд
│   └── admin.py         # обработчики админских команд
├── keyboards/
│   └── main_menu.py     # клавиатуры
├── data/
│   ├── {datafiles}
│   └── {media}
├── .env                 # токен бота, ID админа и другие настройки
└── requirements.txt
```
   - **Конфигурация (.env):**
```
BOT_TOKEN=123456:ABCdef...
ADMIN_ID=123456789
{envvars}
```

5. **Хранение данных:**
{storage}

6. **Обработка ошибок и безопасность:**
   - Все внешние запросы должны иметь таймауты и обработку исключений.
   - При ошибке чтения файлов или БД бот должен отправлять пользователю вежливое сообщение «Сервис временно недоступен, попробуйте позже», а админу — детали ошибки в ЛС.
{security}

7. **Деплой:**
   - Код должен быть готов к запуску на сервере Ubuntu через systemd или Docker (напиши пример Dockerfile и docker-compose.yml для простоты).
   - Включи инструкцию по первому запуску и настройке в файл `README.md`.

**Формат ответа:**
- Предоставь полный код всех файлов проекта.
- Снабди комментариями сложные моменты.
- В ответе используй markdown-блоки для каждого файла.
- В конце дай краткую инструкцию по развёртыванию на VPS.

Напиши код Telegram-бота «{name}» согласно этому техническому заданию.
'''

BOTS = []

# 01 Салоны красоты
BOTS.extend([
{"cat":"01_Салоны_красоты","f":"Бот_Прайс_с_расчётом","n":"Прайс с расчётом стоимости","ctx":"Бот для мастеров сферы красоты. Клиенты выбирают услуги, бот считает итог. Повышает конверсию в запись.","gr":"с названием салона и меню услуг","kb":"InlineKeyboardMarkup с категориями","btn":"     - 💅 Маникюр\n     - 👁️ Брови\n     - 💇‍♀️ Волосы\n     - 🧮 Рассчитать\n     - 📞 Записаться","hdl":"**Услуги:** Список с ценами из JSON, чекбоксы для выбора.\n**Расчёт:** Суммирование выбранных услуг, детализация.\n**Запись:** FSM выбор даты/времени или ссылка на YClients.","adm":"/admin - статистика, /broadcast - рассылка, /export - CSV","lib":"aiohttp","dat":"services.json","med":"portfolio/","env":"SALON_NAME=Студия Анна\nBOOKING_URL=https://yclients.com","stor":"SQLite: users, cart(user_id,service_id), appointments","sec":"Рассылка 0.05сек задержка, корзина живёт 24ч"},
{"cat":"01_Салоны_красоты","f":"Бот_Напомни_про_ресницы","n":"Напомни про ресницы","ctx":"Бот для мастеров ресниц. Авто-напоминания о коррекции за 2 дня. Возвращаемость +30%.","gr":"с именем мастера и фото работ","kb":"ReplyKeyboardMarkup","btn":"     - 📅 Записаться\n     - ⏰ Напоминания\n     - 💰 Прайс\n     - 📸 Работы","hdl":"**/add_client:** Мастер вносит дату, бот ставит напоминание.\n**Напоминания:** Клиент видит дату, подтверждает запись.","adm":"/add_client, /clients, /remind_today, /stats","lib":"aioschedule","dat":"prices.json","med":"portfolio/","env":"MASTER_NAME=Елена\nREMINDER_DAYS=2","stor":"SQLite: clients(user_id,date,next_reminder), reminder_log","sec":"Телефоны хешируются, рассылка 0.1сек"},
{"cat":"01_Салоны_красоты","f":"Бот_Сборщик_пожеланий","n":"Сборщик пожеланий к стрижке","ctx":"Клиент заранее шлёт фото стрижки и описание. Экономит 20мин консультации.","gr":"с призывом подготовить визит","kb":"InlineKeyboard для опроса","btn":"     - ✂️ Оформить заявку\n     - 📋 Мои заявки\n     - 💈 О мастере","hdl":"FSM: мастер, дата, услуга, фото (до 5), описание, контакт.","adm":"/new_requests, /confirm [id], /calendar","lib":"aiofiles, pillow","dat":"masters.json","med":"master_photos/","env":"SALON_NAME=Барбершоп\nMAX_PHOTOS=5","stor":"SQLite: requests(user_id,master_id,photos_json,status)","sec":"Фото макс 10MB, архив через 30 дней"},
{"cat":"01_Салоны_красоты","f":"Бот_Мои_работы","n":"Мои работы портфолио","ctx":"Цифровое портфолио с фильтрами. Заменяет Instagram.","gr":"с именем мастера и кнопкой работ","kb":"InlineKeyboard с фильтрами","btn":"     - 🖼️ Все работы\n     - 💅 Ногти\n     - 👁️ Брови\n     - ❤️ Популярное","hdl":"Лента по 10 фото, фильтры, лайки, поиск по хештегам.","adm":"/upload, /delete [id], /stats, /top","lib":"aiofiles, pillow","dat":"categories.json","med":"portfolio/","env":"CATEGORIES=ногти,брови\nPHOTOS_PER_PAGE=10","stor":"SQLite: portfolio(file_id,category,likes_count), likes","sec":"Ресайз до 1280x1280, проверка прав"},
{"cat":"01_Салоны_красоты","f":"Бот_Оцени_сервис","n":"Оцени сервис","ctx":"Сбор отзывов и оценок. NPS, аналитика для владельца.","gr":"с просьбой оценить обслуживание","kb":"InlineKeyboard с звёздами","btn":"     - ⭐⭐⭐⭐⭐\n     - ⭐⭐⭐⭐\n     - 📝 Отзыв","hdl":"Выбор звёзд, комментарий обязателен для 1-3. QR для кабинета.","adm":"/dashboard, /reviews_bad, /export Excel","lib":"plotly, openpyxl","dat":"questions_nps.json","med":"qr_codes/","env":"NPS_QUESTION=Порекомендуете?\nALERT_ON=3","stor":"SQLite: ratings(user_id,rating,comment), nps_responses","sec":"Анонимность при экспорте, 1 оценка в 24ч"},
{"cat":"01_Салоны_красоты","f":"Бот_Предзапись_коллекция","n":"Предзапись на новую коллекцию","ctx":"Лист ожидания новой услуги. Создаёт ажиотаж, оценивает спрос.","gr":"с анонсом коллекции и датой старта","kb":"InlineKeyboard","btn":"     - 🎯 В лист ожидания\n     - 📋 Моё место\n     - 🖼️ Коллекция","hdl":"Оставляет контакт, получает номер. Рассылка по очереди при старте.","adm":"/waiting_list, /open_booking, /export_waitlist","lib":"aiohttp","dat":"collection.json","med":"collection_photos/","env":"COLLECTION=Осень 2024\nDISCOUNT=15","stor":"SQLite: waitlist(user_id,position,notified)","sec":"Капча от ботов, удаление через 7 дней"},
{"cat":"01_Салоны_красоты","f":"Бот_Свободное_окошко","n":"Свободное окошко","ctx":"Мгновенная рассылка об освободившемся времени со скидкой.","gr":"с призывом подписаться на уведомления","kb":"ReplyKeyboard","btn":"     - 🔔 Подписаться\n     - 📅 Записаться\n     - 💰 Акции","hdl":"Подписка на дни/время. /free_slot [дата] [скидка] - рассылка.","adm":"/free_slot, /subscribers, /stats_slots","lib":"aioschedule","dat":"slots_history.json","med":"promo_banners/","env":"RESERVE_MIN=15\nMIN_DISCOUNT=10","stor":"SQLite: subscriptions(user_id,preferred_days), free_slots","sec":"Макс 3 рассылки в день"},
{"cat":"01_Салоны_красоты","f":"Бот_Визитка_мастера","n":"Визитка мастера","ctx":"Готовое решение: прайс, фото, контакты, запись. Замена соцсетям.","gr":"с именем, фото, описанием","kb":"InlineKeyboard","btn":"     - 📋 Прайс\n     - 📸 Работы\n     - 📍 Контакты\n     - 📞 Записаться","hdl":"Прайс из JSON, медиа-группа фото, геолокация, ссылка на запись.","adm":"/admin статистика, /broadcast, /update_profile","lib":"aiohttp","dat":"prices.json","med":"portfolio/","env":"MASTER_NAME=Анна\nPROMO_ACTIVE=True","stor":"SQLite: users(user_id,last_seen)","sec":"Рассылка 0.05сек, проверка файлов"}
])

print(f"Создано {len(BOTS)} записей")
for b in BOTS:
    p = Path(f"/workspace/промты_ботов/{b['cat']}/{b['f']}/prompt.md")
    if p.parent.exists():
        content = BASE.format(
            name=b['n'], context=b['ctx'], greeting=b['gr'],
            keyboard=b['kb'], buttons=b['btn'], handlers=b['hdl'],
            admin=b['adm'], libs=b['lib'], datafiles=b['dat'],
            media=b['med'], envvars=b['env'], storage=b['stor'],
            security=b['sec']
        )
        p.write_text(content, encoding='utf-8')
        print(f"✅ {b['cat']}/{b['f']}")
    else:
        print(f"⚠️ Нет папки: {b['cat']}/{b['f']}")
