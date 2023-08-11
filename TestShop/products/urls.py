from django.urls import path
from .views import CategoryViewSet, TagViewSet, ProductViewSet, ProductExportExcel

urlpatterns = [
    path('api/categories/', CategoryViewSet.as_view({'get': 'list'}), name='category-list'),
    path('api/tags/', TagViewSet.as_view({'get': 'list'}), name='tag-list'),
    path('api/products/', ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    path('api/products/export/', ProductExportExcel.as_view(), name='product-export'),

]
