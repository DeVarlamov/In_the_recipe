from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее только
    авторам редактировать свои собственные объекты.

    Только автор объекта может редактировать его.
    Все пользователи имеют доступ только для чтения.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
