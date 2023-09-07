from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import Subscribed, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админка User"""
    list_display = ('username', 'email', 'first_name',
                    'last_name',)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ['email', 'first_name', 'last_name']}),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
                                         'email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_superuser', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Subscribed)
class SubscribedAdmin(admin.ModelAdmin):
    """Админка подписчика"""
    list_display = ('id', 'user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('user__username', 'author__username')
    ordering = ('-id',)
    fieldsets = (
        (None, {
            'fields': ('user', 'author')
        }),
    )
