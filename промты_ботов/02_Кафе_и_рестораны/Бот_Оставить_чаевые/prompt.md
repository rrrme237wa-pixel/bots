Ты — senior Python-разработчик, специализирующийся на Telegram-ботах (aiogram 3.x). Создай бота для салонов красоты.

**Контекст:** Бот для клиентов бизнеса. Цель — автоматизация процесса: оставить чаевые. Монетизация: продажа мастерам/салонам.

**Функционал:**
1. `/start` — приветствие, меню (InlineKeyboard): 📋 Услуги, 📸 Портфолио, 📍 Контакты, 📞 Записаться
2. Кнопки:
   - Услуги: список с ценами из JSON
   - Портфолио: медиа-группа фото
   - Контакты: телефон, адрес, карта
   - Записаться: ссылка на YClients/DIKIDI
3. Админ: `/admin` (статистика), `/broadcast` (рассылка)

**Технологии:** Python 3.10+, aiogram 3.x, sqlite3, aiofiles
**Структура:** main.py, config.py, handlers/, keyboards/, data/, .env
**.env:** BOT_TOKEN, ADMIN_ID, MASTER_NAME, BOOKING_URL

**Хранение:** SQLite (users, appointments)
**Деплой:** Docker, docker-compose.yml
