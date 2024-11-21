from django.contrib import admin
from django.urls import path, include
from manutencao.views import landingpage  # Substitua 'your_app' pelo nome do seu aplicativo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('manutencao.urls')),
]

