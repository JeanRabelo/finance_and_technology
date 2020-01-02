import requests
from bs4 import BeautifulSoup as BS

def imagem_e_sessao():
    url_beginning = r'https://cvmweb.cvm.gov.br/SWB//Sistemas/SCW/CPublica/CConsolFdo/FormBuscaParticFdo.aspx'
    s = requests.Session()
    response = s.get(url_beginning)
    soup = BS(response.content, 'html.parser')
    txt_code = soup.find('img').get('src')[2:]
    url_img = "https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica" + txt_code
    response = s.get(url_img)
    print('--------------------')
    cookie_val_1 = s.cookies.get(name='ASP.NET_SessionId', domain='cvmweb.cvm.gov.br')
    print(cookie_val_1)

    cookie_val_2 = s.cookies.get(name='CVMWebCookie', domain='cvmweb.cvm.gov.br')
    print(cookie_val_2)
    print('--------------------')

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

    # cookies_jar.set('name', 'jerry', domain='dev2qa.com', path='/cookies')
    # cookies_jar.set('password', 'jerry888', domain='dev2qa.com', path='/cookies')

    cookies_jar.set('ASP.NET_SessionId', request.POST.get('cookie_val_1'), domain='cvmweb.cvm.gov.br', path='/')
    cookies_jar.set('CVMWebCookie', request.POST.get('cookie_val_2'), domain='cvmweb.cvm.gov.br', path='/')

    url_post = r'https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/CConsolFdo/ResultBuscaParticFdo.aspx?CNPJNome=' + args['txtCNPJNome'] + '&TpPartic=0&Adm=false&numRandom=' + args['numRandom'] + '&SemFrame='
    response = s.post(url_post, args, cookies=cookies_jar)

    return BS(response.content, 'html.parser')
