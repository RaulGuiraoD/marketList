from django.urls import path
from . import views

urlpatterns = [
    path('tiendas/', views.gestionar_tiendas, name='gestionar_tiendas'),
    path('tiendas/eliminar/<int:tienda_id>/', views.eliminar_tienda, name='eliminar_tienda'),
    path('tiendas/editar/<int:tienda_id>/', views.editar_tienda, name='editar_tienda'),
    path('maestro/', views.gestionar_maestro, name='gestionar_maestro'),
    path('maestro/eliminar/<int:producto_id>/', views.eliminar_producto_maestro, name='eliminar_producto_maestro'),
    path('maestro/eliminar-multiple/', views.eliminar_multiple_maestros, name='eliminar_multiple_maestros'),
]