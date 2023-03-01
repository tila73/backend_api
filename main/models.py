from django.db import models
from django.contrib.auth.models import User

# Vendor Model
class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(null=True)

    def __str__(self):
        return self.user.username

# Product Category
# class ProductCategory(models.Model):
#     title=models.CharField(max_length=200)
#     detail=models.TextField(null=True)

#     def __str__(self):
#         return self.title

# Main Category
class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='main_category_images/', null=True)
    slug = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name

# Category
class Category(models.Model):
    # main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.main_category.name + " -- " + self.name 

# Sub Category
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sub_category_images/', null=True)
    slug = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.category.main_category.name + " -- " + self.category.name + " -- " + self.name

# Brands
class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brand_images/', null=True)
    slug = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name

# Product
class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    subcategory=models.ForeignKey(SubCategory, on_delete=models.SET_NULL,null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    vendor=models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    title=models.CharField(max_length=250)
    slug=models.CharField(max_length=250, unique=True, null=True)
    detail=models.TextField(null=True)
    price=models.FloatField()
    image=models.ImageField(upload_to='product_images/', null=True)

    def __str__(self):
        return self.title

# Product Images Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/', null=True)

    def __str__(self):
        return self.image.url

# Customer Model
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.PositiveBigIntegerField(unique=True)

    def __str__(self):
        return self.user.username

# Order Model
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return '%s' % (self.order_time)
        return self.customer.user.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title

# Customer Address Model
class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_addresses')
    address = models.TextField()
    default_address = models.BooleanField(default=False)

    def __str__(self):
        return self.address 

# Product Ratings and Reviews
class ProductRating(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='rating_customers')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    rating=models.IntegerField()
    reviews=models.TextField()
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating} - {self.reviews}'

# Cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum([item.total_price() for item in self.items.all()])

# Cart item
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.product.price * self.quantity

# Payment
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user} for order {self.order} of amount {self.amount}"

