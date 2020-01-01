from django.shortcuts import render, redirect
from scripts_proprios import funcoes

def home_view(request):
    return render(request, 'home.html')

# def resultado_view(request):
#     if request.method == 'POST':
#         print('foi post')
#         resultado = funcoes.somar(request)
#         print('resultado = ' + str(resultado))
#         return render(request, 'resultado.html', {'resultado': resultado})
#     else:
#         return redirect('home')
