from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from usuarios.views import *
from sindicato.views import *
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # USUARIOS
    path('usuarios/',ListarUsuariosView.as_view(),name='usuarios'),
    path('editar/usuario/<pk>',crear_usuario,name='editar_usuario'),
    path('eliminar/usuario/<pk>', eliminar_usuario, name='eliminar_usuario'),
    path('crear/usuario/',crear_usuario,name='crear_usuario'),

    # SINDICATO
    path('',HomeView.as_view(),name='home'),
    path('reportes/',HomeView.as_view(),name='reportes'),
    path('noticias/',HomeView.as_view(),name='noticias'),

    # ROLES
    path('roles/',roles,name='roles'),
    path('eliminar_rol/<pk>',eliminar_rol,name='eliminar_rol'),
    path('crear_rol/',crear_rol,name='crear_rol'),

    # CUOTAS
    path('cuotas/',cuotas ,name='cuotas'),
    path('cuota/<pk>',cuota ,name='cuota'),
    path('actualizar_cuota/<pk>',actualizar_cuota ,name='actualizar_cuota'),

    # actaS
    path('actas/',actas_list ,name='actas'),
    path('acta/<pk>',acta ,name='acta'),
    path('crear_acta/',crear_acta ,name='crear_acta'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)