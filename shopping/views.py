from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ListaCompra, ItemLista
from catalog.models import Tienda, MaestroProducto

def categorizar_mercadona(nombre_prod):
    nombre = nombre_prod.lower()
    categorias = {
        'Congelados': ['congelad', 'conge', 'hielo', 'helad', 'sorbet', 'nugget', 'varit', 'croquet', 'lasaña', 'canelon', 'salteado', 'guisante', 'verdur congelad', 'arroz congelado', 'pizz', 'corneto', 'magnum'],
        'Salsas': ['mayones', 'ketchup', 'mostaz', 'brava', 'soja', 'gajo', 'alioli', 'salsa', 'tabasco', 'teriyaki', 'pesto', 'boloñesa', 'carbonara', 'vinagreta', 'barbacoa', 'bbq', 'roquefort', 'miel y mostaza'],
        'Aperitivos': ['patat bolsa', 'patatas bolsa', 'papas', 'snack', 'fruto seco', 'almendr', 'avellan', 'nueces', 'pistacho', 'pipas', 'palomit', 'nachos', 'tortillita', 'cortez', 'cacahuete', 'anacard', 'picos', 'regaña', 'altramuz'],
        'Pescadería': ['merluz', 'bacala', 'gamba', 'langostin', 'mejillon', 'pulpo', 'sepia', 'calamar', 'dorad', 'lubin', 'emperador', 'almej', 'gula', 'salmon', 'rodaballo', 'dorada', 'lubina'],
        'Despensa y Latas': ['atun', 'lata', 'conserva', 'bote', 'frasco', 'arroz', 'cuscus', 'vasito', 'tarrina', 'pasta', 'macarr', 'espague', 'fideo', 'harin', 'aceit', 'vinagr', 'sal', 'azucar', 'legumbr', 'lentej', 'garbanz', 'alubi', 'cald', 'especi', 'frit', 'maiz', 'miel', 'tomate frito', 'levadura', 'pan rallado', 'colorante'],
        'Lácteos y Frío': ['yogur', 'cuajad', 'mantequill', 'kefir', 'leche', 'batid', 'nat', 'hummu', 'guacamol', 'gelatin', 'postr', 'mozzarel', 'flan', 'masa', 'hojaldre', 'quebrada', 'base pizza', 'bebible', 'natillas', 'salmorejo', 'gazpacho', 'margarina', 'petit'],
        'Frutería y Verdura': ['patat', 'ceboll', 'ajo', 'lechug', 'tomat', 'platan', 'manzan', 'per', 'frut', 'verdur', 'aguacat', 'limon', 'naranj', 'fres', 'uvas', 'pimiento', 'calabaci', 'zanahori', 'seta', 'champi', 'piña', 'kiwi', 'boniat', 'bonia', 'bata', 'batata', 'brocoli', 'berenjena', 'pepino'],
        'Carnicería': ['poll', 'terner', 'cerd', 'lomo', 'filet', 'hamburg', 'alit', 'carn', 'pechug', 'torrez', 'picada', 'pavo fresco', 'cordero', 'conejo'],
        'Charcutería/Quesos': ['embuti', 'chori', 'salchich', 'morta', 'pav', 'jamon', 'bacon', 'fuet', 'pancet', 'ques', 'pate', 'sobrasad', 'brie', 'parmesano', 'cheddar', 'gouda', 'havarti', 'chopped'],
        'Panadería y Dulces': ['pan', 'barr', 'hogaz', 'mold', 'croiss', 'napolitan', 'gallet', 'bizcoch', 'magdalen', 'donut', 'tortit', 'chocolat', 'bombon', 'caramel', 'gominol', 'tarta', 'pastel', 'sobao', 'palmera', 'cereales'],
        'Bebidas y Bodega': ['agu', 'refresc', 'col', 'fant', 'cervez', 'vin', 'zum', 'energet', 'isoton', 'tint', 'sidr', 'caser', 'tonica', 'bati', 'gaseosa', 'licor'],
        'Limpieza': ['detergent', 'suaviz', 'lavavajill', 'lejia', 'fregasuel', 'limpia', 'estropaj', 'bayet', 'fregona', 'escoba', 'bolsa basura', 'aluminio', 'desengrasante', 'antical', 'pastillas lavavajillas', 'film'],
        'Higiene y Cuidado': ['papel', 'higieni', 'cocin', 'servillet', 'champu', 'gel', 'desodor', 'dient', 'cepill', 'maquinill', 'jabon', 'crema', 'colonia', 'compresa', 'tampon', 'acondicionador', 'mascarilla', 'protector'],
        'Mascotas': ['perr', 'gat', 'pienso', 'mascot', 'aren', 'latit', 'snack gato', 'comida humeda', 'malta', 'rascador', 'antiparasit', 'pipet', 'collar', 'chuches', 'chur', 'churu', 'dentastix', 'juguete perro'],
    }
    for categoria, palabras in categorias.items():
        for palabra in palabras:
            if palabra in nombre:
                return categoria
    return 'General'

@login_required
def cambiar_tienda_lista(request, lista_id):
    if request.method == 'POST':
        nueva_tienda_id = request.POST.get('nueva_tienda')
        lista = get_object_or_404(ListaCompra, id=lista_id, usuario=request.user)
        nueva_tienda = get_object_or_404(Tienda, id=nueva_tienda_id, usuario=request.user)
        lista.tienda = nueva_tienda
        lista.save()
    return redirect('ver_lista', lista_id=lista.id)

@login_required
def cambiar_cantidad(request, item_id, operacion):
    item = get_object_or_404(ItemLista, id=item_id, lista__usuario=request.user)
    if operacion == 'sumar':
        item.cantidad += 1
    elif operacion == 'restar' and item.cantidad > 1:
        item.cantidad -= 1
    item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'nueva_cantidad': item.cantidad})
    return redirect('ver_lista', lista_id=item.lista.id)

@login_required
def ver_lista(request, lista_id):
    lista = get_object_or_404(ListaCompra, id=lista_id, usuario=request.user)
    tiendas_disponibles = Tienda.objects.filter(usuario=request.user)
    
    if request.method == 'POST':
        nombre_prod = request.POST.get('nombre').strip().capitalize()
        cantidad_input = int(request.POST.get('cantidad', 1))

        if nombre_prod:
            producto_maestro, created = MaestroProducto.objects.get_or_create(
                usuario=request.user,
                nombre=nombre_prod,
                defaults={'tienda_habitual': lista.tienda}
            )

            if created or producto_maestro.zona == "General":
                nueva_zona = categorizar_mercadona(nombre_prod)
                if nueva_zona != "General":
                    producto_maestro.zona = nueva_zona
                    producto_maestro.save()
            
            item_existente = ItemLista.objects.filter(lista=lista, producto_maestro=producto_maestro).first()
            if item_existente:
                item_existente.cantidad += cantidad_input
                item_existente.save()
            else:
                ItemLista.objects.create(lista=lista, producto_maestro=producto_maestro, cantidad=cantidad_input)

        return redirect('ver_lista', lista_id=lista.id)
    
    orden = request.GET.get('orden', 'recientes')
    if orden == 'secciones':
        criterio = ['comprado', 'producto_maestro__zona', 'producto_maestro__nombre']
    elif orden == 'cantidad':
        criterio = ['comprado', '-cantidad', 'producto_maestro__nombre']
    elif orden == 'antiguos':
        criterio = ['comprado', 'creado_en']
    else:
        criterio = ['comprado', '-creado_en']

    items = lista.items.all().order_by(*criterio)
    return render(request, 'shopping/lista_detalle.html', {
        'lista': lista,
        'tiendas_disponibles': tiendas_disponibles,
        'items': items,
        'sugerencias': MaestroProducto.objects.filter(usuario=request.user).order_by('-frecuencia_uso')[:12],
        'orden_actual': orden 
    })

@login_required
def completar_item(request, item_id):
    item = get_object_or_404(ItemLista, id=item_id, lista__usuario=request.user)
    item.comprado = not item.comprado
    item.save()
    orden = request.GET.get('orden', 'recientes')
    response = redirect('ver_lista', lista_id=item.lista.id)
    response['Location'] += f'?orden={orden}'
    return response

@login_required
def eliminar_item(request, item_id):
    item = get_object_or_404(ItemLista, id=item_id, lista__usuario=request.user)
    lista_id = item.lista.id
    item.delete()
    orden = request.GET.get('orden', 'recientes')
    response = redirect('ver_lista', lista_id=lista_id)
    response['Location'] += f'?orden={orden}'
    return response

@login_required
def finalizar_compra(request, lista_id):
    lista = get_object_or_404(ListaCompra, id=lista_id, usuario=request.user)
    if request.method == 'POST':
        estaba_finalizada_antes = lista.esta_finalizada
        total_raw = request.POST.get('total_ticket', '').strip()
        
        if not total_raw:
            lista.total_ticket = 0
        else:
            try:
                lista.total_ticket = float(total_raw.replace(',', '.'))
            except ValueError:
                lista.total_ticket = 0

        lista.items.all().update(comprado=True)
        lista.esta_finalizada = True
        
        if not lista.fecha_finalizada:
            lista.fecha_finalizada = timezone.now()
        lista.save()
        
        if not estaba_finalizada_antes:
            for item in lista.items.filter(comprado=True):
                producto = item.producto_maestro
                producto.frecuencia_uso += item.cantidad 
                producto.save()
            
        return redirect('dashboard')
    return redirect('ver_lista', lista_id=lista.id)

@login_required
def listas_archivadas(request):
    listas = ListaCompra.objects.filter(usuario=request.user, esta_finalizada=True).order_by('-fecha_finalizada')
    return render(request, 'shopping/listas_archivadas.html', {'listas': listas})

@login_required
def reabrir_lista(request, lista_id):
    lista = get_object_or_404(ListaCompra, id=lista_id, usuario=request.user)
    
    if lista.esta_finalizada:
        for item in lista.items.filter(comprado=True):
            producto = item.producto_maestro
            if producto.frecuencia_uso >= item.cantidad:
                producto.frecuencia_uso -= item.cantidad
            else:
                producto.frecuencia_uso = 0
            producto.save()
    
    lista.esta_finalizada = False
    lista.total_ticket = 0
    lista.save()
    return redirect('ver_lista', lista_id=lista.id)

@login_required
def eliminar_lista(request, lista_id):
    lista = get_object_or_404(ListaCompra, id=lista_id, usuario=request.user)
    if not lista.esta_finalizada:
        lista.delete()
    return redirect('dashboard')

@login_required
def eliminar_multiple_listas(request):
    if request.method == 'POST':
        ids_a_borrar = request.POST.getlist('listas_ids')
        if ids_a_borrar:
            ListaCompra.objects.filter(id__in=ids_a_borrar, usuario=request.user).delete()
    return redirect('listas_archivadas')