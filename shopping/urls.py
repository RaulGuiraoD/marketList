from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('lista/<int:lista_id>/', views.ver_lista, name='ver_lista'), # Esta la crearemos ahora
]