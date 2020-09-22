from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

class ProductImageAdmin(admin.StackedInline):
    model=ProductImage

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    inlines = [ProductImageAdmin]

    list_display = ('title','price','quantity', 'is_hide', 'category','creator','created')
    search_fields = ('category','title','creator')
    list_filter = ["creator", "created", "category"]

    class Meta:
        model=Product

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    list_display = ('transaction_id','date_ordered','customer', 'complete')
    search_fields = ('customer','title','transaction_id')
    list_filter = ["date_ordered", "transaction_id"]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','product','quantity', 'date_added')
    search_fields = ('product','order')
    list_filter = ["order", "date_added"]

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('order','customer','address', 'tel','city','date_added')
    search_fields = ('city','order')
    list_filter = ["order", "city"]

class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'message')
    list_filter = ["email"]

admin.site.register(Category)
admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress,ShippingAddressAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.unregister(Review)
admin.site.register(Review, ReviewAdmin)
