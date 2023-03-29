from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('address', views.CustomerAddressViewSet)
router.register('productrating', views.ProductRatingViewSet)

urlpatterns = [
    # Vendors
    path('vendors/', views.VendorList.as_view()),
    path('vendor/<int:pk>/', views.VendorDetail.as_view()),
    path('seller/login/', views.seller_login, name='seller_login'),
    path('vendor-products/<int:vendor_id>', views.VendorProductList.as_view()),
    path('vendor-product-detail/<int:pk>', views.VendorProductDetail.as_view()),

    #Customers
    path('customers/', views.CustomerList.as_view()),
    path('customer/<int:pk>/', views.CustomerDetail.as_view()),
    path('customer/login/', views.customer_login, name='customer_login'),
    path('customer/register/', views.customer_register, name='customer_register'),

    # Products
    path('products/', views.ProductList.as_view()),
    path('product-create/', views.ProductCreate.as_view()),
    path('search-products/<str:searchString>/', views.ProductList.as_view()),
    # path('product/<int:pk>/', views.ProductDetail.as_view()),
    path('products/<slug:product_slug>/', views.ProductDetail.as_view()),
    # path('<slug:maincategory_slug>/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),

    # Brands
    path('brands/', views.BrandList.as_view()),
    path('brand/<int:pk>/', views.BrandDetail.as_view()),
    path('brands/<slug:brand_slug>/', views.ProductsByBrand.as_view()),

    # Product Categories
    path('main_categories/', views.MainCategoryList.as_view()),
    # path('sub_categories/', views.SubCategoryList.as_view()),
    path('main_categories/<slug:maincategory_slug>/', views.MainCategoryDetail.as_view()),
    # path('categories/', views.CategoryList.as_view()), doesn't work kina vanda yo le mathi ko slug ho vanni bujhxa
    path('<slug:maincategory_slug>/<slug:category_slug>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('<slug:maincategory_slug>/<slug:category_slug>/<slug:subcategory_slug>/', views.SubCategoryDetail.as_view(), name='subcategory-detail'),
    #path('sub_categories/', views.SubCategoryList.as_view()), yo le ni tei main category ko slug linxa
    
    #Orders
    path('orders/', views.OrderList.as_view()),
    path('order/<int:pk>/', views.OrderDetail.as_view()),
    ]

urlpatterns+=router.urls