from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from core.models import PerfilUsuario

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario) 
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def perfil(request):
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        perfil.nombre_completo = request.POST.get('nombre')
        perfil.apellidos = request.POST.get('apellidos')
        perfil.sexo = request.POST.get('sexo')

        nuevo_presupuesto = request.POST.get('presupuesto')
        if nuevo_presupuesto:
            perfil.presupuesto_mensual = nuevo_presupuesto.replace(',', '.')
            
        perfil.avatar_icon = request.POST.get('avatar_icon', perfil.avatar_icon)
        perfil.save()
        
        messages.success(request, "Perfil actualizado")
        return redirect('dashboard')

    return render(request, 'core/perfil.html', {'perfil': perfil})

@login_required
def dashboard(request):
    # Nota: Importamos aquí o arriba para evitar imports circulares si hiciera falta
    from shopping.models import ListaCompra
    from catalog.models import Tienda

    listas_abiertas = ListaCompra.objects.filter(usuario=request.user, esta_finalizada=False).order_by('-fecha_creacion')
    tiendas = Tienda.objects.filter(usuario=request.user).order_by('nombre')

    if request.method == 'POST':
        if 'nombre_tienda' in request.POST:
            nombre = request.POST.get('nombre_tienda', '').strip().capitalize()
            color = request.POST.get('color_tienda', '#007bff')
            if nombre:
                Tienda.objects.get_or_create(usuario=request.user, nombre=nombre, defaults={'color_hex': color})
            return redirect('dashboard')

        tienda_id = request.POST.get('tienda_id')
        if tienda_id:
            from django.shortcuts import get_object_or_404
            tienda = get_object_or_404(Tienda, id=tienda_id, usuario=request.user)
            nueva_lista = ListaCompra.objects.create(usuario=request.user, tienda=tienda)
            return redirect('ver_lista', lista_id=nueva_lista.id)

    return render(request, 'core/dashboard.html', {
    'listas_abiertas': listas_abiertas,
    'tiendas': tiendas,
})