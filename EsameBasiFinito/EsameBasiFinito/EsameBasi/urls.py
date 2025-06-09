from django.contrib import admin
from django.urls import path, include

from TechHub.views import componenti_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TechHub.urls')),
]
