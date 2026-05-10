# Crumbs → Django Migration: Action Plan

> **Objective**: Migrate the Streamlit-based Crumbs bakery ordering system to Django 5.x.
> The new system replaces `Customer.py`, `Manager.py`, `home.py`, `main.py`, and `interaction.py`
> with a proper MVC web application, while faithfully preserving all functionality.

---

## Pre-Flight: Git Hygiene

Before any migration work, the repo needs a proper `.gitignore` and clean baseline.

### `.gitignore` additions (MUST include)

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# Virtual environment
.venv/
venv/
env/

# Django
*.sqlite3
media/
staticfiles/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment / secrets
.env
creds.py
temp.py

# OS
.DS_Store
Thumbs.db
```

### Git convention for this migration

Every milestone ends with `git add . && git commit`. Commit messages follow
[Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short description>

<optional body describing what and why>
```

Types used: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`.

---

## Milestone 0: Django Project Scaffolding

**Goal**: Get a running Django project with SQLite (dev) and proper project structure.

### Steps

1. Create `requirements.txt`:
   ```
   django>=5.1,<6.0
   python-decouple
   ```

2. Create `.env` (gitignored):
   ```
   DJANGO_SECRET_KEY=django-insecure-change-me-in-production
   DJANGO_DEBUG=True
   DJANGO_DB_URL=sqlite:///db.sqlite3
   ```

3. Scaffold Django project:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   django-admin startproject crumbs_project .
   ```

4. Create the main app:
   ```bash
   python manage.py startapp bakery
   ```

5. Register `bakery` in `INSTALLED_APPS`.

6. Set up `settings.py`:
   - Load `DJANGO_SECRET_KEY` and `DJANGO_DEBUG` from `python-decouple`
   - Configure `DATABASES` for SQLite (dev)
   - Add `STATICFILES_DIRS` and `TEMPLATES` dirs
   - Set `LOGIN_URL = '/admin/login/'`
   - Add `INTERNAL_IPS` for dev toolbar (optional)

7. Create directory structure:
   ```
   bakery/
   ├── templates/bakery/
   │   ├── base.html
   │   ├── home.html
   │   ├── menu.html
   │   ├── cart.html
   │   └── checkout.html
   ├── templatetags/
   │   └── __init__.py
   ├── models.py
   ├── views.py
   ├── urls.py
   ├── admin.py
   ├── forms.py
   └── tests.py
   ```

8. Create `crumbs_project/urls.py` with includes.

9. Run `python manage.py check` — clean output.

10. Delete old Streamlit files: `main.py`, `Customer.py`, `Manager.py`, `home.py`,
    `interaction.py`, `creating database.py`, `__pycache__/`.

### Commit

```
git add .
git commit -m "feat: scaffold Django project with bakery app

- Initialize Django 5.1 project (crumbs_project)
- Create bakery app with template and static structure
- Configure settings with python-decouple for env vars
- Add .gitignore for Python/Django/IDE artifacts
- Remove all Streamlit source files (main.py, Customer.py, Manager.py, home.py,
  interaction.py, creating database.py)
- Set up SQLite for development, production config via DATABASE_URL
"
```

### Verification

```bash
python manage.py check      # → System check identified no issues (0 silenced)
python manage.py runserver  # → starts on http://127.0.0.1:8000
```

---

## Milestone 1: Database Models + Migrations

**Goal**: Django models that exactly replicate the MySQL schema from `creating database.py`,
+ migrations with seed data.

### Django Models (`bakery/models.py`)

```python
from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    """Product categories: Cakes, Beverages, Cookies, Pastries"""
    id = models.CharField(max_length=3, primary_key=True)  # C00, B00, K00, P00
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['id']

    def __str__(self):
        return self.name

class Cake(models.Model):
    id = models.CharField(max_length=3, primary_key=True)  # C01..C10
    name = models.CharField(max_length=50)
    price_1kg = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} — ₹{self.price_1kg}/kg'

class Beverage(models.Model):
    id = models.CharField(max_length=3, primary_key=True)  # B01..B10
    name = models.CharField(max_length=50)
    price_medium = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name_plural = 'beverages'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} — ₹{self.price_medium}/med'

class Cookie(models.Model):
    id = models.CharField(max_length=3, primary_key=True)  # K01..K10
    name = models.CharField(max_length=50)
    price_500g = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name_plural = 'cookies'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} — ₹{self.price_500g}/500g'

class Pastry(models.Model):
    id = models.CharField(max_length=3, primary_key=True)  # P01..P10
    name = models.CharField(max_length=50)
    price_per_piece = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name_plural = 'pastries'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} — ₹{self.price_per_piece}/pc'

class Employee(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    salary = models.PositiveIntegerField()
    department = models.CharField(max_length=20)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} ({self.department})'

class PersonalDetail(models.Model):
    """Employee personal details (phone, email)"""
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    phone_no = models.BigIntegerField()
    email_id = models.EmailField(max_length=40)

    def __str__(self):
        return f'{self.name} — {self.email_id}'

class CustomerOrder(models.Model):
    """Customer orders (c_details table)"""
    name = models.CharField(max_length=30)
    phone_no = models.BigIntegerField()
    address = models.CharField(max_length=70, blank=True, default='-')
    amount = models.PositiveIntegerField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return f'Order #{self.id} — {self.name} — ₹{self.amount}'
```

### Admin Registration (`bakery/admin.py`)

```python
from django.contrib import admin
from .models import (
    Category, Cake, Beverage, Cookie, Pastry,
    Employee, PersonalDetail, CustomerOrder,
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_per_page = 10

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price_1kg']
    search_fields = ['name']
    list_filter = ['price_1kg']
    list_per_page = 20

@admin.register(Beverage)
class BeverageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price_medium']
    search_fields = ['name']
    list_per_page = 20

@admin.register(Cookie)
class CookieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price_500g']
    search_fields = ['name']
    list_per_page = 20

@admin.register(Pastry)
class PastryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price_per_piece']
    search_fields = ['name']
    list_per_page = 20

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'salary', 'department']
    search_fields = ['name', 'department']
    list_filter = ['department']
    list_editable = ['salary', 'department']
    list_per_page = 20

@admin.register(PersonalDetail)
class PersonalDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone_no', 'email_id']
    search_fields = ['name', 'email_id']
    list_per_page = 20

@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone_no', 'amount', 'date_time']
    search_fields = ['name', 'phone_no']
    list_filter = ['date_time']
    date_hierarchy = 'date_time'
    readonly_fields = ['date_time']
    list_per_page = 25
```

### Data Migration (seed data)

Create a data migration that inserts the same seed data from `creating database.py`:
- 4 categories (C00=Cakes, B00=Beverages, K00=Cookies, P00=Pastries)
- 10 cakes, 10 pastries, 10 cookies, 10 beverages
- 1 admin user (`admin` / `987abc`)
- Employee and PersonalDetail sample entries (from `interaction.py` seed data)

### Superuser Creation

Create a Django management command `create_admin` or use `createsuperuser` to set up
an admin account with the same credentials as the old `admin` table.

### Migrate + Seed

```bash
python manage.py makemigrations        # Generate model migrations
python manage.py migrate               # Apply to SQLite
python manage.py createsuperuser       # Set up admin user
python manage.py loaddata seed.json    # Seed product data
```

### Commit

```
git add .
git commit -m "feat: add Django models and admin for all bakery entities

- Create 8 models: Category, Cake, Beverage, Cookie, Pastry,
  Employee, PersonalDetail, CustomerOrder
- Register all models in admin with search/filter/list_editable
- Add data migration with seed products matching original MySQL tables
- Set up superuser creation for manager access
- All existing database tables ported 1:1 to Django ORM
"
```

### Verification

```bash
python manage.py shell -c "
from bakery.models import *
print(f'Categories: {Category.objects.count()}')
print(f'Cakes: {Cake.objects.count()}')
print(f'Beverages: {Beverage.objects.count()}')
print(f'Cookies: {Cookie.objects.count()}')
print(f'Pastries: {Pastry.objects.count()}')
print(f'Employees: {Employee.objects.count()}')
"
# → All counts should match the seed data in creating database.py
```

---

## Milestone 2: Admin Panel (Replaces Manager.py + auth)

**Goal**: The Django admin replaces all 294 lines of `Manager.py` — login, CRUD,
search, filter, pagination, history — for free.

### What Manager.py Did → What Replaces It

| Manager.py feature | Django Admin equivalent |
|---|---|
| Login with ID/password | Built-in `django.contrib.auth` with bcrypt |
| View Records | `list_display` per model + search + filters |
| Insert Records | `+ Add` button per model |
| Update Records | Inline edit via `list_editable` or change form |
| Delete Records | Delete confirmation per record |
| View: beverages/cakes/cookies/employee/menu/pastries/personal_details | 7 admin register blocks |
| Logout | Built-in logout view |
| Hardcoded table allow-lists | Model permission system |

### Polish Admin UX

```python
# bakery/admin.py additions
admin.site.site_header = 'Crumbs Bakery Administration'
admin.site.site_title = 'Crumbs Admin'
admin.site.index_title = 'Manage Your Bakery'
```

### Custom Admin Permissions

- Create staff users via `createsuperuser`
- Use Django's permission groups if needed for read-only vs. edit access
- The old `admin` table's plaintext password is replaced by Django's `make_password`

### Commit

```
git add .
git commit -m "feat: replace Manager.py CRUD with Django admin panel

- Register all 8 models in admin with custom list/search/filter
- Style admin header for Crumbs branding
- Django's auth system replaces plaintext password login
- Admin panel covers: View, Insert, Update, Delete on all tables
- Remove Manager.py, no longer needed — admin does it all
"
```

### Verification

1. Start server: `python manage.py runserver`
2. Open `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials
4. Verify each model: list view, add form, edit form, delete flow
5. Verify search works on name columns
6. Verify filters work (department, price range, date)
7. Confirm logout works

---

## Milestone 3: Home Page + Product Browsing (Replaces home.py + menu)

**Goal**: Public-facing pages for the bakery — home page, menu browsing by category.

### URLs

```python
# bakery/urls.py
from django.urls import path
from . import views

app_name = 'bakery'
urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('category/<str:category_id>/', views.category_items, name='category_items'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-confirmed/<int:order_id>/', views.order_confirmed, name='order_confirmed'),
]
```

### Views

```python
# bakery/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Cake, Beverage, Cookie, Pastry, CustomerOrder

def home(request):
    """Landing page — formerly home.py with ASCII art"""
    return render(request, 'bakery/home.html')

def menu_view(request):
    """Category listing — formerly printmenu() in Customer.py"""
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'tidbits': [
            'Enjoy the best of baking with crumbs!',
            'Every flavour has a story to tell!',
            'Count the memories not the calories!',
            'We bet you will keep coming back!',
            'A wonderful gift for your loved ones!',
            'Celebrate with crumbs!',
        ],
        'niceday_messages': [
            'Hope you have a good day :)',
            'Stay hydrated :)',
            'Just in case no one has told you already... you are amazing :)',
            'Be a rainbow in someones storm :)',
            'Perfection is accepting your imperfections :)',
        ],
    }
    return render(request, 'bakery/menu.html', context)

def category_items(request, category_id):
    """Items within a category — replaces printcakes/printbeverages/printcookies/printpastries"""
    category = get_object_or_404(Category, pk=category_id)

    # Fetch items based on category
    items = []
    price_label = ''
    unit_label = ''
    if category_id == 'C00':
        items = Cake.objects.all()
        price_label = 'Price (per kg)'
        unit_label = 'kg'
    elif category_id == 'B00':
        items = Beverage.objects.all()
        price_label = 'Price (medium)'
        unit_label = 'size'
    elif category_id == 'K00':
        items = Cookie.objects.all()
        price_label = 'Price (per 500g)'
        unit_label = 'g'
    elif category_id == 'P00':
        items = Pastry.objects.all()
        price_label = 'Price (per piece)'
        unit_label = 'piece'

    context = {
        'category': category,
        'items': items,
        'price_label': price_label,
        'unit_label': unit_label,
    }
    return render(request, 'bakery/category_items.html', context)
```

### Templates

#### `base.html`
- Bootstrap 5 CDN (or Tailwind via CDN)
- Navbar with: Home | Menu | Cart | Admin
- Sidebar with random tidbit/niceday message (preserving original flavor)
- Content block
- Footer with "Crumbs Bakery"

#### `home.html`
- Brand header: "🍪 CRUMBS 🍪"
- ASCII art preserved as `<pre>` block
- Tagline: "EXPERIENCE THE BEST OF BAKING WITH CRUMBS!! WE'LL BAKE YOUR DAY :)"

#### `menu.html`
- Category cards (Cakes, Beverages, Cookies, Pastries)
- Click → category_items page
- Random tidbit shown at top (matches original Customer.py behavior)

#### `category_items.html`
- Items displayed as cards or a table
- "Add to Cart" button per item (uses Django session-based cart)
- "Back to Categories" link

### Cart Logic (Session-Based)

Add cart helper functions in `bakery/cart.py`:

```python
CART_SESSION_KEY = 'crumbs_cart'

def get_cart(request):
    return request.session.get(CART_SESSION_KEY, {})

def add_to_cart(request, item_id, category_id, name, price, quantity=1, weight=None, size=None):
    cart = request.session.get(CART_SESSION_KEY, {})
    key = f'{category_id}:{item_id}'
    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {
            'item_id': item_id,
            'category_id': category_id,
            'name': name,
            'price': float(price),
            'quantity': quantity,
            'weight': weight,
            'size': size,
        }
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

def remove_from_cart(request, key):
    cart = request.session.get(CART_SESSION_KEY, {})
    cart.pop(key, None)
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

def clear_cart(request):
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True
```

### Forms

Create `bakery/forms.py` for the customer details form (replaces the personal_details
form in Customer.py):

```python
from django import forms

class CustomerDetailsForm(forms.Form):
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Your name'}),
    )
    phone_no = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Phone number'}),
    )
    delivery_option = forms.ChoiceField(
        choices=[('no', 'No'), ('yes', 'Yes')],
        widget=forms.RadioSelect,
        label='Do you want home delivery?',
    )
    address = forms.CharField(
        max_length=70,
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3}),
    )
```

### Commit

```
git add .
git commit -m "feat: add customer-facing pages (home, menu, cart)

- Port home.py landing page to Django template with ASCII art
- Implement menu browsing by category (Cakes, Beverages, Cookies, Pastries)
- Implement session-based shopping cart with add/remove/clear
- Add CustomerDetailsForm for checkout data collection
- Create base template with Bootstrap 5 and navigation
- Preserve original tidbits/niceday random messages
- Set up URL routing: /, /menu/, /category/<id>/, /cart/
"
```

### Verification

1. Visit `http://127.0.0.1:8000/` — home page renders with ASCII art
2. Click "Menu" → category listing shows all 4 categories
3. Click a category → items display with names and prices
4. Click "Add to Cart" → item appears in cart
5. Visit `/cart/` → cart shows items with quantities and subtotal
6. Cart persists across page navigation (session-based)

---

## Milestone 4: Order Checkout Flow (Replaces Customer.py order flow)

**Goal**: Complete checkout flow — personal details → confirm → place order.

### Checkout View Logic

```python
# In views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomerDetailsForm
from .cart import get_cart, clear_cart, CartItem

def checkout_view(request):
    cart = get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('bakery:menu')

    form = CustomerDetailsForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Calculate totals
        subtotal = sum(item['quantity'] * item['price'] for item in cart.values())
        # Handle weight/size-based pricing for cakes and cookies...
        # Handle beverage size multipliers...

        taxes = subtotal * 0.18  # GST
        delivery_charge = 0
        if form.cleaned_data['delivery_option'] == 'yes':
            if subtotal + taxes > 500:
                delivery_charge = 50
            else:
                messages.info(request,
                    'Home delivery available for orders above ₹500 (after tax).')
                return render(request, 'bakery/checkout.html', {
                    'form': form,
                    'cart': cart,
                    'subtotal': subtotal,
                    'taxes': taxes,
                    'delivery_charge': delivery_charge,
                    'grand_total': subtotal + taxes + delivery_charge,
                    'delivery_not_eligible': True,
                })

        grand_total = subtotal + taxes + delivery_charge

        # Save order
        order = CustomerOrder.objects.create(
            name=form.cleaned_data['name'],
            phone_no=form.cleaned_data['phone_no'],
            address=(form.cleaned_data['address']
                     if form.cleaned_data['delivery_option'] == 'yes'
                     else '-'),
            amount=int(grand_total),
        )

        # Clear cart and redirect
        clear_cart(request)
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('bakery:order_confirmed', order_id=order.id)

    # GET: show checkout form
    subtotal = sum(item['quantity'] * item['price'] for item in cart.values())
    taxes = subtotal * 0.18
    context = {
        'form': form,
        'cart': cart,
        'subtotal': subtotal,
        'taxes': taxes,
        'delivery_charge': 50 if subtotal + taxes > 500 else 0,
        'grand_total': subtotal + taxes + (50 if subtotal + taxes > 500 else 0),
    }
    return render(request, 'bakery/checkout.html', context)

def order_confirmed(request, order_id):
    order = get_object_or_404(CustomerOrder, pk=order_id)
    return render(request, 'bakery/order_confirmed.html', {'order': order})
```

### Checkout Page Template

- Step 1: Customer details form (name, phone, delivery option, address)
- Step 2: Order summary (cart items, price breakdown)
- Step 3: Confirm & Place Order button

### Order Confirmed Page

- Success message
- Order number
- Balloons/celebration (🎉)
- "Place Another Order" link → `/menu/`

### Commit

```
git add .
git commit -m "feat: implement checkout flow with order placement

- Add checkout view with customer details form and order summary
- Implement price calculation: subtotal, 18% GST, delivery charge
- Delivery charge: ₹50 for orders above ₹500
- Order saved to CustomerOrder model (matching c_details table)
- Cart cleared on successful order placement
- Order confirmation page with celebration
- Preserve all original Customer.py pricing logic (weight/size multipliers)
"
```

### Verification

1. Add items to cart
2. Visit `/checkout/`
3. Fill in form (name, phone, delivery option)
4. Verify price breakdown: subtotal + GST (18%) = total
5. If home delivery & total > 500: delivery charge ₹50 added
6. Click "Place Order"
7. See confirmation page with order ID
8. Check `/admin/bakery/customerorder/` — order is saved
9. Cart is empty after order

---

## Milestone 5: Tests

**Goal**: Basic test coverage that proves the migration works correctly.

### Test Structure (`bakery/tests.py`)

```python
from django.test import TestCase
from django.urls import reverse
from bakery.models import Cake, Beverage, Cookie, Pastry, Category, CustomerOrder

class ModelTests(TestCase):
    """Test all models can be created and have correct string representations"""

    def setUp(self):
        Category.objects.create(id='C00', name='Cakes')
        Cake.objects.create(id='C01', name='Vanilla', price_1kg=1200)
        Beverage.objects.create(id='B01', name='Coffee', price_medium=150)
        Cookie.objects.create(id='K01', name='Peanut Butter', price_500g=1000)
        Pastry.objects.create(id='P01', name='Vanilla', price_per_piece=40)

    def test_cake_str(self):
        cake = Cake.objects.get(id='C01')
        self.assertIn('Vanilla', str(cake))
        self.assertIn('1200', str(cake))

    def test_category_str(self):
        cat = Category.objects.get(id='C00')
        self.assertEqual(str(cat), 'Cakes')

    def test_beverage_str(self):
        bev = Beverage.objects.get(id='B01')
        self.assertIn('Coffee', str(bev))

    # ... similar for Cookie, Pastry, CustomerOrder

class ViewTests(TestCase):
    """Test all public views return 200"""

    def test_home_page(self):
        response = self.client.get(reverse('bakery:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CRUMBS')

    def test_menu_page(self):
        response = self.client.get(reverse('bakery:menu'))
        self.assertEqual(response.status_code, 200)

    def test_cart_page(self):
        response = self.client.get(reverse('bakery:cart'))
        self.assertEqual(response.status_code, 200)

    def test_category_items(self):
        Category.objects.create(id='C00', name='Cakes')
        response = self.client.get(reverse('bakery:category_items', args=['C00']))
        self.assertEqual(response.status_code, 200)

class OrderFlowTests(TestCase):
    """Test the complete order flow end-to-end"""

    def test_empty_cart_checkout_redirect(self):
        response = self.client.get(reverse('bakery:checkout'))
        self.assertRedirects(response, reverse('bakery:menu'))

    def test_full_order_flow(self):
        # Add item to cart via session
        session = self.client.session
        session['crumbs_cart'] = {
            'C00:C01': {
                'item_id': 'C01', 'category_id': 'C00',
                'name': 'Vanilla', 'price': 1200.0,
                'quantity': 1, 'weight': 0.5, 'size': None,
            }
        }
        session.save()

        # Submit checkout form
        response = self.client.post(reverse('bakery:checkout'), {
            'name': 'Test User',
            'phone_no': 9876543210,
            'delivery_option': 'no',
            'address': '',
        })
        self.assertEqual(response.status_code, 302)  # redirect after success

        # Verify order was created
        self.assertEqual(CustomerOrder.objects.count(), 1)
        order = CustomerOrder.objects.first()
        self.assertEqual(order.name, 'test user')  # lowercased like original

class AdminTests(TestCase):
    """Test admin panel access"""

    def test_admin_login_required(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # redirect to login
```

### Run Tests

```bash
python manage.py test bakery -v 2
```

### Commit

```
git add .
git commit -m "test: add test suite for models, views, and order flow

- Add ModelTests: verify str() methods for all 5 product models
- Add ViewTests: home, menu, cart, category_items return 200
- Add OrderFlowTests: empty cart redirect, end-to-end order placement
- Add AdminTests: verify admin login protection
- All tests passing with SQLite in-memory test database
"
```

### Verification

```bash
python manage.py test bakery -v 2
# → Ran X tests — all passed
```

---

## Milestone 6: Polish + Deployment Readiness (Optional / Stretch)

**Goal**: Production-ready Docker setup, environment separation, and one-command deploy.

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install gunicorn && pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "crumbs_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: crumbs
      POSTGRES_USER: crumbs
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      DJANGO_DB_URL: postgres://crumbs:${DB_PASSWORD}@db:5432/crumbs
    depends_on:
      - db
volumes:
  pgdata:
```

### Environment Separation

- `settings/dev.py` — SQLite, debug=True
- `settings/prod.py` — PostgreSQL, debug=False, sentry, whitenoise
- `DJANGO_SETTINGS_MODULE` env var switches between them

### Commit

```
git add .
git commit -m "chore: add Docker and production configuration

- Add Dockerfile with gunicorn for production serving
- Add docker-compose.yml with PostgreSQL backend
- Split settings into dev/prod profiles
- Add whitenoise for static file serving in production
- Environment variables via .env for secret management
"
```

---

## Full File Tree After Migration

```
Crumbs/
├── .env                          # Gitignored — secrets
├── .gitignore
├── AGENTS.md                     # Updated for Django
├── README.md
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── crumbs_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── bakery/
│   ├── __init__.py
│   ├── admin.py                  # All model admin registrations
│   ├── apps.py
│   ├── cart.py                   # Session-based cart helpers
│   ├── forms.py                  # Customer details form
│   ├── models.py                 # All 8 models
│   ├── tests.py                  # Model + view + flow tests
│   ├── urls.py
│   ├── views.py
│   ├── templatetags/
│   │   └── __init__.py
│   └── templates/
│       └── bakery/
│           ├── base.html
│           ├── home.html
│           ├── menu.html
│           ├── category_items.html
│           ├── cart.html
│           ├── checkout.html
│           └── order_confirmed.html
└── static/
    └── bakery/
        ├── css/
        │   └── style.css
        └── js/
            └── main.js
```

---

## Deletion Manifest

The following old files are removed during the migration (Milestone 0):

| File | Reason |
|---|---|
| `main.py` | Replaced by Django URL routing + views |
| `Customer.py` | Replaced by bakery views + forms |
| `Manager.py` | Replaced by Django admin |
| `home.py` | Replaced by home.html template |
| `interaction.py` | Legacy CLI, no longer needed |
| `creating database.py` | Replaced by Django migrations |
| `creds.py` | Replaced by `.env` + `settings.py` |
| `__pycache__/` | Build artifact, gitignored |

---

## Summary of Gains After Migration

| Area | Streamlit (Before) | Django (After) |
|---|---|---|
| **Manager CRUD** | 294 lines custom code | Zero lines — built-in admin |
| **Auth** | Plaintext in DB, 20-char max | bcrypt, sessions, CSRF |
| **Database** | Raw MySQL with partial injection risk | ORM with parameterized queries |
| **State** | `st.session_state` (lost on refresh) | Server-side sessions |
| **URLs** | State-machine (`st.session_state.view`) | Named URL patterns |
| **Tests** | Zero | 10+ tests covering models, views, flow |
| **API** | Impossible | Add DRF/Ninja in one afternoon |
| **Deploy** | `streamlit run main.py` (single process) | Gunicorn + Nginx/Docker |
| **Schema** | Manual script | Versioned migrations |
| **Code** | ~4000 lines across 6 modules | ~500 lines Django code + templates |
