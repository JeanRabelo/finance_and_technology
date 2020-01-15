import re

def lista_fundos(soup):
    lista = []

    soup_fundos = soup.find_all('tr')

    for soup_fundo in soup_fundos:
        soup_fundo_detalhes = soup_fundo.find_all('td')
        dicionario = dict()
        dicionario['cnpj'] = soup_fundo_detalhes[0].find('a').string
        dicionario['nome'] = soup_fundo_detalhes[1].find('a').string
        dicionario['tipo_fundo'] = soup_fundo_detalhes[2].string
        dicionario['link_1'] = soup_fundo_detalhes[0].find('a')['href']
        dicionario['link_2'] = soup_fundo_detalhes[1].find('a')['href']
        lista.append(dicionario)

    return lista

def ativos(soup):
    soup_infosPublicas = soup.find(id='dlAplics')
    soup_infosConfidenciais = soup.find(id='trAplicsConf')


    lista_linhasTitulo = [['Ativo', 'Classificação', 'Empresa ligada', 'vendasMês-quant', 'vendasMês-valor',
    'aquisicoesMês-quant', 'aquisicoesMês-valor', 'posiçãoFinal-quant', 'custo', 'mercado', r'% patrim liq']]
    lista_linhasPublicas = []
    lista_linhasConfidenciais = []

    if soup_infosPublicas is not None:
        soup_linhasPublicas = soup_infosPublicas.find_all(bgcolor=re.compile('(?:Cornsilk|#FAEFCA)'))
        print('-----------------soup_linhasPublicas-----------------inicio')
        print(soup_linhasPublicas)
        print('-----------------soup_linhasPublicas-----------------fim')
        for soup_linha in soup_linhasPublicas:
            lista_celulasPublicas = []
            soup_celulas = soup_linha.find_all('td')
            for soup_celula in soup_celulas:
                lista_celulasPublicas.append(soup_celula.get_text())
            lista_linhasPublicas.append(lista_celulasPublicas)

    if soup_infosConfidenciais is not None:
        soup_linhasConfidenciais = soup_infosConfidenciais.find_all(bgcolor=re.compile('(?:#F8DAC7|#FAE5D7)'))
        print('-----------------soup_linhasConfidenciais-----------------inicio')
        print(soup_linhasConfidenciais)
        print('-----------------soup_linhasConfidenciais-----------------fim')
        for soup_linha in soup_linhasConfidenciais:
            lista_celulasConfidenciais = []
            soup_celulas = soup_linha.find_all('td')
            for soup_celula in soup_celulas:
                lista_celulasConfidenciais.append(soup_celula.get_text())
            lista_linhasConfidenciais.append(lista_celulasConfidenciais)

    lista_linhas = lista_linhasTitulo + lista_linhasPublicas + lista_linhasConfidenciais

    from pprint import pprint
    pprint(lista_linhas)

    return lista_linhas
