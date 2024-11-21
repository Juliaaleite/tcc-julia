from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('landingpage/', views.landingpage, name='landingpage'),
    path('cadastro_manutencao/', views.cadastro_manutencao, name='cadastro_manutencao'),
    path('status_maquina/', views.status_maquina, name='status_maquina'),
    path('entrarDOC/', views.login_view, name='entrarDOC'),
    path('cadastro_docente/', views.cadastro, name='cadastro_docente'),
    path('manualwebadm/', views.manualwebadm, name='manualwebadm'),
    path('manualwebdoc/', views.manualwebdoc, name='manualwebdoc'),
    path('cadastro_maquina/', views.cadastrar_maquina, name='cadastro_maquina'),
    path('manual_maquina/', views.manual_maquinas, name='manual_maquina'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('calendarioadm/', views.calendarioadm, name='calendarioadm'),
    path('calendariodoc/', views.calendariodoc, name='calendariodoc'),
    path('', views.login_view, name='entrarDOC'),
    path('calendarioadm/', views.calendarioadm, name='calendarioadm'),
    path('calendariodoc/', views.calendariodoc, name='calendariodoc'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
