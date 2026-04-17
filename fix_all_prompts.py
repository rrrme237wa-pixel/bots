#!/usr/bin/env python3
"""Исправляет все промты, добавляя недостающую информацию."""
from pathlib import Path

FULL_TEMPLATE = """Ты — senior Python-разработчик, специализирующийся на создании Telegram-ботов с использованием библиотеки aiogram 3.x. Твоя задача — написать полноценного, готового к развёртыванию на сервере Telegram-бота «{name}».

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
├── main.py              # точка входа, инициализация бота и диспетчера
├── config.py            # загрузка настроек из .env и JSON файлов
├── handlers/
│   ├── user.py          # обработчики пользовательских команд и кнопок
│   └── admin.py         # обработчики админских команд (/admin, /broadcast)
├── keyboards/
│   └── main_menu.py     # функции создания Inline/Reply клавиатур
├── data/
│   ├── {datafiles}
│   └── {media}
├── .env                 # токен бота, ID админа и другие настройки
└── requirements.txt
```
   - **Конфигурация (.env):**
```
BOT_TOKEN=123456:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_ID=123456789
{envvars}
```

5. **Хранение данных:**
{storage}

6. **Обработка ошибок и безопасность:**
   - Все внешние запросы должны иметь таймауты (не более 10 сек) и обработку исключений.
   - При ошибке чтения файлов или БД бот должен отправлять пользователю вежливое сообщение «Сервис временно недоступен, попробуйте позже», а админу — детали ошибки в ЛС.
{security}

7. **Деплой:**
   - Код должен быть готов к запуску на сервере Ubuntu через systemd или Docker.
   - Напиши пример Dockerfile и docker-compose.yml для простоты развёртывания.
   - Включи инструкцию по первому запуску и настройке в файл `README.md`.

**Формат ответа:**
- Предоставь полный код всех файлов проекта.
- Снабди комментариями сложные моменты (особенно FSM, callback_data, работу с БД).
- В ответе используй markdown-блоки для каждого файла с указанием имени файла.
- В конце дай краткую инструкцию по развёртыванию на VPS (Ubuntu 20.04+).

Напиши код Telegram-бота «{name}» согласно этому техническому заданию.
"""

# Данные для всех ботов (пример для нескольких категорий)
BOTS_DATA = {
    "06_Авто_и_транспорт": {
        "Бот_Водитель_мероприятие": {
            "name": "Водитель на мероприятие",
            "context": "Сервис заказа водителей с личным авто для мероприятий (свадьбы, корпоративы, трансферы). Клиенты выбирают класс авто, дату и время. Водители получают заявки.",
            "greeting": "с названием сервиса, преимуществами (пунктуальность, опытные водители) и кнопками выбора услуг",
            "keyboard": "InlineKeyboardMarkup с категориями услуг",
            "buttons": ["🚗 Легковое авто", "🚐 Минивэн", "🚌 Автобус", "📅 Мои заказы", "📞 Связаться"],
            "handlers": "**Выбор авто:** Каталог с фото, описанием, вместимостью, ценой за час.\n**Заказ:** FSM опросник: дата, время, маршрут, длительность. Расчёт итоговой стоимости.\n**Мои заказы:** История заказов со статусами (новый, подтверждён, выполнен).",
            "admin": "/admin - статистика заказов, /drivers - список водителей, /broadcast - рассылка",
            "libs": "aiohttp для внешних запросов, pillow для обработки фото",
            "datafiles": "vehicles.json (автопарк с характеристиками)",
            "media": "vehicles_photos/",
            "envvars": "SERVICE_NAME=AutoDrive\nMIN_BOOKING_HOURS=3\nBASE_RATE_PER_HOUR=1500",
            "storage": "SQLite: users(user_id,role), orders(id,user_id,vehicle_id,date,hours,total,status), vehicles(id,name,capacity,rate_per_hour)",
            "security": "Проверка доступности авто перед подтверждением. Блокировка пользователей после 3 отмен без причины."
        },
        "Бот_Напоминалка_ТО": {
            "name": "Напоминалка ТО",
            "context": "Бот для автосервисов. Автоматически напоминает клиентам о необходимости планового ТО berdasarkan пробегу или времени. Увеличивает возвращаемость клиентов на 40%.",
            "greeting": "с названием сервиса и текущими акциями на ТО",
            "keyboard": "ReplyKeyboardMarkup",
            "buttons": ["📅 Записаться на ТО", "📊 Моя история", "💰 Прайс ТО", "📞 Контакты"],
            "handlers": "**Запись:** Выбор типа ТО (масло, фильтры, колодки), даты и времени.\n**Напоминания:** Клиент вносит данные авто (марка, пробег, дата последнего ТО). Бот рассчитывает следующее ТО.\n**История:** Все прошлые визиты с чеками.",
            "admin": "/add_client - добавить клиента, /reminders_today - кому напомнить, /stats - статистика",
            "libs": "aioschedule для планирования",
            "datafiles": "to_types.json, prices.json",
            "media": "service_photos/",
            "envvars": "SERVICE_NAME=АвтоМастер\nREMINDER_KM=10000\nREMINDER_MONTHS=6",
            "storage": "SQLite: clients(user_id,car_model,last_km,last_to_date,next_reminder), visits(client_id,date,type,cost)",
            "security": "Рассылка не чаще 1 раза в неделю. Возможность отписаться от напоминаний."
        }
    }
}

def format_buttons(btn_list):
    return '\n'.join([f"     - {b}" for b in btn_list])

total_fixed = 0
for category, bots in BOTS_DATA.items():
    cat_path = Path(f"/workspace/промты_ботов/{category}")
    if not cat_path.exists():
        print(f"⚠️ Категория {category} не найдена")
        continue
    
    for folder, data in bots.items():
        bot_path = cat_path / folder
        prompt_file = bot_path / "prompt.md"
        
        if not bot_path.exists():
            print(f"⚠️ Папка {folder} не найдена")
            continue
        
        data['buttons'] = format_buttons(data['buttons'])
        content = FULL_TEMPLATE.format(**data)
        
        prompt_file.write_text(content, encoding='utf-8')
        lines = len(content.split('\n'))
        print(f"✅ {category}/{folder}: {lines} строк")
        total_fixed += 1

print(f"\n🎉 Исправлено промтов: {total_fixed}")
