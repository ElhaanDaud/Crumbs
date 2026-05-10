from django.contrib import admin
from .models import (
    Category, Cake, Beverage, Cookie, Pastry,
    Employee, PersonalDetail, CustomerOrder,
)


admin.site.site_header = 'Crumbs Bakery Administration'
admin.site.site_title = 'Crumbs Admin'
admin.site.index_title = 'Manage Your Bakery'


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
