# Crumbs → Django Migration: Kickoff Prompt

Copy-paste this to an AI agent to start executing the migration plan at `.sisyphus/MIGRATE_Crumbs_Django.md`.

---

## Execution Prompt

```
You are executing Milestone 0 of the Crumbs → Django migration plan at
.sisyphus/MIGRATE_Crumbs_Django.md. The workspace is /home/aureon/knowledge/Crumbs.

CONTEXT: This is a bakery ordering system currently using Streamlit + mysql-connector.
We are migrating to Django 5.x. No requirements.txt, no pyproject.toml exist.
Python 3.14.4 is available. The existing codebase has these source files:
main.py, Customer.py, Manager.py, home.py, interaction.py, creating database.py,
creds.py (gitignored), .gitignore (only creds.py + temp.py), AGENTS.md, README.md,
and .sisyphus/ directory with plan files.

MILESTONE 0 GOAL: Scaffold Django project, create bakery app, write .gitignore,
update AGENTS.md, delete all old Streamlit files. Then git add . && git commit
with a conventional commit message.

STEP-BY-STEP:
1. Update .gitignore with full Python/Django/Docker/IDE entries (see plan)
2. Create requirements.txt with django>=5.1,<6.0 and python-decouple
3. Create .env file with DJANGO_SECRET_KEY, DJANGO_DEBUG=True
4. Create directory structure: bakery/templates/bakery/, bakery/templatetags/
5. Run: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
6. Run: django-admin startproject crumbs_project .
7. Create bakery app: python manage.py startapp bakery
8. Set up settings.py: add bakery to INSTALLED_APPS, load env vars, templates, static config
9. Create base template files in bakery/templates/bakery/ (base.html, home.html, menu.html, cart.html, checkout.html, order_confirmed.html)
10. Create crumbs_project/urls.py with bakery.urls included
11. Delete old files: main.py, Customer.py, Manager.py, home.py, interaction.py, creating database.py, __pycache__/
12. Run python manage.py check — must show no issues
13. Update AGENTS.md to reflect Django project structure
14. git add . && git commit -m "feat: scaffold Django project with bakery app

- Initialize Django 5.1 project for Crumbs bakery ordering system
- Create bakery app with model/view/template/admin structure
- Configure django-decouple for environment variable management
- Add comprehensive .gitignore for Python/Django/Docker/IDE artifacts
- Remove all Streamlit source files (main.py, Customer.py, Manager.py, home.py,
  interaction.py, creating database.py)
- Set up SQLite for development with path to swap to PostgreSQL in production
"

CONSTRAINTS:
- Do NOT run any Django management commands that require a database (migrate, etc.)
  — those come in Milestone 1 after models are defined
- Use python-decouple for all env vars, never hardcode secrets
- Keep templates minimal (just extends base.html with placeholder content)
- Update AGENTS.md with new Django project structure info
- If python3 manage.py check fails, fix the issue — do not proceed with broken project
```

---

To run each subsequent milestone after M0 completes, use the same pattern: read the
corresponding milestone section from `.sisyphus/MIGRATE_Crumbs_Django.md` and feed
it as context + instructions to your execution agent.
