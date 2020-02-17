def celula_tratada(texto):
    if texto == r'Paranegociação':
        return r'Para negociação'
    elif texto.replace('-','').replace(',','').replace('.','').isnumeric():
            return texto.replace('.','').replace(',','.')
    else:
        return texto
