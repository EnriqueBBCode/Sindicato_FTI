from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic import ListView
from .models import *
from datetime import datetime

class ListarUsuariosView(ListView):
    model = Usuario  # Modelo que se va a listar
    template_name = 'listar_usuarios.html'  # Nombre de la plantilla
    context_object_name = 'usuarios'  # Contexto que usarás en la plantilla

def crear_usuario(request,pk=None):
    usuario = None
    roles = Roll.objects.all()
    if pk:
        usuario = Usuario.objects.get(pk=pk)
    if request.method == "POST":
        nombre = request.POST['nombre']
        solapin = request.POST['solapin']
        correo = request.POST['correo']
        if not usuario:
            password = request.POST['password']
        else:
            try:
                pk_rol = request.POST['rol']
                rol = Roll.objects.get(pk=pk_rol)
                print(rol)
            except:
                rol = None
                
        salario = request.POST['salario']
        username = correo.split('@')[0]
        if usuario:
            usuario.first_name = nombre
            usuario.solapin = solapin
            usuario.email = correo
            usuario.salario = salario
            usuario.username = username
            if rol:
                usuario.roll = rol
            else:
                usuario.roll = None
            usuario.save()
        else:
            Usuario.objects.create_user(
                first_name = nombre,
                solapin = solapin,
                email = correo,
                password = password,
                salario = salario,
                username = username,
            )
        return redirect('usuarios')
    else:
        return render(request,'crear_usuario.html',{'usuario':usuario,'roles':roles})

def eliminar_usuario(request,pk):
    usuario = Usuario.objects.get(pk=pk)
    if request.method == "GET":
        return render(request,'eliminar_usuario.html',{'usuario':usuario})
    if request.method == "POST":
        usuario.delete()
        return redirect('usuarios')
    
def roles(request):
    roles = Roll.objects.all()
    return render(request,'roles.html',{'roles':roles})

def crear_rol(request):
    if request.method == "POST":
        nombre: str = request.POST['nombre']
        usuarios,roles,cuotas,actas,noticias,reportes = [False]*6
        if 'usuarios' in request.POST:
            usuarios = True
        if 'roles' in request.POST:
            roles = True
        if 'cuotas' in request.POST:
            cuotas = True
        if 'actas' in request.POST:
            actas = True
        if 'noticias' in request.POST:
            noticias = True
        if 'reportes' in request.POST:
            reportes = True

        rol:Roll = Roll.objects.create(
            nombre = nombre,
            gestionar_usuarios = usuarios,
            gestionar_roles = roles,
            gestionar_cuotas = cuotas,
            gestionar_actas = actas,
            gestionar_noticias = noticias,
            gestionar_reportes = reportes,
        )
        return redirect('roles')
    else:
        return render(request,'crear_rol.html')

def eliminar_rol(request,pk):
    rol = Roll.objects.get(pk=pk)
    if request.method == "GET":
        return render(request,'eliminar_rol.html',{'rol':rol})
    if request.method == "POST":
        rol.delete()
        return redirect('roles')