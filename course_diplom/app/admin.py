from django.contrib import admin
from .models import Category, CustomUser, Item, Order, ItemInfo, OrderInfo, Shop, Parameter, ItemParameter, Contact


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk',)
    pass

class ContactAdmin(admin.ModelAdmin):
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
    pass

class OrderInfoAdmin(admin.ModelAdmin):
    pass

## модель through, которую django создаёт автоматом для m2m связей.
class ContactsInfoInline(admin.TabularInline):
    model = Contact.user.through

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'pk', 'type', 'first_name', 'last_name', 'middle_name', 'company', 'position', )
    inlines = [ContactsInfoInline]

class ContactAdmin(admin.ModelAdmin):
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
admin.site.register(Contact, ContactAdmin)