from django.urls import include, path

from api.v1.urls import urlpatterns as api_v1_urls

urlpatterns = [
    path('', include(api_v1_urls)),
]
