from django.shortcuts import render
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth
from shopping.models import ListaCompra
from catalog.models import Tienda, MaestroProducto

@login_required
def estadisticas(request):
    ahora = timezone.now()
    perfil = request.user.perfilusuario
    listas_usuario = ListaCompra.objects.filter(usuario=request.user, esta_finalizada=True)

    gasto_mes = listas_usuario.filter(
        fecha_finalizada__month=ahora.month,
        fecha_finalizada__year=ahora.year
    ).aggregate(Sum('total_ticket'))['total_ticket__sum'] or 0

    presupuesto = perfil.presupuesto_mensual or 0
    porcentaje_consumido = 0
    restante = 0
    excedente = 0

    if presupuesto > 0:
        gasto_float = float(gasto_mes)
        ppto_float = float(presupuesto)
        porcentaje_consumido = (gasto_float / ppto_float) * 100
        if gasto_float > ppto_float:
            excedente = gasto_float - ppto_float
            restante = 0
        else:
            restante = ppto_float - gasto_float
            excedente = 0

    historial_meses = (
        listas_usuario
        .annotate(mes=TruncMonth('fecha_finalizada'))
        .values('mes')
        .annotate(total=Sum('total_ticket'))
        .order_by('-mes')
    )

    top_productos = MaestroProducto.objects.filter(
        usuario=request.user, 
        frecuencia_uso__gt=0
    ).order_by('-frecuencia_uso')[:5]

    tiendas_stats = Tienda.objects.filter(usuario=request.user).annotate(
        total_gastado=Sum('listacompra__total_ticket', filter=Q(listacompra__esta_finalizada=True)),
        num_visitas=Count('listacompra', filter=Q(listacompra__esta_finalizada=True))
    ).filter(num_visitas__gt=0).order_by('-total_gastado')

    context = {
        'gasto_mes': gasto_mes,
        'presupuesto': presupuesto,
        'porcentaje': min(porcentaje_consumido, 100),
        'restante': restante,
        'excedente': excedente,
        'historial_meses': historial_meses,
        'top_productos': top_productos,
        'tiendas_stats': tiendas_stats,
        'mes_nombre': ahora.strftime('%B'),
        'perfil': perfil,
    }
    return render(request, 'analytics/estadisticas.html', context)