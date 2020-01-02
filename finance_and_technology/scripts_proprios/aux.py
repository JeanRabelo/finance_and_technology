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
