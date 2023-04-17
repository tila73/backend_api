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

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['id', 'product', 'image']

class ProductCreateSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = models.Product
        fields=['id', 'main_category', 'category', 'subcategory', 'brand', 'vendor', 'title', 'slug', 'detail', 'price', 'image', 'quantity', 'product_images']

    def create(self, validated_data):
        product_images_data = validated_data.pop('product_images', [])
        product = models.Product.objects.create(**validated_data)
        for image_data in product_images_data:
            models.ProductImage.objects.create(product=product, **image_data)
        return product
    
class ProductListSerializer(serializers.ModelSerializer):
    product_ratings=serializers.StringRelatedField(many=True, read_only=True)
    brand_name = serializers.CharField(source='brand.name')
    class Meta:
        model=models.Product
        fields=['id', 'main_category', 'category', 'subcategory', 'brand', 'brand_name', 'vendor', 'title', 'slug', 'detail', 'price', 'product_ratings', 'image', 'quantity']

    def __init__(self, *args, **kwargs):
        super(ProductListSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1
        
class ProductDetailSerializer(serializers.ModelSerializer):
    product_ratings=serializers.StringRelatedField(many=True, read_only=True)
    product_images = ProductImageSerializer(many=True, read_only=True)
    main_category_name = serializers.CharField(source='category.main_category.name')

    class Meta:
        many=True
        model=models.Product
        fields=['id', 'category', 'subcategory', 'main_category_name', 'brand', 'vendor', 'title', 'slug', 'detail', 'price', 'quantity', 'product_ratings', 'image', 'product_images']

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

    # def __init__(self, *args, **kwargs):
    #     super(OrderSerializer, self).__init__(*args, **kwargs)
    #     self.Meta.depth = 1

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
        fields=['id', 'customer', 'street_address', 'city', 'province', 'zip', 'default_address']

    # def __init__(self, *args, **kwargs):
    #     super(CustomerAddressSerializer, self).__init__(*args, **kwargs)
    #     self.Meta.depth = 1

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductRating
        fields=['id', 'customer', 'product', 'rating', 'reviews', 'add_time']

    def __init__(self, *args, **kwargs):
        super(ProductRatingSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1

# Sub Category
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubCategory
        fields = ['id', 'name', 'image', 'slug']

# Sub Category Detail
class SubCategoryDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    main_category_name = serializers.CharField(source='category.main_category.name')
    products = serializers.SerializerMethodField()
    class Meta:
        model=models.SubCategory
        fields=['id', 'name', 'image', 'slug', 'category', 'category_name', 'main_category_name', 'products']

    def get_products(self, obj):
        products = obj.product_set.all()
        return ProductListSerializer(products, many=True).data

    # def __init__(self, *args, **kwargs):
    #     super(SubCategorySerializer, self).__init__(*args, **kwargs)
    #     self.Meta.depth = 1

# Category
class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'slug', 'subcategories']

# Category Detail    
class CategoryDetailSerializer(serializers.ModelSerializer):
    main_category_name = serializers.CharField(source='main_category.name')
    subcategories = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        # fields = ('id', 'name', 'slug', 'subcategories', 'products')
        fields = ('id', 'name', 'slug', 'main_category', 'main_category_name', 'subcategories', 'products')

    def get_subcategories(self, instance):
        subcategories = instance.subcategories.all()
        serializer = SubCategoryDetailSerializer(subcategories, many=True)
        return serializer.data

    def get_products(self, obj):
        products = obj.product_set.all()
        return ProductListSerializer(products, many=True).data


# Main Category
class MainCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = models.MainCategory
        fields = ['id', 'name', 'image', 'slug', 'categories']

    def __init__(self, *args, **kwargs):
        super(MainCategorySerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1
class MainCategoryDetailSerializer(serializers.ModelSerializer):
    categories = CategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = models.MainCategory
        fields = ['id', 'name', 'image', 'slug', 'categories']

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

class VendorDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ["total_vendor_products"]

class CustomerDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ["total_customer_addresses"]

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    
    class Meta:
        model = models.Cart
        fields = ['items']

    def create(self, validated_data):
        cart_customer = validated_data.pop('customer')
        items_data = validated_data.pop('items')
        cart = models.Cart.objects.create(customer=cart_customer, **validated_data)
        for item_data in items_data:
            models.CartItem.objects.create(cart=cart, **item_data)
        return cart
    
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = ['id', 'full_name', 'email', 'message']
class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FAQ
        fields = ['id', 'question', 'answer']
    
