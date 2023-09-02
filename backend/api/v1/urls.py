from api.v1.views import IngredientViewSet, RecipeViewSet, TagViewSet
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

app_name = 'api'

handler404 = 'api.views.my_custom_page_not_found_view'

router_v1 = DefaultRouter()

router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'tags', TagViewSet, basename='tag')
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls)),
    re_path('auth/', include('djoser.urls.authtoken')),
]
