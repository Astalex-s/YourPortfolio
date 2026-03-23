# YourPortfolio

Персональный портфолио-сайт на Django с тёмным дизайном (dark navy + gold accent).

---

## Страницы

| URL | Описание |
|-----|----------|
| `/` | Главная — Hero секция |
| `/about/` | О себе + Навыки |
| `/services/` | Услуги |
| `/resume/` | Резюме (образование + опыт работы) |
| `/portfolio/` | Портфолио (сетка проектов) |
| `/portfolio/<slug>/` | Детальная страница проекта |
| `/contact/` | Форма обратной связи |
| `/admin/` | Панель управления |

---

## Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Astalex-s/YourPortfolio.git
cd YourPortfolio

# 2. Создать виртуальное окружение
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

# 3. Обновить pip
python -m pip install --upgrade pip

# 4. Установить зависимости
pip install -r requirements/local.txt

# 5. Создать .env файл
cp .env.example .env
# Отредактируйте .env (см. раздел «Переменные окружения»)

# 6. Применить миграции
python manage.py migrate

# 7. Создать суперпользователя
python manage.py createsuperuser

# 8. Запустить сервер
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/ — Админ-панель: http://127.0.0.1:8000/admin/

---

## Переменные окружения (.env)

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
CONTACT_EMAIL=your@email.com
DEFAULT_FROM_EMAIL=noreply@yoursite.com
```

---

## Наполнение через Админ-панель

### 1. Настройки сайта (Pages → Настройки сайта)

Singleton-запись, одна на весь сайт.

| Поле | Описание |
|------|----------|
| `owner_name` | Ваше имя |
| `tagline` | Должность / слоган |
| `about_text` | Текст блока «О себе» |
| `avatar` | Фото на главной (рекомендуется 3:4) |
| `about_photo` | Фото на странице «Обо мне» |
| `logo` | Логотип в шапке и подвале |
| `email` | Контактный email |
| `phone` | Телефон |
| `location` | Город / страна |
| `birth_date` | Дата рождения |
| `resume_pdf` | PDF резюме для скачивания |
| `meta_description` | SEO-описание |

### 2. Образование (Pages → Настройки сайта → Образование)

Inline-таблица, можно добавить несколько записей.

| Поле | Описание |
|------|----------|
| `degree` | Степень / специальность |
| `institution` | Учебное заведение |
| `period` | Период, например: `2018 — 2022` |
| `description` | Дополнительное описание |
| `order` | Порядок отображения |

### 3. Опыт работы (Pages → Настройки сайта → Опыт работы)

Inline-таблица, можно добавить несколько записей.

| Поле | Описание |
|------|----------|
| `position` | Должность |
| `company` | Компания |
| `period` | Период, например: `2022 — настоящее время` |
| `description` | Описание обязанностей |
| `order` | Порядок отображения |

### 4. Социальные ссылки (Pages → Настройки сайта → Ссылки соцсетей)

| Поле | Пример |
|------|--------|
| `name` | GitHub |
| `url` | `https://github.com/username` |
| `icon_class` | `fab fa-github` |
| `order` | 1 |

Иконки из Font Awesome 6: https://fontawesome.com/icons

### 5. Сертификаты (Pages → Настройки сайта → Сертификаты)

| Поле | Описание |
|------|----------|
| `name` | Название сертификата |
| `issuer` | Кто выдал |
| `year` | Год получения |
| `image` | Изображение сертификата |
| `url` | Ссылка на оригинал (опционально) |
| `order` | Порядок в слайдере |

### 6. Теги технологий (Portfolio → Теги технологий)

| Поле | Описание |
|------|----------|
| `name` | Название технологии |
| `color` | HEX-цвет, например `#3776AB` |
| `logo_key` | Slug для иконки с [simpleicons.org](https://simpleicons.org) |

Примеры `logo_key`: `python`, `django`, `fastapi`, `flask`, `git`, `postgresql`,
`docker`, `nginx`, `vite`, `telegram`, `googlesheets`, `n8n`, `javascript`, `html5`, `css3`

### 7. Проекты (Portfolio → Проекты)

| Поле | Описание |
|------|----------|
| `title` | Название проекта |
| `slug` | URL-идентификатор (заполняется автоматически) |
| `mockup_image` | Изображение для карточки (рекомендуется 4:3) |
| `brief_description` | Краткое описание (до 300 символов) |
| `task_description` | Задача |
| `solution_description` | Решение |
| `how_it_works` | Как работает (опционально) |
| `result_description` | Результат |
| `demo_video_url` | Ссылка на YouTube/Vimeo (embed URL) |
| `demo_video_file` | Видео-файл |
| `source_link` | Ссылка на репозиторий |
| `live_demo_link` | Ссылка на живое демо |
| `tech_stack` | Теги технологий |
| `is_featured` | Показывать на главной странице |
| `is_published` | Опубликован |
| `order` | Порядок в сетке |

Скриншоты добавляются через Inline «Скриншоты проекта» — появятся в слайдере на детальной странице.

> В полях описаний (задача, решение и т.д.) поддерживаются абзацы: двойной перенос строки создаёт новый абзац.

---

## Структура проекта

```
├── apps/
│   ├── pages/          # Главная, About, Services, Resume, Contact
│   ├── portfolio/      # Список и детали проектов
│   ├── accounts/       # Авторизация
│   ├── core/           # Абстрактные модели, context processors
│   └── crm/            # CRM-модуль
├── config/
│   └── settings/
│       ├── base.py
│       ├── local.py    # Для разработки (DEBUG=True, SQLite)
│       └── production.py
├── templates/
│   ├── base.html
│   └── components/
│       ├── navbar.html
│       └── footer.html
├── static/
│   ├── css/main.css
│   └── js/main.js
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
└── docker/             # Docker-конфигурация
```

---

## Стек

- **Backend:** Django 5.2, Python
- **БД:** SQLite (разработка) / PostgreSQL (продакшн)
- **Фронтенд:** Vanilla JS, кастомный CSS (без Bootstrap)
- **Деплой:** Gunicorn + Nginx + Docker
- **Статика:** WhiteNoise

---

## Docker

```bash
docker-compose up --build
```

---

## Цветовая схема

| Переменная | Значение | Назначение |
|------------|----------|------------|
| `--bg-primary` | `#0a0e1a` | Основной фон |
| `--bg-secondary` | `#0d1228` | Фон чередующихся секций |
| `--bg-card` | `#111830` | Фон карточек |
| `--accent` | `#f0a500` | Золотой акцент |
| `--text-primary` | `#ffffff` | Основной текст |
| `--text-secondary` | `#8892b0` | Вторичный текст |

Все переменные — в `static/css/main.css` в блоке `:root {}`.
