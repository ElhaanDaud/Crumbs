from django.db import migrations


def seed_data(apps, schema_editor):
    Category = apps.get_model('bakery', 'Category')
    Cake = apps.get_model('bakery', 'Cake')
    Beverage = apps.get_model('bakery', 'Beverage')
    Cookie = apps.get_model('bakery', 'Cookie')
    Pastry = apps.get_model('bakery', 'Pastry')
    Employee = apps.get_model('bakery', 'Employee')
    PersonalDetail = apps.get_model('bakery', 'PersonalDetail')

    # Categories
    Category.objects.bulk_create([
        Category(id='C00', name='Cakes'),
        Category(id='P00', name='Pastries'),
        Category(id='K00', name='Cookies'),
        Category(id='B00', name='Beverages'),
    ])

    # Cakes
    Cake.objects.bulk_create([
        Cake(id='C01', name='Vanilla', price_1kg=1200),
        Cake(id='C02', name='Pineapple', price_1kg=1200),
        Cake(id='C03', name='Strawberry', price_1kg=1280),
        Cake(id='C04', name='Blueberry', price_1kg=1280),
        Cake(id='C05', name='Choco Delight', price_1kg=1280),
        Cake(id='C06', name='Black Forest', price_1kg=1480),
        Cake(id='C07', name='Cheesecake', price_1kg=1680),
        Cake(id='C08', name='Butter Scotch', price_1kg=1800),
        Cake(id='C09', name='Piramys', price_1kg=1800),
        Cake(id='C10', name='Red Velvet', price_1kg=2000),
    ])

    # Beverages
    Beverage.objects.bulk_create([
        Beverage(id='B01', name='Apple Juice', price_medium=50),
        Beverage(id='B02', name='Banana Milk', price_medium=50),
        Beverage(id='B03', name='Citrus Peach', price_medium=70),
        Beverage(id='B04', name='Mango Rush', price_medium=70),
        Beverage(id='B05', name='Choco Shake', price_medium=70),
        Beverage(id='B06', name='Espresso', price_medium=120),
        Beverage(id='B07', name='Americano', price_medium=120),
        Beverage(id='B08', name='Cold Coffee', price_medium=120),
        Beverage(id='B09', name='Cafe Mocha', price_medium=150),
        Beverage(id='B10', name='Cappucino', price_medium=150),
    ])

    # Cookies
    Cookie.objects.bulk_create([
        Cookie(id='K01', name='Peanut Butter', price_500g=1000),
        Cookie(id='K02', name='Oatmeal', price_500g=1000),
        Cookie(id='K03', name='Raisin', price_500g=1250),
        Cookie(id='K04', name='Toffee Pecan', price_500g=1250),
        Cookie(id='K05', name='Almond Butter', price_500g=1250),
        Cookie(id='K06', name='Fudge Walnut', price_500g=1500),
        Cookie(id='K07', name='Macadamia', price_500g=1500),
        Cookie(id='K08', name='Chocolate', price_500g=1500),
        Cookie(id='K09', name='Walnut', price_500g=1500),
        Cookie(id='K10', name='White Choco', price_500g=2000),
    ])

    # Pastries
    Pastry.objects.bulk_create([
        Pastry(id='P01', name='Vanilla', price_per_piece=40),
        Pastry(id='P02', name='Chocolate', price_per_piece=40),
        Pastry(id='P03', name='Pineapple', price_per_piece=40),
        Pastry(id='P04', name='Strawberry', price_per_piece=40),
        Pastry(id='P05', name='Blueberry', price_per_piece=40),
        Pastry(id='P06', name='Mango Crush', price_per_piece=40),
        Pastry(id='P07', name='Guava Love', price_per_piece=40),
        Pastry(id='P08', name='Litchi', price_per_piece=40),
        Pastry(id='P09', name='Butter Scotch', price_per_piece=50),
        Pastry(id='P10', name='Chocochip', price_per_piece=50),
    ])

    # Employees (from interaction.py seed data)
    Employee.objects.bulk_create([
        Employee(id='E01', name='John', salary=30000, department='Sales'),
        Employee(id='E02', name='Jane', salary=35000, department='Kitchen'),
        Employee(id='E03', name='Mike', salary=32000, department='Delivery'),
        Employee(id='E04', name='Sarah', salary=38000, department='Management'),
        Employee(id='E05', name='David', salary=28000, department='Sales'),
    ])

    # Personal details (from interaction.py seed data)
    PersonalDetail.objects.bulk_create([
        PersonalDetail(id='E01', name='John', phone_no=9876543210, email_id='john@crumbs.com'),
        PersonalDetail(id='E02', name='Jane', phone_no=9876543211, email_id='jane@crumbs.com'),
        PersonalDetail(id='E03', name='Mike', phone_no=9876543212, email_id='mike@crumbs.com'),
        PersonalDetail(id='E04', name='Sarah', phone_no=9876543213, email_id='sarah@crumbs.com'),
        PersonalDetail(id='E05', name='David', phone_no=9876543214, email_id='david@crumbs.com'),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
