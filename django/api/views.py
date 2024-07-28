from rest_framework import mixins, viewsets
from rest_framework.serializers import Serializer
from rest_framework_tracking.mixins import LoggingMixin


class CommonAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Базовый класс для обработки запросов по API. (Класс для определения новых методов)
    """

    lookup_field = "id"
    # authentication_classes = (JWTAuthentication,)

    PERMISSIONS = {}

    # Словарь с сериализаторами для запроса и ответа.
    # Пример: {'create': {'request': Serializer, 'response': Serializer}}
    # По умолчанию используется serializer_class
    serializer_action_class: dict[str, dict[str, Serializer]] = {}


class GenericAPIView(LoggingMixin, CommonAPIView):
    """
    Класс для обработки запросов по API. (Класс для переопределения методов DRF)
    """

    logging_methods = ["POST", "PUT", "GET", "PATCH", "DELETE"]

    def get_serializer_class(self):
        """Возвращает класс сериализатора для запроса"""

        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method." % self.__class__.__name__
        )

        if self.action not in self.serializer_action_class:
            return self.serializer_class

        return self.serializer_action_class.get(self.action).get("request", self.serializer_class)

    def get_response_data(self, serializer_class, instance, pagination=True, **kwargs) -> dict:
        if "many" in kwargs and pagination:
            page = self.paginate_queryset(instance)
            if page is not None:
                serializer = serializer_class(page, **kwargs)
                return self.get_paginated_response(serializer.data)
        return serializer_class(instance, **kwargs).data
