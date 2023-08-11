from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import openpyxl
from io import BytesIO
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Tag, Product
from .serializers import CategorySerializer, TagSerializer, ProductSerializer
from config.settings import CACHE_TTL



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        cache_key = 'product_list'
        cached_data = cache.get(cache_key)
        if cached_data is None:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
            return Response(serializer.data)
        return Response(cached_data)




class ProductExportExcel(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)


        wb = openpyxl.Workbook()
        ws = wb.active


        headers = ['ID', 'Name', 'Description', 'Category Name', 'Price', 'Created At', 'Tags']
        ws.append(headers)


        for product in serializer.data:
            row = [
                str(product['id']),
                product['name'],
                product['description'],
                product['category_name'],
                str(product['price']),
                str(product['created_at']),
                ', '.join([str(tag) for tag in product['tags']])
            ]
            ws.append(row)


        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'


        output = BytesIO()
        wb.save(output)
        response.write(output.getvalue())

        return response