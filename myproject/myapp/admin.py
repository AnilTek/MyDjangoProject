from django.contrib import admin
from .models import CustomUser, Product, LoanModel, Product_Category, CarModel

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category")

class UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'gender', 'username')

class LoanModelAdmin(admin.ModelAdmin):
    list_display = ('cibil_score', 'anual_income', 'bank_asset_value')

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('model', 'year', 'millage')

admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Product_Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(CustomUser, UsersAdmin)
admin.site.register(LoanModel, LoanModelAdmin)


