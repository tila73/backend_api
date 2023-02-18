#from django.shortcuts import render
from rest_framework import generics, permissions,pagination,viewsets
from . import serializers
from . import models
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class VendorList(generics.ListCreateAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer

class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorDetailSerializer

class ProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    # view level pagination
    # pagination_class = pagination.PageNumberPagination
    
    # def get_queryset(self):
    #     brand_name = self.kwargs.get('brand_name', None)
    #     if brand_name is not None:
    #         queryset = models.Product.objects.filter(brand__name=brand_name)
    #     else:
    #         queryset = models.Product.objects.all()
    #     return queryset

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductDetailSerializer

#Customers
class CustomerList(generics.ListCreateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerDetailSerializer

# Order
class OrderList(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

class OrderDetail(generics.ListAPIView):
    #queryset = models.OrderItems.objects.all()
    serializer_class = serializers.OrderDetailSerializer

    def get_queryset(self):
        order_id=self.kwargs['pk']
        order=models.Order.objects.get(id=order_id)
        order_items=models.OrderItem.objects.filter(order=order)
        return order_items
    
class CustomerAddressViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CustomerAddressSerializer
    queryset = models.CustomerAddress.objects.all()

class ProductRatingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductRatingSerializer
    queryset = models.ProductRating.objects.all()

# Main Category
# class MainCategoryList(APIView):
#     def get(self, request):
#         main_categories = models.MainCategory.objects.all()
#         serializer = serializers.MainCategorySerializer(main_categories, many=True)
#         return Response(serializer.data)
class MainCategoryList(generics.ListAPIView):
    serializer_class = serializers.MainCategorySerializer
    queryset = models.MainCategory.objects.all()

    # def get_queryset(self):
    #     queryset = models.MainCategory.objects.all()
    #     main_category_slug = self.request.query_params.get('main_category_slug')
    #     if main_category_slug is not None:
    #         queryset = queryset.filter(slug=main_category_slug)
    #     return queryset


# class MainCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.MainCategory.objects.all()
#     serializer_class = serializers.MainCategoryDetailSerializer

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
# class CategoryList(APIView):
#     def get(self, request, main_category_slug):
#         main_category = get_object_or_404(models.MainCategory, slug=main_category_slug)
#         categories = models.Category.objects.filter(main_category=main_category)
#         serializer = serializers.CategorySerializer(categories, many=True)
#         return Response(serializer.data)
class CategoryList(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

#     def get_queryset(self):
#         main_category_slug = self.kwargs['main_category_slug']
#         queryset = models.Category.objects.filter(main_category__slug=main_category_slug)
#         return queryset

# class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Category.objects.all()
#     serializer_class = serializers.CategoryDetailSerializer

# Sub Category
# class SubCategoryList(APIView):
#     def get(self, request, main_category_slug, category_slug):
#         main_category = get_object_or_404(models.MainCategory, slug=main_category_slug)
#         category = get_object_or_404(models.Category, main_category=main_category, slug=category_slug)
#         sub_categories = models.SubCategory.objects.filter(category=category)
#         serializer = serializers.SubCategorySerializer(sub_categories, many=True)
#         return Response(serializer.data)
class SubCategoryList(generics.ListCreateAPIView):
    queryset = models.SubCategory.objects.all()
    serializer_class = serializers.SubCategorySerializer

# class SubCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.SubCategory.objects.all()
#     serializer_class = serializers.SubCategoryDetailSerializer

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
    
