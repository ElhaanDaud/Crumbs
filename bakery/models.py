from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['id']

    def __str__(self):
        return self.name


class Cake(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    price_1kg = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} — ₹{self.price_1kg}/kg'


class Beverage(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    price_medium = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name_plural = 'beverages'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} — ₹{self.price_medium}/med'


class Cookie(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    price_500g = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name_plural = 'cookies'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} — ₹{self.price_500g}/500g'


class Pastry(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
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
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    phone_no = models.BigIntegerField()
    email_id = models.EmailField(max_length=40)

    def __str__(self):
        return f'{self.name} — {self.email_id}'


class CustomerOrder(models.Model):
    name = models.CharField(max_length=30)
    phone_no = models.BigIntegerField()
    address = models.CharField(max_length=70, blank=True, default='-')
    amount = models.PositiveIntegerField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return f'Order #{self.id} — {self.name} — ₹{self.amount}'
