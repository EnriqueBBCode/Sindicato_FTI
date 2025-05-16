from django.db import models
from datetime import datetime

# Create your models here.
 
meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

class Parte(models.Model):
    usuario = models.ForeignKey("usuarios.Usuario", on_delete=models.CASCADE, related_name='parte')
    asistencia = models.BooleanField(default=False)

class Acta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=250)
    info = models.TextField(blank=True,null=True)
    categoria = models.CharField(max_length=50,default="asistencia")
    asistencias = models.ManyToManyField(Parte,blank=True)

    def cant_usuarios(self):
        return self.asistencias.count()

class Cuota(models.Model):
    # monto = models.PositiveIntegerField()
    mes_id = models.CharField(max_length=50,unique=True) #sintaxys = "mes.2025"
    # usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cuota')
    acta = models.OneToOneField(Acta, on_delete=models.CASCADE)

    def nombre(self):
        mes = int(self.mes_id.split('.')[0])
        anno: str = self.mes_id.split('.')[1]
        return f"{meses[mes-1]} {anno}"
    
    def datos(self):
        pago = 0
        no_pago = 0
        total = 0
        porciento = 0

        for parte in self.acta.asistencias.all():
            total += parte.usuario.cuota()
            if parte.asistencia:
                pago += parte.usuario.cuota()
            else:
                no_pago += parte.usuario.cuota()

        usuarios_pago: int = self.acta.asistencias.filter(asistencia=True).count()
        usuarios: int = self.acta.asistencias.all().count()
        porciento: float = pago/total*100
        porciento_usuarios: float = usuarios_pago/usuarios*100

        return {
            'pago':pago,
            'no_pago':no_pago,
            'total':total,
            'usuarios_pago':usuarios_pago,
            'usuarios':usuarios,
            'porciento':round(porciento),
            'porciento_usuarios':round(porciento_usuarios),
        }
    
    def usuarios_atrasados(self):

        fecha_actual = datetime.now()
        mes = fecha_actual.month
        anno = fecha_actual.year
        # Creo un id con la sintacxis mes.año ej: 5.2025
        mes_id = f"{mes}.{anno}"

        usuarios_atrasados_colection = list(self.acta.asistencias.filter(asistencia=False))
        print(usuarios_atrasados_colection)
        if not self.mes_id == mes_id and len(usuarios_atrasados_colection)>0:
            return usuarios_atrasados_colection
        return False