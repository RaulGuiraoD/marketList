from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_compra, name='lista_compra'),
    path('completar/<int:pk>/', views.completar_producto, name='completar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
]