# Backend — Интернет-магазин (Django + DRF)

Учебный REST API интернет-магазина по техническому заданию.

## Стек

- Python 3.11+
- Django 5/6
- Django REST Framework
- djangorestframework-simplejwt (JWT)
- django-cors-headers
- django-filter
- Pillow
- drf-spectacular (Swagger)
- SQLite (разработка)

## Структура

```
backend/
├── config/           # настройки проекта
├── apps/
│   ├── catalog/      # категории, товары, изображения
│   ├── orders/       # заказы и позиции
│   └── users/        # регистрация, JWT, профиль
├── manage.py
├── requirements.txt
└── README.md
```

## Быстрый старт

```bash
# 1. Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Миграции
python manage.py migrate

# 4. Создать суперпользователя
python manage.py createsuperuser

# 5. Запуск
python manage.py runserver
```

Админка: http://127.0.0.1:8000/admin/  
Swagger:  http://127.0.0.1:8000/api/docs/  
API:      http://127.0.0.1:8000/api/

> По умолчанию в `settings.py` путь к БД может быть `/tmp/store_db.sqlite3` (для окружений с ограничениями на запись). Для локальной разработки замените на `BASE_DIR / 'db.sqlite3'`.

## API endpoints

### Каталог
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/categories/` | Список категорий |
| GET | `/api/products/` | Список товаров (фильтры, поиск, сортировка, пагинация) |
| GET | `/api/products/{id}/` | Детали товара |

**Параметры `/api/products/`:**
- `category=<slug>` — фильтр по категории
- `min_price=`, `max_price=` — диапазон цен
- `in_stock=true` — только в наличии
- `search=<текст>` — поиск по названию/описанию/SKU
- `ordering=price` / `-price` / `-created_at`
- `page=2` — пагинация (по 12)

### Авторизация (JWT)
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/auth/register/` | Регистрация `{email, password, password_confirm, first_name}` |
| POST | `/api/auth/login/` | Вход `{email, password}` → access + refresh |
| POST | `/api/auth/refresh/` | Обновление access-токена `{refresh}` |
| GET/PATCH | `/api/auth/me/` | Профиль текущего пользователя (Bearer token) |

### Заказы
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/orders/` | Создать заказ (гость или авторизованный) |
| GET | `/api/orders/` | История заказов (только авторизованный) |
| GET | `/api/orders/{id}/` | Детали заказа (владелец) |

**Пример создания заказа:**
```json
{
  "full_name": "Иван Иванов",
  "phone": "+996700123456",
  "email": "ivan@mail.com",
  "address": "г. Бишкек, ул. Чуй 1",
  "comment": "",
  "delivery_method": "courier",
  "payment_method": "cash",
  "items": [
    {"product": 1, "quantity": 2},
    {"product": 3, "quantity": 1}
  ]
}
```

`delivery_method`: `pickup` | `courier`  
`payment_method`: `cash` | `card`

## Админка

В Django Admin доступны:
- Категории (с иерархией parent/children)
- Товары + инлайн изображений
- Заказы + инлайн позиций, смена статуса

## Тестовые данные

После миграций можно создать демо-данные (категории и товары) через shell или админку.  
Суперпользователь по умолчанию (если создан скриптом): `admin` / `admin123`.

## CORS

Разрешены origins:
- `http://localhost:5173`
- `http://127.0.0.1:5173`
- `http://localhost:3000`
- `http://127.0.0.1:3000`
