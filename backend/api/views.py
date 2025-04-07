from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Max

from api.serializers import (
    ProductSerializer,
    OrderSerializer,
    ProductInfoSerializer
)
from api.models import Product, Order

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer


# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, id=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'


# @api_view(['GET'])
# def order_list(request):
#     # orders = Order.objects.all()
#     orders = Order.objects.prefetch_related('items__product') # prefetches items as well
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })

    return Response(serializer.data)
