from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Tienda, MaestroProducto

@login_required
def gestionar_tiendas(request):
    tiendas = Tienda.objects.filter(usuario=request.user).order_by('nombre')
    return render(request, 'catalog/gestionar_tiendas.html', {'tiendas': tiendas})

@login_required
def eliminar_tienda(request, tienda_id):
    tienda = get_object_or_404(Tienda, id=tienda_id, usuario=request.user)
    tienda.delete()
    return redirect('gestionar_tiendas')

@login_required
def editar_tienda(request, tienda_id):
    tienda = get_object_or_404(Tienda, id=tienda_id, usuario=request.user)
    if request.method == 'POST':
        nombre = request.POST.get('nombre').strip().capitalize()
        color = request.POST.get('color_hex')
        if nombre:
            try:
                if not Tienda.objects.filter(usuario=request.user, nombre=nombre).exclude(id=tienda.id).exists():
                    tienda.nombre = nombre
                    tienda.color_hex = color
                    tienda.save()
            except IntegrityError:
                pass
    return redirect('gestionar_tiendas')

@login_required
def gestionar_maestro(request):
    productos = MaestroProducto.objects.filter(usuario=request.user).order_by('nombre')
    query = request.GET.get('q')
    if query:
        productos = productos.filter(nombre__icontains=query)
    return render(request, 'catalog/gestionar_maestro.html', {'productos': productos})

@login_required
def eliminar_producto_maestro(request, producto_id):
    producto = get_object_or_404(MaestroProducto, id=producto_id, usuario=request.user)
    producto.delete()
    return redirect('gestionar_maestro')

@login_required
def eliminar_multiple_maestros(request):
    if request.method == 'POST':
        ids_a_borrar = request.POST.getlist('productos_ids')
        if ids_a_borrar:
            MaestroProducto.objects.filter(id__in=ids_a_borrar, usuario=request.user).delete()
    return redirect('gestionar_maestro')