from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """
    Пагинация на основе номера страницы с ограничением
    количества элементов на странице.

    Атрибуты:

    page_size (int): Количество элементов на странице по умолчанию.
    page_size_query_param (str): Название параметра запроса,
    который позволяет пользователю указать количество элементов на странице.
    :param PageNumberPagination: Базовый класс для
    пагинации на основе номера страницы.
    """

    page_size = 6
    page_size_query_param = 'limit'
