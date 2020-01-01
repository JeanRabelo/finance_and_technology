def somar(request):
    numero_1 = int(request.POST.get('quantity1'))
    numero_2 = int(request.POST.get('quantity2'))
    return (numero_1 + numero_2)
