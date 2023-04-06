#from django.shortcuts import render
from rest_framework import generics, permissions,pagination,viewsets
from . import serializers
from . import models
from .pagination import CustomPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

class VendorList(generics.ListCreateAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer

class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorDetailSerializer

@csrf_exempt
def seller_login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(username=username,password=password)
    
    if user:
        vendor=models.Vendor.objects.get(user=user)
        msg={
            'bool':True,
            'user':user.username,
            'id':vendor.id,
        }
    else:
        msg={
            'bool':False,
            'msg':'Invalid username or password!'
        }
    return  JsonResponse(msg)

@csrf_exempt
def seller_register(request):
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    email=request.POST.get('email')
    address=request.POST.get('address')
    mobile=request.POST.get('mobile')
    username=request.POST.get('username')
    password=request.POST.get('password')
    hashed_password = make_password(password)
    
    try:
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed_password,
        )
        if user:
            try:
                # Create vendor
                vendor=models.Vendor.objects.create(
                    user=user,
                    address=address,
                    mobile=mobile
                )
                msg={
                    'bool':True,
                    'user':user.username,
                    'seller':vendor.id,
                    'msg':'Thank you for your registration. You can login now.'
                }
            except IntegrityError:
                msg={
                    'bool':False,
                    'msg':'A user with that mobile number already exists.'
                }
        else:
            msg={
                'bool':False,
                'msg':'Oops...! Something went wrong.'
            }
    except IntegrityError:
        msg={
            'bool':False,
            'msg':'Username already exists.'
        }
    return  JsonResponse(msg)

class VendorProductList(generics.ListAPIView):
    serializer_class=serializers.ProductCreateSerializer
    
    def get_queryset(self):
        vendor_id=self.kwargs['vendor_id']
        vendor=models.Vendor.objects.get(pk=vendor_id)
        return models.Product.objects.filter(vendor=vendor)
    
class VendorProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class=serializers.ProductCreateSerializer
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        product_serializer = self.get_serializer(instance=instance, data=request.data)
        if product_serializer.is_valid():
            product = product_serializer.save()

            # Delete all existing ProductImage objects for the product
            product.product_images.all().delete()

            # Update each uploaded file and save it to the database
            for file in request.FILES.getlist('product_images'):
                product_image = models.ProductImage.objects.create(
                    product=product,
                    image=file,
                )

            headers = self.get_success_headers(product_serializer.data)
            return Response(product_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_success_headers(self, data):
        try:
            return {'Location': data['url']}
        except (TypeError, KeyError):
            return {}

class ProductCreate(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductCreateSerializer

    def post(self, request, *args, **kwargs):
        product_serializer = self.get_serializer(data=request.data)
        if product_serializer.is_valid():
            product = product_serializer.save()

            # Loop through each uploaded file and save it to the database
            for file in request.FILES.getlist('product_images'):
                product_image = models.ProductImage.objects.create(
                    product=product,
                    image=file,
                )

            headers = self.get_success_headers(product_serializer.data)
            return Response(product_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    pagination_class = CustomPagination
    # view level pagination
    # pagination_class = pagination.PageNumberPagination
    
    def get_queryset(self):
        if 'searchString' in self.kwargs:
            search=self.kwargs['searchString']
            qs=models.Product.objects.filter(Q(title__icontains=search))
            return qs
        else:
            return self.queryset

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductDetailSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=self.kwargs['product_slug'])
        return obj

# main category slug, category slug, subcategory slug, product slug garna
# class ProductDetail(generics.RetrieveAPIView):
#     serializer_class = serializers.ProductDetailSerializer

#     def get_object(self):
#         # category_slug = self.kwargs.get('category_slug')
#         subcategory_slug = self.kwargs.get('subcategory_slug')
#         product_slug = self.kwargs.get('product_slug')
#         return get_object_or_404(models.Product, subcategory__slug=subcategory_slug, slug=product_slug)

#Customers
class CustomerList(generics.ListCreateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerDetailSerializer

class AddressList(generics.ListCreateAPIView):
    queryset = models.CustomerAddress.objects.all()
    serializer_class = serializers.CustomerAddressSerializer

    def perform_create(self, serializer):
        # Get the customer ID from the request data
        customer_id = self.request.data.get("customer")

        # Set the new address as the default if no default address exists
        if models.CustomerAddress.objects.filter(customer_id=customer_id, default_address=True).count() == 0:
            serializer.validated_data['default_address'] = True

        # Set the new address as the default and unset any existing default address
        elif serializer.validated_data.get('default_address', False):
            current_default = models.CustomerAddress.objects.get(customer_id=customer_id,  default_address=True)
            current_default.default_address = False
            current_default.save()
            serializer.validated_data['default_address'] = True

        # Create the new address
        serializer.save(customer_id=customer_id)

class CustomerAddressList(generics.ListAPIView):
    serializer_class=serializers.CustomerAddressSerializer
    
    def get_queryset(self):
        customer_id=self.kwargs['customer_id']
        customer=models.Customer.objects.get(pk=customer_id)
        return models.CustomerAddress.objects.filter(customer=customer)
    
class CustomerAddressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CustomerAddress.objects.all()
    serializer_class=serializers.CustomerAddressSerializer

    def perform_update(self, serializer):
        # Get the customer ID from the request data
        customer_id = serializer.validated_data.get("customer")

        # Set the new address as the default if no default address exists
        if models.CustomerAddress.objects.filter(customer_id=customer_id, default_address=True).exclude(id=serializer.instance.id).count() == 0:
            serializer.validated_data['default_address'] = True

        # Set the new address as the default and unset any existing default address
        elif serializer.validated_data.get('default_address', False):
            current_default = models.CustomerAddress.objects.get(customer_id=customer_id, default_address=True)
            current_default.default_address = False
            current_default.save()
            serializer.validated_data['default_address'] = True

            # Update the previous default address to be non-default
            previous_default = serializer.instance
            previous_default.default_address = False
            previous_default.save()

        # Update the address
        serializer.save()

@csrf_exempt
def customer_login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(username=username,password=password)
    if user:
        customer=models.Customer.objects.get(user=user)
        msg={
            'bool':True,
            'user':user.username,
            'id':customer.id,
        }
    else:
        msg={
            'bool':False,
            'msg':'Invalid username or password!'
        }
    return  JsonResponse(msg)

@csrf_exempt
def customer_register(request):
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    email=request.POST.get('email')
    mobile=request.POST.get('mobile')
    username=request.POST.get('username')
    password=request.POST.get('password')
    hashed_password = make_password(password)
    
    try:
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed_password,
        )
        if user:
            try:
                # Create customer
                customer=models.Customer.objects.create(
                    user=user,
                    mobile=mobile
                )
                msg={
                    'bool':True,
                    'user':user.username,
                    'customer':customer.id,
                    'msg':'Thank you for your registration. You can login now.'
                }
            except IntegrityError:
                msg={
                    'bool':False,
                    'msg':'A user with that mobile number already exists.'
                }
        else:
            msg={
                'bool':False,
                'msg':'Oops...! Something went wrong.'
            }
    except IntegrityError:
        msg={
            'bool':False,
            'msg':'Username already exists.'
        }
    return  JsonResponse(msg)

# Order
class OrderList(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return super().post(request, *args, **kwargs)

class OrderDetail(generics.ListAPIView):
    #queryset = models.OrderItems.objects.all()
    serializer_class = serializers.OrderDetailSerializer

    def get_queryset(self):
        order_id=self.kwargs['pk']
        order=models.Order.objects.get(id=order_id)
        order_items=models.OrderItem.objects.filter(order=order)
        return order_items

class ProductRatingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductRatingSerializer
    queryset = models.ProductRating.objects.all()

# Main Category
# class MainCategoryList(generics.ListAPIView):
#     serializer_class = serializers.MainCategorySerializer
#     queryset = models.MainCategory.objects.all()
class MainCategoryList(generics.ListAPIView):
    serializer_class = serializers.MainCategorySerializer
    queryset = models.MainCategory.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Add categories and subcategories to each main category
        for main_category_data in data:
            main_category = models.MainCategory.objects.get(id=main_category_data['id'])
            categories = models.Category.objects.filter(main_category=main_category)
            category_serializer = serializers.CategorySerializer(categories, many=True)
            main_category_data['categories'] = category_serializer.data
            for category_data in main_category_data['categories']:
                category = models.Category.objects.get(id=category_data['id'])
                subcategories = models.SubCategory.objects.filter(category=category)
                subcategory_serializer = serializers.SubCategorySerializer(subcategories, many=True)
                category_data['subcategories'] = subcategory_serializer.data
        return Response(data)

# Main Category Detail
class MainCategoryDetail(generics.RetrieveAPIView):
    serializer_class = serializers.MainCategoryDetailSerializer

    def get_object(self):
        maincategory_slug = self.kwargs.get('maincategory_slug')
        return get_object_or_404(models.MainCategory, slug=maincategory_slug)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"show_subcategories": True})
        return context

# Category
# class CategoryList(generics.ListCreateAPIView):
#     queryset = models.Category.objects.all()
#     serializer_class = serializers.CategorySerializer

# Category Detail
class CategoryDetail(generics.RetrieveAPIView):
    serializer_class = serializers.CategoryDetailSerializer

    def get_object(self):
        maincategory_slug = self.kwargs.get('maincategory_slug')
        category_slug = self.kwargs.get('category_slug')
        return get_object_or_404(models.Category, main_category__slug=maincategory_slug, slug=category_slug)

# Sub Category
# class SubCategoryList(generics.ListCreateAPIView):
#     queryset = models.SubCategory.objects.all()
#     serializer_class = serializers.SubCategorySerializer

# Sub Category Detail
class SubCategoryDetail(generics.RetrieveAPIView):
    serializer_class = serializers.SubCategoryDetailSerializer

    def get_object(self):
        # maincategory_slug = self.kwargs.get('maincategory_slug')
        category_slug = self.kwargs.get('category_slug')
        subcategory_slug = self.kwargs.get('subcategory_slug')
        return get_object_or_404(models.SubCategory, category__slug=category_slug, slug=subcategory_slug)
        # return get_object_or_404(models.SubCategory, main_category__slug=maincategory_slug, category__slug=category_slug, slug=subcategory_slug)

# Brand
class BrandList(generics.ListCreateAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandDetailSerializer

class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandDetailSerializer

class ProductsByBrand(generics.ListAPIView):
    serializer_class = serializers.ProductListSerializer

    def get(self, request, *args, **kwargs):
        brand_slug = self.kwargs['brand_slug']
        brand = get_object_or_404(models.Brand, slug=brand_slug)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'brand_name': brand.name,
            'data': serializer.data
        }
        return Response(response_data)

    def get_queryset(self):
        brand_slug = self.kwargs['brand_slug']
        return models.Product.objects.filter(brand__slug=brand_slug)
    
class VendorDashboard(generics.RetrieveAPIView):
    queryset=models.Vendor.objects.all()
    serializer_class=serializers.VendorDashboardSerializer

class CustomerDashboard(generics.RetrieveAPIView):
    queryset=models.Customer.objects.all()
    serializer_class=serializers.CustomerDashboardSerializer
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_cart(request):
    cart_customer = request.user.customer
    cart = cart_customer.cart
    if cart is None:
        cart = models.Cart.objects.create(customer=cart_customer)
    serializer = models.CartSerializer(data=request.data)
    if serializer.is_valid():
        for item in serializer.validated_data['items']:
            product = models.Product.objects.get(id=item['product_id'])
            cart_item = models.CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=item['quantity']
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)