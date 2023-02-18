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
    # Products
    path('products/', views.ProductList.as_view()),
    path('product/<int:pk>/', views.ProductDetail.as_view()),
    # Product Categories
    # path('main_categories/', views.MainCategoryList.as_view(), name='main-category-list'),
    # path('main-categories/<slug:main_category_slug>/', views.MainCategoryList.as_view(), name='main_category_detail'),
    # path('<slug:main_category_slug>/categories/', views.CategoryList.as_view(), name='category-list'),
    # path('<slug:main_category_slug>/<slug:category_slug>/sub-categories/', views.SubCategoryList.as_view(), name='sub-category-list'),

    path('main_categories/', views.MainCategoryList.as_view()),
    path('main_categories/<slug:maincategory_slug>/', views.MainCategoryDetail.as_view()),
    # path('main_category/<int:pk>/', views.MainCategoryDetail.as_view()),
    # path('<slug:main_category_slug>/categories/', views.MainCategoryDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
    # path('category/<int:pk>/', views.CategoryDetail.as_view()),
    path('sub_categories/', views.SubCategoryList.as_view()),
    # path('sub_category/<int:pk>/', views.SubCategoryDetail.as_view()),

    # Brands
    path('brands/', views.BrandList.as_view()),
    path('brand/<int:pk>/', views.BrandDetail.as_view()),
    # path('brands/<slug:brand_name>/', views.ProductsByBrand.as_view()),
    path('brands/<slug:brand_slug>/', views.ProductsByBrand.as_view()),
    # path('brands/<slug:brand_name>/', views.ProductsByBrand.as_view(), name='products-by-brand'),
    # path('brands/<str:brand_slug>/', views.BrandProductListView.as_view(), name='brand-products'),
    
    #Customers
    path('customers/', views.CustomerList.as_view()),
    path('customer/<int:pk>/', views.CustomerDetail.as_view()),
    #Orders
    path('orders/', views.OrderList.as_view()),
    path('order/<int:pk>/', views.OrderDetail.as_view()),
    ]

urlpatterns+=router.urls