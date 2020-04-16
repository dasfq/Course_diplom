from django.contrib import admin
from .models import Category, CustomUser, Item, Order, ItemInfo, OrderInfo, Shop, Parameter, ItemParameter


class CategoryAdmin(admin.ModelAdmin):
    pass

class ShopAdmin(admin.ModelAdmin):
    pass

class ParameterAdmin(admin.ModelAdmin):
    pass

class ItemParameterAdmin(admin.ModelAdmin):
    pass

class ItemAdmin(admin.ModelAdmin):
    pass

class ItemInfoAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    # list_display = ("date", 'user')
    # inlines = ["date", 'user', 'item']
    pass

class OrderInfoAdmin(admin.ModelAdmin):
    pass

class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(ItemInfo, ItemInfoAdmin)
admin.site.register(ItemParameter, ItemParameterAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
