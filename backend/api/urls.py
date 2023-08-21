from api.views import IngredientViewSet, TagViewSet
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'tags', TagViewSet, basename='tag')
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls)),
    re_path('auth/', include('djoser.urls.authtoken')),
]
