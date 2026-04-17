Ты — senior Python-разработчик (aiogram 3.x). Создай фитнес-бота.

**Контекст:** Для клиентов бизнеса. Цель — автоматизация процесса: места группа.

**Функционал:**
1. `/start` — меню: 📅 Расписание, 💪 Мои тренировки, 🔔 Напоминания
2. FSM для записи на занятия, подсчет мест
3. APScheduler для напоминаний об абонементах
4. Админ: `/add_workout`, `/broadcast`

**Технологии:** aiogram 3.x, sqlite3, apscheduler
**Структура:** main.py, handlers/, keyboards/, database/
**.env:** BOT_TOKEN, ADMIN_ID, GYM_NAME
