from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from .serializers import OrderSerializer


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # Добавить фильтрацию и какой нибудь Filtration

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