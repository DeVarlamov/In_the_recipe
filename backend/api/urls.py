from api.v1.urls import urlpatterns as api_v1_urls
from django.urls import include, path

urlpatterns = [
    path('', include(api_v1_urls)),
]
