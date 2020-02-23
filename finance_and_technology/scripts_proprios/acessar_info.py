import requests
from bs4 import BeautifulSoup as BS
from . import aux
from random import choice
from pprint import pprint

def pegar_soup_resposta(request, lista_datas = None, num_fundo = None):
    # Checar se é pra pegar mais de um posicionamento:
    if lista_datas is None:
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

        print('Data 1 acessada')

        return BS(response.content, 'html.parser')
    else:
        soups_adicionais = []
        i = 2
        for data in lista_datas:
            print('Entramos na data ' + str(i))

            link_1 = request.POST['link_1']
            link_2 = request.POST['link_2']

            s = requests.Session()
            cookies_jar = requests.cookies.RequestsCookieJar()

            cookies_jar.set('ASP.NET_SessionId', request.POST.get('cookie_val_1'), domain='cvmweb.cvm.gov.br', path='/')
            cookies_jar.set('CVMWebCookie', request.POST.get('cookie_val_2'), domain='cvmweb.cvm.gov.br', path='/')

            argumentos_aspnet = {}
            argumentos_aspnet['Form1'] = request.POST['argumentos_aspnet_Form1']
            argumentos_aspnet['__EVENTTARGET'] = 'ddCOMPTC'
            argumentos_aspnet['__EVENTARGUMENT'] = request.POST['argumentos_aspnet___EVENTARGUMENT']
            argumentos_aspnet['__LASTFOCUS'] = ''
            argumentos_aspnet['__VIEWSTATE'] = request.POST['argumentos_aspnet___VIEWSTATE']
            argumentos_aspnet['__VIEWSTATEGENERATOR'] = request.POST['argumentos_aspnet___VIEWSTATEGENERATOR']
            argumentos_aspnet['__EVENTVALIDATION'] = request.POST['argumentos_aspnet___EVENTVALIDATION']
            argumentos_aspnet['ddCOMPTC'] = data['codigo']

            # url_generica = r'https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/CConsolFdo' + argumentos_aspnet['Form1'][1:] + r'&SemFrame='
            # print('Argumentos aspnet form 1')
            # pprint(argumentos_aspnet['Form1'])
            # n_partic = argumentos_aspnet['Form1'].find('PK_PARTIC')
            # num_fundo = argumentos_aspnet['Form1'][n_partic:(n_partic+16)]
            # print('Num fundo do artica (PK_PARTIC) do artica = ' + str(num_fundo))
            # url_generica = r'https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/CDA/CPublicaCDA.aspx?' + num_fundo + '&SemFrame='
            # action_str = BS(response_generica.content, 'html.parser').find(id='Form1')['action']
            del argumentos_aspnet['Form1']

            # response_generica = s.post(url_generica, argumentos_aspnet)
            # print('<<<argumentos_aspnet>>>')
            # pprint(argumentos_aspnet)
            # pprint(BS(response_generica.content, 'html.parser'))

            # argumentos_aspnet['Form1'] = request.POST['argumentos_aspnet_Form1']

            # action_str = BS(response_generica.content, 'html.parser').find(id='Form1')['action']
            # n_partic = action_str.find('PK_PARTIC')
            # num_fundo = action_str[n_partic:(n_partic+16)]
            # num_fundo = 'PK_PARTIC=179448'
            # n_partic = action_str.find('PK_PARTIC')
            # num_fundo = action_str[n_partic:(n_partic+16)]
            url = r'https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/CDA/CPublicaCDA.aspx?' + num_fundo + '&SemFrame='
            # ESSA É CLARAMENTE A PARTE MAIS PROBLEMÁTICA DO CÓDIGO INTEIRO!!!- INICIO
            response = s.post(url, argumentos_aspnet, cookies=cookies_jar)
            # ESSA É CLARAMENTE A PARTE MAIS PROBLEMÁTICA DO CÓDIGO INTEIRO!!! - FIM
            soups_adicionais.append(BS(response.content, 'html.parser'))
            print('Data ' + str(i) + ' acessada')
            i = i + 1
        return soups_adicionais


def retornar_fundo(request):
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

    return BS(response.content, 'html.parser')
