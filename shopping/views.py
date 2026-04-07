from django.shortcuts import render, redirect, get_object_or_404
from .models import Tienda, ListaCompra, MaestroProducto, ItemLista

def dashboard(request):
    listas_abiertas = ListaCompra.objects.filter(esta_finalizada=False).order_by('-fecha_creacion')
    tiendas = Tienda.objects.all()

    if request.method == 'POST':
        # Caso A: Añadir una tienda nueva
        if 'nombre_tienda' in request.POST:
            nombre = request.POST.get('nombre_tienda')
            color = request.POST.get('color_tienda', '#007bff')
            if nombre:
                Tienda.objects.create(nombre=nombre, color_hex=color)
            return redirect('dashboard')

        # Caso B: Crear una nueva lista de la compra
        tienda_id = request.POST.get('tienda_id')
        if tienda_id:
            tienda = get_object_or_404(Tienda, id=tienda_id)
            nueva_lista = ListaCompra.objects.create(tienda=tienda)
            return redirect('ver_lista', lista_id=nueva_lista.id)

    return render(request, 'shopping/dashboard.html', {
        'listas_abiertas': listas_abiertas,
        'tiendas': tiendas,
    })

def ver_lista(request, lista_id):
    # Por ahora, solo un placeholder para que no de error
    lista = get_object_or_404(ListaCompra, id=lista_id)
    return render(request, 'shopping/lista_detalle.html', {'lista': lista})