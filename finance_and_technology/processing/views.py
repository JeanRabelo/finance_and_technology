from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from scripts_proprios import autenticacao
from base64 import b64encode
from pprint import pprint

# Create your views here.

@login_required(login_url = '/accounts/login/')
def buscaFundo_view(request):
    [img_data, cookie_val_1, cookie_val_2] = autenticacao.imagem_e_sessao()
    imagem_captcha = b64encode(img_data).decode("utf-8")

    return render(request, 'processing/buscar_fundo.html', {'imagem_captcha' : imagem_captcha, 'cookie_val_1': cookie_val_1, 'cookie_val_2': cookie_val_2})

@login_required(login_url = '/accounts/login/')
def escolherFundo_view(request):
    if request.method == 'POST':
        # print(request.POST)
        # print(type(request.POST['sessao']['s']))
        lista_fundos = autenticacao.enviar_dados(request)
        pprint(lista_fundos)
        return render(request, 'processing/escolher_fundo.html', {'lista_fundos' : lista_fundos})
    else:
        return redirect('processing:buscar_fundo')
