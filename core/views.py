from django.views import View
from django.shortcuts import render

class HomeView(View):
    def get(self, request, *args, **kwargs):
        contexto = {'mensaje': '¡Bienvenido al Home!'} #spe
        return render(request, 'home.html', contexto)