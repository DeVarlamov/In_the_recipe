from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)


class CreateListRetriveViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Набор представлений, который сочетает в себе функциональность создания,
    перечисления и извлечения моделей.

    Этот набор представлений наследуется от классов CreateModelMixin,
    ListModelMixin, RetrieveModelMixin и GenericViewSet,
    предоставляя полный набор действий для взаимодействия с моделями.

    Действия:
    - Создать: Создайте новый экземпляр модели.
    - Список: Извлекает список всех экземпляров модели.
    - Извлечение: Извлечение конкретного экземпляра модели по его уникальному
    идентификатору.
    ```
    """
    pass
