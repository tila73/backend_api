from django.db import models
from django.contrib.auth.models import User
# import markdown
# import bleach
from ckeditor.fields import RichTextField
from django.core.mail import send_mail

# Vendor Model
class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.TextField(null=True)
    mobile = models.PositiveBigIntegerField(unique=True, null=True)

    def __str__(self):
        return self.user.username
    
    # Total Vendor Products
    def total_vendor_products(self):
        total_products = Product.objects.filter(vendor=self).count()
        return total_products
    
# class Vendor(models.Model):
#     full_name=models.CharField(max_length=150, null=True)
#     email=models.CharField(max_length=150, null=True)
#     address=models.CharField(max_length=200, null=True)
#     mobile=models.CharField(max_length=20, null=True)
#     password=models.CharField(max_length=100, null=True)

#     def __str__(self):
#         return self.full_name

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
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL,null=True)
    category=models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    subcategory=models.ForeignKey(SubCategory, on_delete=models.SET_NULL,null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    vendor=models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    title=models.CharField(max_length=250)
    slug=models.CharField(max_length=250, unique=True, null=True)
    detail=RichTextField(null=True)
    price=models.FloatField()
    image=models.ImageField(upload_to='product_images/', null=True)
    quantity = models.IntegerField(null=True)

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
    cart = models.ForeignKey('Cart', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    # Total Customer Products
    def total_customer_addresses(self):
        total_addresses = CustomerAddress.objects.filter(customer=self).count()
        return total_addresses

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
    street_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=50, null=True)
    zip = models.CharField(max_length=10, null=True)
    default_address = models.BooleanField(default=False)

    def __str__(self):
        return self.street_address 

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
    cart_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum([item.total_price() for item in self.items.all()])

# Cart item
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
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
    
class Contact(models.Model):
    full_name=models.CharField(max_length=100)
    email=models.EmailField()
    message=models.TextField()
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.message

    def save(self, *args, **kwargs):
        send_mail(
            "Contact Message",
            "Here is the message.",
            "tila.ale00@gmail.com",
            [self.email],
            fail_silently=False,
            html_message=f'<p>{self.full_name}</p><p>{self.message}</p>'
        )   
        return super(Contact,self).save(*args, **kwargs)

class FAQ(models.Model):
    question = models.CharField(max_length=100)
    answer = models.TextField()

    def __str__(self) -> str:
        return self.question