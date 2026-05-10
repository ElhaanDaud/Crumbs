from django.test import TestCase
from django.urls import reverse
from bakery.models import (
    Category, Cake, Beverage, Cookie, Pastry,
    Employee, PersonalDetail, CustomerOrder,
)


class ModelTests(TestCase):
    def setUp(self):
        Category.objects.create(id='X00', name='TestCategory')
        Cake.objects.create(id='X01', name='TestCake', price_1kg=999)
        Beverage.objects.create(id='X01', name='TestBev', price_medium=99)
        Cookie.objects.create(id='X01', name='TestCookie', price_500g=555)
        Pastry.objects.create(id='X01', name='TestPastry', price_per_piece=15)
        Employee.objects.create(id='X01', name='TestEmp', salary=25000, department='Test')
        PersonalDetail.objects.create(id='X01', name='TestEmp', phone_no=1111111111, email_id='test@example.com')

    def test_category_str(self):
        cat = Category.objects.get(id='X00')
        self.assertEqual(str(cat), 'TestCategory')

    def test_category_meta(self):
        self.assertEqual(Category._meta.verbose_name_plural, 'categories')

    def test_cake_str(self):
        cake = Cake.objects.get(id='X01')
        self.assertIn('TestCake', str(cake))
        self.assertIn('999', str(cake))

    def test_beverage_str(self):
        bev = Beverage.objects.get(id='X01')
        self.assertIn('TestBev', str(bev))

    def test_beverage_meta(self):
        self.assertEqual(Beverage._meta.verbose_name_plural, 'beverages')

    def test_cookie_str(self):
        cookie = Cookie.objects.get(id='X01')
        self.assertIn('TestCookie', str(cookie))

    def test_cookie_meta(self):
        self.assertEqual(Cookie._meta.verbose_name_plural, 'cookies')

    def test_pastry_str(self):
        pastry = Pastry.objects.get(id='X01')
        self.assertIn('TestPastry', str(pastry))

    def test_pastry_meta(self):
        self.assertEqual(Pastry._meta.verbose_name_plural, 'pastries')

    def test_employee_str(self):
        emp = Employee.objects.get(id='X01')
        self.assertIn('TestEmp', str(emp))
        self.assertIn('Test', str(emp))

    def test_personal_detail_str(self):
        pd = PersonalDetail.objects.get(id='X01')
        self.assertIn('test@example.com', str(pd))

    def test_customer_order_str(self):
        order = CustomerOrder.objects.create(name='Tester', phone_no=1234567890, amount=500)
        self.assertIn('Tester', str(order))
        self.assertIn('500', str(order))

    def test_customer_order_defaults(self):
        order = CustomerOrder.objects.create(name='Tester', phone_no=1234567890)
        self.assertEqual(order.address, '-')
        self.assertIsNone(order.amount)

    def test_customer_order_ordering(self):
        CustomerOrder.objects.create(name='First', phone_no=1, amount=100)
        CustomerOrder.objects.create(name='Second', phone_no=2, amount=200)
        orders = CustomerOrder.objects.all()
        self.assertEqual(orders[0].name, 'Second')

    def test_cake_min_price_validator(self):
        from django.core.exceptions import ValidationError
        try:
            cake = Cake(id='X99', name='Free', price_1kg=0)
            cake.full_clean()
            self.fail('Should have raised ValidationError')
        except ValidationError:
            pass


class ViewTests(TestCase):
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

    def test_category_items_with_seed_data(self):
        response = self.client.get(reverse('bakery:category_items', args=['C00']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cakes')

    def test_category_items_not_found(self):
        response = self.client.get(reverse('bakery:category_items', args=['XXX']))
        self.assertEqual(response.status_code, 404)

    def test_checkout_page_empty_cart_redirect(self):
        response = self.client.get(reverse('bakery:checkout'))
        self.assertRedirects(response, reverse('bakery:menu'))

    def test_add_to_cart_cakes(self):
        response = self.client.get(reverse('bakery:add_to_cart', args=['C00', 'C01']))
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get('crumbs_cart', {})
        self.assertIn('C00:C01', cart)
        self.assertEqual(cart['C00:C01']['name'], 'Vanilla')

    def test_remove_from_cart(self):
        self.client.get(reverse('bakery:add_to_cart', args=['C00', 'C01']))
        response = self.client.get(reverse('bakery:remove_from_cart', args=['C00:C01']))
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get('crumbs_cart', {})
        self.assertNotIn('C00:C01', cart)

    def test_checkout_page_with_cart(self):
        self.client.get(reverse('bakery:add_to_cart', args=['C00', 'C01']))
        response = self.client.get(reverse('bakery:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vanilla')

    def test_category_items_beverages(self):
        response = self.client.get(reverse('bakery:category_items', args=['B00']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beverages')

    def test_category_items_cookies(self):
        response = self.client.get(reverse('bakery:category_items', args=['K00']))
        self.assertEqual(response.status_code, 200)

    def test_category_items_pastries(self):
        response = self.client.get(reverse('bakery:category_items', args=['P00']))
        self.assertEqual(response.status_code, 200)


class OrderFlowTests(TestCase):
    def test_full_order_flow_no_delivery(self):
        self.client.get(reverse('bakery:add_to_cart', args=['C00', 'C01']))
        response = self.client.post(reverse('bakery:checkout'), {
            'name': 'Test User',
            'phone_no': 9876543210,
            'delivery_option': 'no',
            'address': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomerOrder.objects.count(), 1)
        order = CustomerOrder.objects.first()
        self.assertEqual(order.name, 'Test User')
        cart = self.client.session.get('crumbs_cart', {})
        self.assertEqual(cart, {})

    def test_full_order_flow_with_delivery(self):
        self.client.get(reverse('bakery:add_to_cart', args=['C00', 'C01']))
        response = self.client.post(reverse('bakery:checkout'), {
            'name': 'Delivery User',
            'phone_no': 9876543211,
            'delivery_option': 'yes',
            'address': '123 Test St',
        })
        self.assertIn(response.status_code, [200, 302])
        if response.status_code == 302:
            order = CustomerOrder.objects.first()
            self.assertIsNotNone(order)
            self.assertEqual(order.address, '123 Test St')

    def test_delivery_not_eligible(self):
        self.client.get(reverse('bakery:add_to_cart', args=['B00', 'B01']))
        response = self.client.post(reverse('bakery:checkout'), {
            'name': 'Low Order',
            'phone_no': 9876543212,
            'delivery_option': 'yes',
            'address': '456 Low St',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home delivery available for orders above')

    def test_multiple_items_order(self):
        self.client.get(reverse('bakery:add_to_cart', args=['C00', 'C01']))
        self.client.get(reverse('bakery:add_to_cart', args=['C00', 'C02']))
        self.client.get(reverse('bakery:add_to_cart', args=['C00', 'C02']))
        response = self.client.post(reverse('bakery:checkout'), {
            'name': 'Multi Buyer',
            'phone_no': 9876543213,
            'delivery_option': 'no',
            'address': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomerOrder.objects.count(), 1)
        order = CustomerOrder.objects.first()
        self.assertIsNotNone(order.amount)
        cart = self.client.session.get('crumbs_cart', {})
        self.assertEqual(cart, {})


class AdminTests(TestCase):
    def test_admin_login_required(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_admin_login_page(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)
