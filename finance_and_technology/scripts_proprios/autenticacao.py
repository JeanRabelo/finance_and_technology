import requests
from bs4 import BeautifulSoup as BS
from . import aux
import json

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

    # argumentos_aspnet['__EVENTTARGET'] = soup.find(id='__EVENTTARGET')['value']
    argumentos_aspnet['Form1'] = soup.find(id='Form1')['action']
    argumentos_aspnet['__EVENTTARGET'] = 'ddlFundos$_ctl5$Linkbutton4'
    argumentos_aspnet['__EVENTARGUMENT'] = ''
    argumentos_aspnet['__VIEWSTATE'] = soup.find(id='__VIEWSTATE')['value']
    argumentos_aspnet['__VIEWSTATEGENERATOR'] = soup.find(id='__VIEWSTATEGENERATOR')['value']
    argumentos_aspnet['__EVENTVALIDATION'] = soup.find(id='__EVENTVALIDATION')['value']

    with open('argumentos_aspnet.json', 'w') as fp:
        json.dump(argumentos_aspnet, fp)

    return aux.lista_fundos(soup)

def retornar_fundo(request):
    cookie_val_1 = request.POST['cookie_val_1']
    cookie_val_2 = request.POST['cookie_val_2']

    s = requests.Session()
    cookies_jar = requests.cookies.RequestsCookieJar()

    cookies_jar.set('ASP.NET_SessionId', request.POST.get('cookie_val_1'), domain='cvmweb.cvm.gov.br', path='/')
    cookies_jar.set('CVMWebCookie', request.POST.get('cookie_val_2'), domain='cvmweb.cvm.gov.br', path='/')

    with open('argumentos_aspnet.json') as json_file:
        argumentos_aspnet = json.load(json_file)

    url_generica = r'https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/CConsolFdo' + argumentos_aspnet['Form1'][1:]
    del argumentos_aspnet['Form1']

    response_generica = s.post(url_generica, argumentos_aspnet)

    action_str = BS(response_generica.content, 'html.parser').find(id='Form1')['action']
    n_partic = action_str.find('PK_PARTIC')
    num_fundo = action_str[n_partic:(n_partic+16)]

    print('num fundo = ' + num_fundo)
    # num_fundo = r'PK_PARTIC=178347'

    url = r'https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/CDA/CPublicaCDA.aspx?' + num_fundo + '&SemFrame='
    response = s.get(url, cookies=cookies_jar)

    # Opening JSON file

    return aux.ativos(BS(response.content, 'html.parser'))
