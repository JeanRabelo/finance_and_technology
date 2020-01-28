import requests
from bs4 import BeautifulSoup as BS
from . import aux
import json
from random import choice

def imagem_e_sessao():
    url_beginning = r'https://cvmweb.cvm.gov.br/SWB//Sistemas/SCW/CPublica/CConsolFdo/FormBuscaParticFdo.aspx'
    s = requests.Session()
    response = s.get(url_beginning)
    soup = BS(response.content, 'html.parser')
    txt_code = soup.find('img').get('src')[2:]
    url_img = "https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica" + txt_code
    response = s.get(url_img)
    cookie_val_1 = s.cookies.get(name='ASP.NET_SessionId', domain='cvmweb.cvm.gov.br')
    cookie_val_2 = s.cookies.get(name='CVMWebCookie', domain='cvmweb.cvm.gov.br')
    img_data = response.content
    return [img_data, cookie_val_1, cookie_val_2]

def enviar_dados(request):
    args = dict()
    args['txtCNPJNome'] = request.POST.get('nome_ou_cnpj')
    args['ddlTpFdo'] = 0
    args['numRandom'] = request.POST.get('captcha')
    args['btnContinuar'] = 'Continuar >'

    s = requests.Session()
    cookies_jar = requests.cookies.RequestsCookieJar()

    cookies_jar.set('ASP.NET_SessionId', request.POST.get('cookie_val_1'), domain='cvmweb.cvm.gov.br', path='/')
    cookies_jar.set('CVMWebCookie', request.POST.get('cookie_val_2'), domain='cvmweb.cvm.gov.br', path='/')

    url_post = r'https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/CConsolFdo/ResultBuscaParticFdo.aspx?CNPJNome=' + args['txtCNPJNome'] + '&TpPartic=0&Adm=false&numRandom=' + args['numRandom'] + '&SemFrame='
    response = s.post(url_post, args, cookies=cookies_jar)

    soup = BS(response.content, 'html.parser')
    argumentos_aspnet = {}

    argumentos_aspnet['Form1'] = soup.find(id='Form1')['action']
    argumentos_aspnet['EVENTARGUMENT'] = ''
    argumentos_aspnet['VIEWSTATE'] = soup.find(id='__VIEWSTATE')['value']
    argumentos_aspnet['VIEWSTATEGENERATOR'] = soup.find(id='__VIEWSTATEGENERATOR')['value']
    argumentos_aspnet['EVENTVALIDATION'] = soup.find(id='__EVENTVALIDATION')['value']

    return [aux.lista_fundos(soup), argumentos_aspnet]

def retornar_fundo(request):
    cookie_val_1 = request.POST['cookie_val_1']
    cookie_val_2 = request.POST['cookie_val_2']
    link_1 = request.POST['link_1']
    link_2 = request.POST['link_2']

    s = requests.Session()
    cookies_jar = requests.cookies.RequestsCookieJar()

    cookies_jar.set('ASP.NET_SessionId', request.POST.get('cookie_val_1'), domain='cvmweb.cvm.gov.br', path='/')
    cookies_jar.set('CVMWebCookie', request.POST.get('cookie_val_2'), domain='cvmweb.cvm.gov.br', path='/')

    argumentos_aspnet = {}
    argumentos_aspnet['Form1'] = request.POST['argumentos_aspnet_Form1']
    argumentos_aspnet['__EVENTARGUMENT'] = request.POST['argumentos_aspnet___EVENTARGUMENT']
    argumentos_aspnet['__VIEWSTATE'] = request.POST['argumentos_aspnet___VIEWSTATE']
    argumentos_aspnet['__VIEWSTATEGENERATOR'] = request.POST['argumentos_aspnet___VIEWSTATEGENERATOR']
    argumentos_aspnet['__EVENTVALIDATION'] = request.POST['argumentos_aspnet___EVENTVALIDATION']
    argumentos_aspnet['__EVENTTARGET'] = choice([link_1,link_2])

    url_generica = r'https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/CConsolFdo' + argumentos_aspnet['Form1'][1:]

    del argumentos_aspnet['Form1']

    response_generica = s.post(url_generica, argumentos_aspnet)

    argumentos_aspnet['Form1'] = request.POST['argumentos_aspnet_Form1']

    action_str = BS(response_generica.content, 'html.parser').find(id='Form1')['action']
    n_partic = action_str.find('PK_PARTIC')
    num_fundo = action_str[n_partic:(n_partic+16)]

    url = r'https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/CDA/CPublicaCDA.aspx?' + num_fundo + '&SemFrame='
    response = s.get(url, cookies=cookies_jar)

    return [aux.ativos(BS(response.content, 'html.parser')),argumentos_aspnet, request]
