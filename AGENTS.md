# Crumbs — Agentic Coding Guide

## Project Overview

Django-based bakery ordering system (migrated from Streamlit/CLI). Customers place orders
with weight/size/quantity options; managers perform CRUD operations. No tests exist yet.

## Project Structure

```
Crumbs/
├── bakery/                        # Main Django app
│   ├── templates/bakery/          # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── menu.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   └── order_confirmed.html
│   ├── templatetags/              # Custom template tags
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                   # Admin configuration
│   ├── apps.py
│   ├── forms.py                   # Django forms
│   ├── models.py                  # Database models
│   ├── tests.py                   # Tests
│   ├── urls.py                    # URL routing
│   └── views.py                   # View functions
├── crumbs_project/                # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                # Project settings (env-based config)
│   ├── urls.py                    # Root URL configuration
│   └── wsgi.py
├── static/                        # Static files (CSS, JS, images)
├── .venv/                         # Virtual environment (gitignored)
├── .env                           # Environment variables (gitignored)
├── .gitignore
├── AGENTS.md                     # This file
├── manage.py                     # Django management script
├── README.md
└── requirements.txt              # Python dependencies
```

## Build / Run / Lint / Test Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the development server
python manage.py runserver

# Run Django system checks
python manage.py check

# Run database migrations (after defining models)
python manage.py migrate

# Create migrations after model changes
python manage.py makemigrations

# Run tests
python manage.py test

# No linter/formatter is configured. If adding one, prefer ruff:
# pip install ruff
# ruff check .                            # lint
# ruff format .                           # format
# ruff check --fix .                      # auto-fix

# Install dependencies
pip install -r requirements.txt
```

## Code Style Guidelines

### Imports
- Group: standard library → third-party (django, decouple) → local modules
- One import per line
- No `import *` unless absolutely necessary

### Formatting & Naming
- **4-space indentation**, no tabs
- **snake_case** for functions, variables, file names
- **PascalCase** for classes
- **UPPER_CASE** for module-level constants
- Prefer **single quotes** for strings, **double quotes** for docstrings or when the string contains a single quote
- **f-strings** for string formatting (avoid `.format()` or `%`)

### Types
- Do NOT use type hints (existing code does not use them, stay consistent)
- If type hints are added later, prefer Python 3.10+ union syntax (`X | Y`)

### Django Patterns
- Use class-based views or function-based views consistently (follow existing pattern)
- Use `{% url %}` template tag for URL lookups (never hardcode URLs)
- Use Django's ORM for all database queries (never raw SQL)
- Use `python-decouple` for all environment variable access
- Forms should use Django's `forms.Form` or `forms.ModelForm`

### Database
- Use Django ORM migrations for schema management
- Never write raw SQL unless absolutely necessary (and document why)
- Use parameterized queries if raw SQL is unavoidable

### Error Handling
- Catch specific exceptions first, then generic `Exception` as fallback
- Show errors in templates with Django messages framework
- Use `try/except/else` pattern for database operations

### Functions
- Keep functions focused and well-scoped
- Follow Django's "fat models, thin views" principle

### Git
- Commit messages: conventional commits format (feat:, fix:, refactor:, chore:, docs:)
- Keep credentials in `.env` (gitignored), never commit them
