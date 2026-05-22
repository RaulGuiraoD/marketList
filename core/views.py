import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from core.models import PerfilUsuario
from django.utils.text import slugify
from django.core.files.storage import default_storage

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
        # 1. Captura de datos básicos
        perfil.nombre_completo = request.POST.get('nombre')
        perfil.apellidos = request.POST.get('apellidos')
        perfil.sexo = request.POST.get('sexo')

        # 2. Presupuesto
        nuevo_presupuesto = request.POST.get('presupuesto')
        if nuevo_presupuesto:
            try:
                presupuesto_limpio = nuevo_presupuesto.replace(',', '.')
                perfil.presupuesto_mensual = float(presupuesto_limpio)
            except ValueError:
                perfil.presupuesto_mensual = 0.00

        # 3. Procesar Imagen de forma nativa y robusta
        if 'avatar_image' in request.FILES:
            imagen = request.FILES['avatar_image']
            
            # Validar peso máximo (5 MB)
            MAX_FILE_SIZE = 5 * 1024 * 1024  
            if imagen.size > MAX_FILE_SIZE:
                messages.error(request, "La imagen no puede pesar más de 5MB.")
                return redirect('perfil')

            # Validar extensiones
            extension = os.path.splitext(imagen.name)[1].lower()
            extensiones_validas = ['.jpg', '.jpeg', '.png', '.webp']
            if extension not in extensiones_validas:
                messages.error(request, "Formato no válido. Solo se permite JPG, PNG o WEBP.")
                return redirect('perfil')

            # Renombrar de forma limpia y asignación directa a Django
            nombre_limpio = slugify(os.path.splitext(imagen.name)[0])
            nuevo_nombre = f"user_{request.user.id}_{nombre_limpio}{extension}"
            
            # Al asignarle el nombre modificado al objeto del archivo,
            # Django se encarga de subirlo e indexarlo en la base de datos automáticamente al hacer .save()
            imagen.name = nuevo_nombre
            perfil.avatar_image = imagen
            
        # Guardado definitivo
        perfil.save()
        messages.success(request, "Perfil actualizado con éxito")
        
        # Redirección forzada al dashboard
        return redirect('dashboard')

    return render(request, 'core/perfil.html', {'perfil': perfil})

@login_required
def dashboard(request):
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