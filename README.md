# YourPortfolio

Персональный портфолио-сайт на Django с тёмным дизайном (dark navy + gold accent).

---

## Страницы

| URL | Описание |
|-----|----------|
| `/` | Главная — Hero секция |
| `/about/` | О себе + Навыки |
| `/services/` | Услуги |
| `/resume/` | Резюме (образование + опыт) |
| `/portfolio/` | Портфолио (сетка проектов) |
| `/portfolio/<slug>/` | Детальная страница проекта |
| `/contact/` | Форма обратной связи |
| `/admin/` | Панель управления |

---

## Быстрый старт

```bash
# 1. Клонировать и войти в папку
cd YourPortfolio

# 2. Создать виртуальное окружение
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

# 3. Обновить pip (важно — иначе Pillow не установится)
python -m pip install --upgrade pip

# 4. Установить зависимости
pip install -r requirements/local.txt

# 4. Создать .env файл (скопировать из примера)
cp .env.example .env            # если есть
# или создать вручную (см. раздел «Переменные окружения»)

# 5. Применить миграции
python manage.py migrate

# 6. Создать суперпользователя
python manage.py createsuperuser

# 7. Запустить сервер
python manage.py runserver
```

Сайт будет доступен по адресу: http://127.0.0.1:8000/

---

## Переменные окружения (.env)

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
CONTACT_EMAIL=your@email.com
DEFAULT_FROM_EMAIL=noreply@yoursite.com
```

---

## Наполнение сайта через Админ-панель

Перейдите на http://127.0.0.1:8000/admin/ и заполните:
### 1. Настройки сайта (SiteSettings)
Раздел **Pages → Настройки сайта** — единственная запись, Singleton.

| Поле | Описание |
|------|----------|
| `owner_name` | Ваше имя (отображается в логотипе, Hero, About) |
| `tagline` | Должность / слоган (например: «Backend Developer») |
| `about_text` | Текст блока «О себе» |
| `avatar` | Фото (рекомендуемое соотношение 3:4) |
| `email` | Контактный email |
| `phone` | Телефон (отображается в шапке) |
| `location` | Город / страна |
| `resume_pdf` | PDF резюме для скачивания |
| `meta_description` | SEO-описание |
| `cv_data` | JSON с данными CV (см. ниже) |

### 2. Формат cv_data (JSON)

```json
{
  "experience": [
    {
      "position": "Backend Developer",
      "company":  "Company Name",
      "period":   "Jan 2023 — Present",
      "description": "Описание опыта работы."
    }
  ],
  "education": [
    {
      "degree":      "Bachelor of Computer Science",
      "institution": "University Name",
      "period":      "2019 — 2023",
      "description": "Описание."
    }
  ],
  "skills_bars": [
    {"name": "Python",     "percent": 90},
    {"name": "Django",     "percent": 85},
    {"name": "PostgreSQL", "percent": 80},
    {"name": "Docker",     "percent": 75},
    {"name": "REST API",   "percent": 88},
    {"name": "Git",        "percent": 85}
  ]
}
```

> Если `skills_bars` не заполнен, страница /about/ покажет дефолтные навыки из `views.py`.

### 3. Социальные ссылки (SocialLink)

Добавляются через Inline в настройках сайта.

| Поле | Пример |
|------|--------|
| `name` | GitHub |
| `url` | https://github.com/username |
| `icon_class` | `fab fa-github` |
| `order` | 1 |

Иконки — из Font Awesome 6: https://fontawesome.com/icons

### 4. Проекты (Portfolio → Projects)

| Поле | Описание |
|------|----------|
| `title` | Название проекта |
| `slug` | URL-идентификатор (авто) |
| `mockup` | Изображение для сетки |
| `short_description` | Краткое описание |
| `task` / `solution` / `result` | Описание работы |
| `tech_stack` | Теги технологий |
| `is_featured` | Показывать на главной |
| `is_published` | Опубликован |

---

## Структура проекта

```
YourPortfolio/
├── apps/
│   ├── pages/          # Главная, About, Services, Resume, Contact
│   ├── portfolio/      # Список и детали проектов
│   ├── accounts/       # Авторизация
│   ├── core/           # Абстрактные модели, context processors
│   └── crm/            # (Phase 2)
├── config/
│   └── settings/
│       ├── base.py
│       ├── local.py
│       └── production.py
├── templates/
│   ├── base.html
│   └── components/
│       ├── navbar.html
│       └── footer.html
├── static/
│   ├── css/main.css
│   └── js/main.js
└── media/              # Загруженные файлы
```

---

## Docker (опционально)

```bash
docker-compose up --build
```

---

## Настройка навыков (skills_bars)

Для страницы `/about/` навыки с прогресс-барами берутся из `cv_data.skills_bars`.
Каждый элемент: `{"name": "Название", "percent": 85}`.

Если поле не заполнено — показываются дефолтные навыки из `apps/pages/views.py`:
```python
DEFAULT_SKILLS = [
    {'name': 'Python',     'percent': 90},
    ...
]
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

Все переменные — в `static/css/main.css` в блоке `:root { }`.
