from django.contrib import admin
from . import models

class VendorAdmin(admin.ModelAdmin):
    list_display=['username', 'address', 'mobile']
    def username(self, obj):
        return obj.user.username
admin.site.register(models.Vendor, VendorAdmin)
admin.site.register(models.MainCategory)
admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.Brand)
# admin.site.register(models.Product)
# admin.site.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['username', 'mobile']
    def username(self, obj):
        return obj.user.username
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.CustomerAddress)
admin.site.register(models.ProductRating)
# Product Image
admin.site.register(models.ProductImage)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)

class ProductImagesInline(admin.StackedInline):
    model = models.ProductImage

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    inlines = [
        ProductImagesInline,
    ]

admin.site.register(models.Product, ProductAdmin)
