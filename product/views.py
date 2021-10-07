from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
from .models import Product, ProductReview
from .serializers import ProductListSerializer, ProductDetailSerializer, ProductCreateSerializer, ProductReviewSerializer
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import permissions

# 1. Подход с созданием функции
# 127.0.0.1:8000/products/
# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)



# 2. Создание класса от APIView
# class ProductListView(APIView):
    
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

#     def delete(self, request):
        

#     def update(self, request):



# 3. GenericAPIview(
#     CRUD
# )

# class ProductListView(ListAPIView):
#     '''
#     GET метод
#     '''
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer

# #RetrieveAPIView -> Отвечает за получение конкретной данные
# class ProductDetailView(RetrieveAPIView):
#     '''
#     GET метод
#     '''
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailSerializer


# # Read -> Create, Update, Delete

# class ProductUpdateView(UpdateAPIView):
#     '''
#     PUT, PATCH метод
#     '''
#     queryset = Product.objects.all()
#     serializer_class = ProductCreateSerializer



# class ProductDeleteView(DestroyAPIView):
#     '''
#     DELETE метод
#     '''
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer
    


# class ProductCreateView(CreateAPIView):
#     '''
#     POST метод
#     '''
#     queryset = Product.objects.all()
#     serializer_class = ProductCreateSerializer






# 4. ModelViewset(
#   CreateMixin, UpdateMixin, DeleteMixin, RetrieveMixin
# )

class ProductReviewViewset(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        '''
        Передаём request в сериализаторы чтобы оттуда получить юзера
        '''
        return {'request': self.request}

    def get_serializer(self, *args, **kwargs):
        '''
        Добавляем в наши аргументы те данные которые мы возвращаем в get_serializer_context
        '''
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)




class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [filters.DjangoFilterBackend, rest_filters.SearchFilter]
    filterset_fields = ['price', 'title']
    search_fields = ['title', 'description']
    permission_class = [permissions.IsAdminUser]
    serializer_class = ProductListSerializer

    def get_permissions(self):
        for self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAdminUser()]
        return []

    def get_serializer_class(self):
        if self.action in ['list', 'delete']:
            return ProductListSerializer

        elif self.action == 'retrieve':
            return ProductDetailSerializer

        return ProductCreateSerializer

    @action(['GET'], detail=True)
    def reviews(self, request, pk=None):
        product = self.get_object()
        # reviews = ProductReview.objects.filter(product=product)
        reviews = product.reviews.all() 
        serializer = ProductReviewSerializer(
            reviews, many=True
        ).data
        return Response(serializer, status=200)


    def get_serializer_context(self):
        '''
        Передаём request в сериализаторы чтобы оттуда получить юзера
        '''
        return {'request': self.request}

    def get_serializer(self, *args, **kwargs):
        '''
        Добавляем в наши аргументы те данные которые мы возвращаем в get_serializer_context
        '''
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)