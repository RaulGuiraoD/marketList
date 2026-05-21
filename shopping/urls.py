from django.urls import path
from . import views

urlpatterns = [
    path('lista/<int:lista_id>/', views.ver_lista, name='ver_lista'),
    path('lista/cambiar-tienda/<int:lista_id>/', views.cambiar_tienda_lista, name='cambiar_tienda_lista'),
    path('lista/eliminar/<int:lista_id>/', views.eliminar_lista, name='eliminar_lista'),
    path('item/cambiar-cantidad/<int:item_id>/<str:operacion>/', views.cambiar_cantidad, name='cambiar_cantidad'),
    path('item/completar/<int:item_id>/', views.completar_item, name='completar_item'),
    path('item/eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('lista/finalizar/<int:lista_id>/', views.finalizar_compra, name='finalizar_compra'),
    path('archivadas/', views.listas_archivadas, name='listas_archivadas'),
    path('lista/reabrir/<int:lista_id>/', views.reabrir_lista, name='reabrir_lista'),
    path('archivadas/eliminar-multiple/', views.eliminar_multiple_listas, name='eliminar_multiple_listas'),
]