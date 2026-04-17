#!/usr/bin/env python3
import os
from pathlib import Path

# Простой шаблон для всех оставшихся ботов
TEMPLATE = '''Ты — senior Python-разработчик, специализирующийся на создании Telegram-ботов с использованием библиотеки aiogram 3.x. Твоя задача — написать полноценного, готового к развёртыванию на сервере Telegram-бота «{name}».

**Контекст проекта:**
Этот бот продаётся как готовое решение для {target}. Цель — {goal}. Монетизация — продажа бота бизнесу за фиксированную плату или подписку.

**Функциональные требования:**

1. **Стартовое сообщение и меню:**
   - При команде `/start` бот отправляет приветственное сообщение с названием сервиса и описанием возможностей.
   - Главная клавиатура (ReplyKeyboardMarkup):
{buttons}

2. **Обработка команд:**
{handlers}

3. **Администрирование:**
   - Команда `/admin` — статистика, заявки, рассылка.
   - Команда `/broadcast [текст]` — рассылка всем пользователям.
   - Команда `/export` — выгрузка данных в CSV.

4. **Технические детали:**
   - **Стек:** Python 3.10+, aiogram 3.x, aiosqlite, apscheduler.
   - **Структура:** main.py, config.py, database.py, handlers/, keyboards/, utils/, .env, requirements.txt
   - **.env:** BOT_TOKEN, ADMIN_ID, {env_vars}

5. **Хранение данных:** SQLite с таблицами users, requests, {tables}

6. **Безопасность:** Таймауты, валидация, защита админских команд.

7. **Деплой:** Docker-ready код с инструкцией.

**Формат ответа:** Полный код всех файлов с комментариями.

Напиши код бота согласно этому заданию.
'''

# Данные для каждого бота из имени папки
BOT_DATA = {
    "Бот_Поздравление": ("Поздравление именинника", "организаторов дней рождений", "собирать видеопоздравления от друзей", "🎥 Записать поздравление\n     - 📹 Мои видео\n     - 🎂 О празднике\n     - 📞 Организатор", "Запись видео: загрузка файла, хранение до даты события.", "EVENT_DATE, VIDEO_MAX_MB", "video_greetings (id, sender_id, video_path, uploaded_at)"),
    "Бот_Сборщик_гостей": ("Сбор гостей на мероприятие", "организаторов свадеб и событий", "RSVP и предпочтения гостей", "✅ Подтвердить участие\n     - 🍽️ Выбрать блюдо\n     - 📍 Карта\n     - 📞 Орг", "RSVP форма, выбор блюд, учёт аллергий.", "EVENT_DATE, RSVP_DEADLINE", "guests (id, user_id, rsvp_status, meal_choice, allergies)"),
    "Бот_Вопросы_спикеру": ("Вопросы спикеру", "модераторов конференций", "сбор и рейтинг вопросов", "❓ Задать вопрос\n     - 🔥 Популярные\n     - 📅 Программа\n     - 📞 Модератор", "Анонимные вопросы, лайки, топ для озвучивания.", "EVENT_NAME", "questions (id, session_id, text, likes_count, is_answered)"),
    "Бот_Трансфер": ("Трансфер на мероприятие", "организаторов крупных событий", "координация трансфера гостей", "🚐 Заказать трансфер\n     - 📋 Мои заказы\n     - 📍 Точки встречи\n     - 📞 Диспетчер", "FSM: тип транспорта, откуда, когда, сколько человек.", "EVENT_NAME, DISPATCHER_PHONE", "transfers (id, user_id, vehicle_type, pickup_location, status)"),
    "Бот_Тайный_Санта": ("Тайный Санта", "организаторов корпоративов", "распределение участников и вишлисты", "🎅 Участвовать\n     - 🎁 Мой подопечный\n     - 📝 Вишлист\n     - 📊 Участники", "Регистрация, авто-распределение, вишлисты.", "GAME_NAME, EXCHANGE_DATE", "participants (id, game_id, user_id, wishlist, assigned_to)"),
    "Бот_Сертификат": ("Сертификат участника", "организаторов курсов", "генерация PDF-сертификатов", "📜 Получить сертификат\n     - 📋 Мои сертификаты\n     - ✅ Подтвердить участие\n     - 📞 Поддержка", "Проверка участия, генерация PDF с именем и датой.", "CERT_TEMPLATE, HOURS", "certificates (id, user_id, event_id, pdf_path, issued_at)"),
    "Бот_Расписание_конференции": ("Расписание конференции", "организаторов форумов", "программа и напоминания о секциях", "📅 Программа\n     - ⭐ Избранное\n     - 📍 Карта зала\n     - 📞 Оргкомитет", "Список секций, избранное, напоминания за 5 мин.", "CONF_NAME, CONF_DATE", "sessions (id, title, speaker, time, room), favorites (user_id, session_id)"),
    "Бот_Викторина": ("Викторина для корпоратива", "ведущих мероприятий", "интерактивные викторины с очками", "🎮 Начать игру\n     - 📊 Мой счёт\n     - 🏆 Лидеры\n     - 📋 Правила", "Ведущий запускает раунд, вопросы с вариантами, подсчёт очков.", "HOST_NAME, POINTS_PER_Q", "quiz_games (id, host_id, status), questions (id, game_id, text, options, correct), scores (user_id, points)"),
    "Бот_Программа_свадьбы": ("Программа свадьбы", "молодожёнов", "тайминг и информация для гостей", "📅 Тайминг дня\n     - 📍 Локации\n     - 🚗 Трансфер\n     - 📞 Координатор", "Почасовая программа, адреса, трансфер.", "COUPLE_NAMES, WEDDING_DATE", "schedule (id, time, activity, location), transport (route, departure_time)"),
    "Бот_Фотобудка": ("Фотобудка", "организаторов праздников", "фото с рамкой мероприятия", "📸 Отправить фото\n     - 🖼️ Мои фото\n     - 🎉 Галерея\n     - 📞 Орг", "Загрузка фото, наложение рамки (Pillow), галерея.", "FRAME_PATH, MAX_SIZE_MB", "photos (id, user_id, original_path, processed_path, likes)"),
}

def main():
    base = Path("/workspace/промты_ботов")
    
    for folder_name, data in BOT_DATA.items():
        # Ищем папку
        for path in base.rglob(folder_name):
            if path.is_dir():
                prompt_file = path / "prompt.md"
                if prompt_file.exists():
                    with open(prompt_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if len(content.split('\n')) < 50:
                        name, target, goal, buttons, handlers, env_vars, tables = data
                        new_content = TEMPLATE.format(
                            name=name, target=target, goal=goal,
                            buttons=buttons, handlers=handlers,
                            env_vars=env_vars, tables=tables
                        )
                        with open(prompt_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"✅ {folder_name}")
                    else:
                        print(f"⏭️ {folder_name} (ok)")

if __name__ == "__main__":
    main()
