from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Max

from api.serializers import (
    ProductSerializer,
    OrderSerializer,
    ProductInfoSerializer,
)

from api.models import Product, Order

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)

from rest_framework.views import APIView
from rest_framework import generics


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]

        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()


# class ProductCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer


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


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products': products,
#         'count': len(products),
#         'max_price': products.aggregate(max_price=Max('price'))['max_price']
#     })

#     return Response(serializer.data)


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })

        return Response(serializer.data)