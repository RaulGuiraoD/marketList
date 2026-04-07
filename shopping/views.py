from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto

def lista_compra(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre')
        if nombre_producto:
            Producto.objects.create(nombre=nombre_producto)
        return redirect('lista_compra')
    
    productos = Producto.objects.all()
    return render(request, 'shopping/lista.html', {'prodcutos': productos})

def completar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.completado = not producto.completado
    producto.save()
    return redirect('lista_compra')

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('lista_compra')
