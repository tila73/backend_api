from rest_framework import serializers
from . import models

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Vendor
        fields=['id', 'user','address']

    def __init__(self, *args, **kwargs):
        super(VendorSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Vendor
        fields=['id', 'user','address']

    def __init__(self, *args, **kwargs):
        super(VendorDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class ProductListSerializer(serializers.ModelSerializer):
    product_ratings=serializers.StringRelatedField(many=True, read_only=True)
    brand_name = serializers.CharField(source='brand.name')
    class Meta:
        model=models.Product
        fields=['id', 'category', 'brand', 'brand_name', 'vendor', 'title', 'slug', 'detail', 'price', 'product_ratings', 'image']

    def __init__(self, *args, **kwargs):
        super(ProductListSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['id', 'product', 'image']

class ProductDetailSerializer(serializers.ModelSerializer):
    product_ratings=serializers.StringRelatedField(many=True, read_only=True)
    product_images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        many=True
        model=models.Product
        fields=['id', 'category', 'brand', 'vendor', 'title', 'slug', 'detail', 'price', 'product_ratings', 'product_images']

    def __init__(self, *args, **kwargs):
        super(ProductDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Customer
        fields=['id', 'user', 'mobile']

    def __init__(self, *args, **kwargs):
        super(CustomerSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Customer
        fields=['id', 'user', 'mobile']

    def __init__(self, *args, **kwargs):
        super(CustomerDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Order
        fields=['id', 'customer']

    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.OrderItem
        fields=['id', 'order', 'product']

    def __init__(self, *args, **kwargs):
        super(OrderDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CustomerAddress
        fields=['id', 'customer', 'address', 'default_address']

    def __init__(self, *args, **kwargs):
        super(CustomerAddressSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductRating
        fields=['id', 'customer', 'product', 'rating', 'reviews', 'add_time']

    def __init__(self, *args, **kwargs):
        super(ProductRatingSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Sub Category
# class SubCategorySerializer(serializers.ModelSerializer):
#     subcategory_product = ProductListSerializer(many=True, read_only=True)
#     class Meta:
#         model = models.SubCategory
#         fields = '__all__'
# class SubCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.SubCategory
#         fields = ('id', 'name', 'image', 'slug')

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.SubCategory
        fields=['id', 'category', 'name', 'image', 'slug']

    def __init__(self, *args, **kwargs):
        super(SubCategorySerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# class SubCategoryDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.SubCategory
#         fields=['id', 'category', 'name', 'image', 'slug']

#     def __init__(self, *args, **kwargs):
#         super(SubCategoryDetailSerializer, self).__init__(*args, **kwargs)
#         self.Meta.depth = 1

# Category
# class CategorySerializer(serializers.ModelSerializer):
#     sub_categories = SubCategorySerializer(many=True, read_only=True)
#     class Meta:
#         model=models.Category
#         fields = '__all__'
#         # fields = ('id', 'name', 'slug', 'sub_categories')

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.Category
#         fields=['id', 'main_category', 'name', 'slug']

#     def __init__(self, *args, **kwargs):
#         super(CategorySerializer, self).__init__(*args, **kwargs)
#         self.Meta.depth = 1

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model=models.Category
        fields=['id', 'main_category', 'name', 'slug', 'subcategories']

    def get_subcategories(self, obj):
        show_subcategories = self.context.get('show_subcategories', False)
        if not show_subcategories:
            return None

        subcategories = models.SubCategory.objects.filter(category=obj)
        serializer = SubCategorySerializer(instance=subcategories, many=True)
        return serializer.data


# class CategoryDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.Category
#         fields=['id', 'main_category', 'name', 'slug']

#     def __init__(self, *args, **kwargs):
#         super(CategoryDetailSerializer, self).__init__(*args, **kwargs)
#         self.Meta.depth = 1

# Main Category
# class MainCategorySerializer(serializers.ModelSerializer):
#     categories = CategorySerializer(many=True, read_only=True)
#     class Meta:
#         model = models.MainCategory
#         fields = '__all__'
#         # fields = ('id', 'name', 'image', 'slug', 'categories')

class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MainCategory
        fields = ['id', 'name', 'image', 'slug']

    def __init__(self, *args, **kwargs):
        super(MainCategorySerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class MainCategoryDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = models.MainCategory
        fields = ['id', 'name', 'image', 'slug', 'categories']

# class MainCategoryDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.MainCategory
#         fields=['id', 'name', 'image', 'slug']

#     def __init__(self, *args, **kwargs):
#         super(MainCategoryDetailSerializer, self).__init__(*args, **kwargs)
#         self.Meta.depth = 1

# Brand
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Brand
        fields=['id', 'name', 'image', 'slug']

    def __init__(self, *args, **kwargs):
        super(BrandSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Brand
        fields=['id', 'name', 'image', 'slug']

    def __init__(self, *args, **kwargs):
        super(BrandDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1