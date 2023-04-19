from django.contrib import admin
from . import models
from django.utils.html import format_html

class VendorAdmin(admin.ModelAdmin):
    list_display=['username', 'address', 'mobile']
    def username(self, obj):
        return obj.user.username
admin.site.register(models.Vendor, VendorAdmin)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display=['name', 'display_image', 'slug']

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" />'.format(obj.image.url))

    display_image.allow_tags = True
    display_image.short_description = 'Image'
admin.site.register(models.MainCategory, MainCategoryAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=['main_category', 'name', 'slug']
    def name(self, obj):
        return obj.name
admin.site.register(models.Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display=['category', 'name', 'display_image', 'slug']

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" />'.format(obj.image.url))

    display_image.allow_tags = True
    display_image.short_description = 'Image'
admin.site.register(models.SubCategory, SubCategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display=['name', 'display_image', 'slug']

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" />'.format(obj.image.url))

    display_image.allow_tags = True
    display_image.short_description = 'Image'
admin.site.register(models.Brand, BrandAdmin)
# admin.site.register(models.Product)
# admin.site.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['username', 'mobile']
    def username(self, obj):
        return obj.user.username
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
# admin.site.register(models.CustomerAddress)
# admin.site.register(models.ProductRating)
# Product Image
admin.site.register(models.ProductImage)
# admin.site.register(models.Cart)
# admin.site.register(models.CartItem)
class ContactAdmin(admin.ModelAdmin):
    list_display=['full_name', 'email', 'message', 'add_time']
    def message(self, obj):
        return obj.message
admin.site.register(models.Contact, ContactAdmin)
class FAQAdmin(admin.ModelAdmin):
    list_display=['question', 'answer']
admin.site.register(models.FAQ, FAQAdmin)

class ProductImagesInline(admin.StackedInline):
    model = models.ProductImage

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    inlines = [
        ProductImagesInline,
    ]

admin.site.register(models.Product, ProductAdmin)
