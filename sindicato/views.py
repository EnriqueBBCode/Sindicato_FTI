from django.shortcuts import render, redirect
from .models import *
from usuarios.models import *
from datetime import datetime
# Create your views here.

def actas_list(request):
    if request.method == "GET":
        return render(request, 'actas/index.html',{'actas':Acta.objects.all()})

def acta(request,pk):
    acta = Acta.objects.get(pk=pk)
    if request.method == "POST":
        partes_ids = request.POST.getlist('parte')
        print(partes_ids)

        for p in acta.asistencias.all():
            if str(p.id) in partes_ids:
                p.asistencia = True
                print('asistencia')
            else:
                p.asistencia = False
                print('aucencia')

            p.save()
        return redirect('acta',acta.pk)

    else:
        return render(request, 'actas/details.html',{'acta':acta})

def crear_acta(request):
    if request.method == "POST":
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        info = request.POST.get('info')
        usuarios_ids = request.POST.getlist('usuarios')  # Lista de IDs seleccionados

        # Crear la instancia del acta
        acta = Acta.objects.create(
            nombre=nombre,
            info=info,
        )

        # Crear instancias de Parte por cada usuario seleccionado
        for usuario_id in usuarios_ids:
            usuario = Usuario.objects.get(id=usuario_id)
            parte = Parte.objects.create(
                usuario=usuario,
                asistencia=False  # Establecer el valor inicial de asistencia
            )
            acta.asistencias.add(parte)  # Asociar el objeto Parte al acta

        # Guardar el acta
        acta.save()
        
        # Redirigir o mostrar un mensaje
        return redirect('actas')  # Cambiar por el nombre de tu vista o URL de destino

    else:
        usuarios = Usuario.objects.all()
        context = {
            'usuarios':usuarios,
        }
        return render(request, 'actas/crear.html',context)

def crear_cuota(request):
    if request.method == "GET":
        return redirect('home')
    else:
        return render(request,'cuota/crear.html')

def cuotas(request):

    # Obtenemos fecha actual, separamos mes y año
    fecha_actual = datetime.now()
    mes: int = fecha_actual.month
    anno = fecha_actual.year
    # Creo un id con la sintacxis mes.año ej: 5.2025
    mes_id = f"{mes}.{anno}"
    # Obtener el nombre del mes 2 Febrero
    mes_name = meses[mes-1]

    # Creala cuota del mes actual si no existe
    if not Cuota.objects.filter(mes_id=mes_id).exists():
        # Creo el acta con la que se va a controlar los pagos
        acta = Acta.objects.create(
            nombre=f"Pago de la Cuota Sindical de {mes_name} del {anno}",
            info=f'Pagos de la cuota de {mes}/{anno}',
        )
        # Creo un parte por cada usuario del sindicato
        for usuario in Usuario.objects.all():
            parte = Parte.objects.create(
                usuario=usuario,
                asistencia=False  # Establecer el valor inicial de asistencia
            )
            acta.asistencias.add(parte)
            
        # Creo la cuota del mes y le asigno el acta creada
        Cuota.objects.create(
            mes_id = mes_id,
            acta = acta
        )

    # Obtengo todas las cuotas y las ordeno por fecha descendente para que la primera sea la mas reciente
    cuotas = list(Cuota.objects.all().order_by('mes_id'))

    # Buscando usuarios con pagos atrasados
    usuarios_atrasados = []
    for cuota in cuotas:
        cuota.datos_dic = cuota.datos()
        usuarios_atrasados_aux = cuota.usuarios_atrasados()
        if usuarios_atrasados_aux:
            usuarios_atrasados = usuarios_atrasados + usuarios_atrasados_aux
        print(usuarios_atrasados)

    # Almaceno todos los datos que voy a mandar al frontend
    mes_primera_cuota_registrada = int(cuotas[0].mes_id.split('.')[0])
    print(mes_primera_cuota_registrada)
    context = {
        'cuotas' : cuotas,
        'mes':mes,
        'anno':anno,
        'usuarios_atrasados':usuarios_atrasados,
        'meses_restantes':meses[mes:],
        'meses_faltantes':meses[:mes_primera_cuota_registrada-1],
    }

    return render(request,'cuotas/index.html', context)

def cuota(request,pk):
    cuota = Cuota.objects.get(pk=pk)
    context = {
        'cuota' : cuota,
    }
    return render(request,'cuotas/cuota.html', context)

def actualizar_cuota(request,pk):
    acta = Acta.objects.get(pk=pk)
    if request.method == "POST":
        partes_ids = request.POST.getlist('parte')
        print(partes_ids)

        for p in acta.asistencias.all():
            print(p.id)
            if str(p.id) in partes_ids:
                p.asistencia = True
                print('asistencia')
            else:
                p.asistencia = False
                print('aucencia')

            p.save()
        return redirect('cuotas')