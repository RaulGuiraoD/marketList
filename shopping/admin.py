from django.contrib import admin
from .models import Tienda, MaestroProducto, ListaCompra, ItemLista

admin.site.register(Tienda)
admin.site.register(MaestroProducto)
admin.site.register(ListaCompra)
admin.site.register(ItemLista)