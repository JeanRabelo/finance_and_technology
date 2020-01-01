from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from scripts_proprios import funcoes

# Create your views here.

@login_required(login_url = '/accounts/login/')
def inputs_view(request):
    return render(request, 'processing/inputs.html')

@login_required(login_url = '/accounts/login/')
def resultadoSoma_view(request):
    if request.method == 'POST':
        resultado = funcoes.somar(request)
        return render(request, 'processing/resultado_soma.html', {'resultado' : resultado})
    else:
        return redirect('accounts:login')
