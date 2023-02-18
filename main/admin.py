from django.contrib import admin
from . import models

admin.site.register(models.Vendor)
admin.site.register(models.MainCategory)
admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.Brand)
# admin.site.register(models.Product)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.CustomerAddress)
admin.site.register(models.ProductRating)
# Product Image
admin.site.register(models.ProductImage)

class ProductImagesInline(admin.StackedInline):
    model = models.ProductImage

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    inlines = [
        ProductImagesInline,
    ]

admin.site.register(models.Product, ProductAdmin)
