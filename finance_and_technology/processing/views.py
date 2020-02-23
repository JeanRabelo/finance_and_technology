from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from scripts_proprios import autenticacao, acessar_info, organizar_dados, excel_related
from base64 import b64encode
from io import BytesIO
from pprint import pprint

import json


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
def xlsx_composicao_carteira_view(request):
    # 1º lugar: pegar composição padrão
    soup_1 = acessar_info.pegar_soup_resposta(request)
    posicionamento = organizar_dados.extrair_posicionamento(soup_1)
    print('Data 1 processada')
    lista_datas = organizar_dados.extrair_datas(soup_1)
    pk_partic = organizar_dados.extrair_pkPartic(soup_1)
    request_2 = autenticacao.atualizar_request(request, soup_1)
    # pprint(lista_datas)

    # 2º lugar: Criar lista de posicionamentos
    historico = [posicionamento]

    # # 3º lugar: append apenas o segundo posicionamento
    # soup_adicional = acessar_info.pegar_soup_resposta(request_2, [lista_datas[1]])[0]
    # posicionamento_adicional = organizar_dados.extrair_posicionamento(soup_adicional)
    # historico.append(posicionamento_adicional)

    # 3º lugar: Append o que tiver a mais
    if len(lista_datas)>1:
        print('Essas são as datas: ')
        pprint(lista_datas)
        soups_adicionais = acessar_info.pegar_soup_resposta(request_2, lista_datas[1:], pk_partic)
        i = 2
        for soup_adicional in soups_adicionais:
            posicionamento_adicional = organizar_dados.extrair_posicionamento(soup_adicional)
            historico.append(posicionamento_adicional)
            print('Data ' + str(i) + ' processada')
            i = i + 1

    # 4º lugar: Colocar histórico no excel e retornar excel
    # ------------ TESTE ------------
    with open('resultado_fundo.txt', 'w') as outfile:
        json.dump(historico, outfile)
    # ----------- TESTOU -----------
    excel = excel_related.colocar_no_excel(historico)
    return excel
