from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Пользовательский класс разрешений, который разрешает только автору объекта
    чтобы изменить его, разрешив при этом доступ только для
    чтения другим пользователям.

    Наследуется от `rest_framework.permissions.Базовое разрешение`.

    Методы:
    - has_permission(запрос, просмотр): определяет,
    есть ли у пользователя разрешение
    чтобы получить доступ к просмотру.
    - has_object_permission(запрос, просмотр, obj): определяет,
    есть ли у пользователя
    разрешение на выполнение указанного метода над объектом."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
