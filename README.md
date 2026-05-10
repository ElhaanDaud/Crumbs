# Crumbs 🍪

A Django-based bakery ordering system. Customers browse a menu of cakes, beverages, cookies, and pastries, add items to a cart with weight/size/quantity options, and place orders. Managers can perform CRUD operations on the database via Django Admin.

Originally built as a Streamlit/CLI prototype (12th grade project), migrated to Django for production deployment.

## Features

- **Menu browsing** — View items by category (cakes, beverages, cookies, pastries) with prices
- **Shopping cart** — Add items with configurable weight (cakes), size (beverages), or quantity (cookies/pastries); update or remove items
- **Checkout flow** — Enter customer details, choose home delivery, receive order confirmation with a unique order ID
- **Admin panel** — Django Admin interface for managers to manage products, categories, employees, and orders
- **Responsive design** — Works across devices with a clean Bootstrap-based UI

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5.1+ |
| Database | PostgreSQL 16 (prod) / SQLite (dev) |
| Frontend | Bootstrap 5, Django Templates |
| WSGI | Gunicorn |
| Containerization | Docker / Docker Compose |

## Quick Start

### Local development

```bash
# Clone the repo
git clone <repo-url>
cd Crumbs

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env    # or create from scratch:
                        # DJANGO_SECRET_KEY=your-secret-key
                        # DJANGO_DEBUG=True
                        # DJANGO_SETTINGS_MODULE=crumbs_project.settings.dev

# Run migrations
python manage.py migrate

# Start the dev server
python manage.py runserver
```

Visit **http://localhost:8000** in your browser.

### Docker (production-like)

```bash
cp .env.example .env    # set DJANGO_SECRET_KEY and DB_PASSWORD
docker compose up --build
```

The app will be available at **http://localhost:8000**.

## Project Structure

```
Crumbs/
├── bakery/                  # Main Django app
│   ├── templates/bakery/   # HTML templates (home, menu, cart, checkout, etc.)
│   ├── templatetags/        # Custom template tags
│   ├── admin.py            # Admin configuration
│   ├── cart.py             # Cart session management
│   ├── forms.py            # Django forms
│   ├── models.py           # Database models
│   ├── urls.py             # URL routing
│   └── views.py            # View functions
├── crumbs_project/          # Django project settings
│   └── settings/           # Settings split by environment
│       ├── base.py         # Shared settings
│       ├── dev.py          # Development overrides
│       └── prod.py         # Production overrides
├── static/                 # Static assets (CSS, JS, images)
├── docker-compose.yml      # Docker Compose setup (PostgreSQL + Django)
├── Dockerfile              # Docker image definition
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Database Models

| Model | Description |
|---|---|
| `Category` | Product categories (C00=Cakes, B00=Beverages, K00=Cookies, P00=Pastries) |
| `Cake` | Cakes with price per kg |
| `Beverage` | Beverages with medium size price |
| `Cookie` | Cookies with price per 500g |
| `Pastry` | Pastries with price per piece |
| `CustomerOrder` | Customer orders with delivery details |
| `Employee` | Staff records (name, salary, department) |
| `PersonalDetail` | Contact information (phone, email) |

## API / URLs

| Path | View | Description |
|---|---|---|
| `/` | `home` | Landing page |
| `/menu/` | `menu_view` | Category listing |
| `/menu/<category_id>/` | `category_items` | Items in a category |
| `/cart/` | `cart_view` | Shopping cart |
| `/cart/add/<category_id>/<item_id>/` | `add_to_cart_view` | Add item to cart |
| `/cart/remove/<key>/` | `remove_from_cart_view` | Remove cart item |
| `/checkout/` | `checkout_view` | Checkout form |
| `/order-confirmed/<order_id>/` | `order_confirmed` | Order confirmation |
| `/admin/` | Django Admin | Admin CRUD interface |

## Admin Access

Login at `/admin/` with a superuser account:

```bash
python manage.py createsuperuser
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | Yes | Django secret key |
| `DJANGO_DEBUG` | No | Set `True` for development |
| `DJANGO_SETTINGS_MODULE` | No | Default: `crumbs_project.settings.dev` |
| `DJANGO_DB_URL` | No | Database URL (defaults to SQLite) |
| `DB_PASSWORD` | Docker only | PostgreSQL password |

## Commands

```bash
# Run tests
python manage.py test

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Django system checks
python manage.py check
```

## License

MIT
