import re
from scripts_proprios import organizar_dadosAux
from pprint import pprint

def extrair_posicionamento(soup):
    # Criar dict
    posicionamento = {}
    try:
        posicionamento['data'] = soup.find(id="ddCOMPTC").find(selected = 'selected').text
    except:
        posicionamento['data'] = 'data com problema'
        print('\n\n\nAmigo, rolou um problema, e ele está explicado abaixo\n\n\n')
        pprint(soup)


    soup_infosPublicas = soup.find(id='dlAplics')
    soup_infosConfidenciais = soup.find(id='trAplicsConf')


    lista_linhasTitulo = [['Ativo', 'Classificação', 'Empresa ligada', 'vendasMês-quant', 'vendasMês-valor',
    'aquisicoesMês-quant', 'aquisicoesMês-valor', 'posiçãoFinal-quant', 'custo', 'mercado', r'% patrim liq']]
    lista_linhasPublicas = []
    lista_linhasConfidenciais = []

    if soup_infosPublicas is not None:
        soup_linhasPublicas = soup_infosPublicas.find_all(bgcolor=re.compile('(?:Cornsilk|#FAEFCA)'))
        for soup_linha in soup_linhasPublicas:
            lista_celulasPublicas = []
            soup_celulas = soup_linha.find_all('td')
            for soup_celula in soup_celulas:
                lista_celulasPublicas.append(organizar_dadosAux.celula_tratada(soup_celula.get_text()))
            lista_linhasPublicas.append(lista_celulasPublicas)

    if soup_infosConfidenciais is not None:
        soup_linhasConfidenciais = soup_infosConfidenciais.find_all(bgcolor=re.compile('(?:#F8DAC7|#FAE5D7)'))
        for soup_linha in soup_linhasConfidenciais:
            lista_celulasConfidenciais = []
            soup_celulas = soup_linha.find_all('td')
            for soup_celula in soup_celulas:
                lista_celulasConfidenciais.append(organizar_dadosAux.celula_tratada(soup_celula.get_text()))
            lista_linhasConfidenciais.append(lista_celulasConfidenciais)

    lista_linhas = lista_linhasTitulo + lista_linhasPublicas + lista_linhasConfidenciais

    posicionamento['carteira'] = lista_linhas

    return posicionamento

def extrair_datas(soup):
    lista_datas = []
    soup_datas = soup.find(id="ddCOMPTC").find_all('option')
    for soup_data in soup_datas:
        data = {}
        data['valor'] = soup_data.text
        data['codigo'] = soup_data.get('value')
        lista_datas.append(data)

    return lista_datas
