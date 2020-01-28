from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from scripts_proprios import autenticacao
from base64 import b64encode
import csv


# Create your views here.

@login_required(login_url = '/accounts/login/')
def buscaFundo_view(request):
    [img_data, cookie_val_1, cookie_val_2] = autenticacao.imagem_e_sessao()
    imagem_captcha = b64encode(img_data).decode("utf-8")

    return render(request, 'processing/buscar_fundo.html', {'imagem_captcha' : imagem_captcha, 'cookie_val_1': cookie_val_1, 'cookie_val_2': cookie_val_2})

@login_required(login_url = '/accounts/login/')
def escolherFundo_view(request):
    if request.method == 'POST':
        enviar_dados_resultado =  autenticacao.enviar_dados(request)
        lista_fundos = enviar_dados_resultado[0]
        argumentos_aspnet = enviar_dados_resultado[1]
        cookie_val_1 = request.POST['cookie_val_1']
        cookie_val_2 = request.POST['cookie_val_2']
        return render(request, 'processing/escolher_fundo.html', {'lista_fundos' : lista_fundos, 'cookie_val_1': cookie_val_1, 'cookie_val_2': cookie_val_2, 'argumentos_aspnet': argumentos_aspnet})
    else:
        return redirect('processing:buscar_fundo')

@login_required(login_url = '/accounts/login/')
def fundo_view(request):
    if request.method == 'POST':
        [response, argumentos_aspnet, request_old] = autenticacao.retornar_fundo(request)
        table_header = response[0]
        table_content = response[1:]
        return render(request, 'processing/fundo.html', {'table_header': table_header,
        'table_content': table_content,
        'argumentos_aspnet': argumentos_aspnet,
        'cookie_val_1': request_old.POST.get('cookie_val_1'),
        'cookie_val_2': request_old.POST.get('cookie_val_2')})
    else:
        return redirect('processing:buscar_fundo')

@login_required(login_url = '/accounts/login/')
def csv_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="generico.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow([request.POST.get('argumentos_aspnet_Form1'), 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
