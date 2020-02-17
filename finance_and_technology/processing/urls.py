from django.urls import path
from . import views

app_name = 'processing'

urlpatterns = [
    path('buscar_fundo/', views.buscaFundo_view, name = 'buscar_fundo'),
    path('escolher_fundo/', views.escolherFundo_view, name = 'escolher_fundo'),
    path('fundo/', views.fundo_view, name = 'fundo'),
    path('xlsx_composicao_carteira/', views.xlsx_composicao_carteira_view, name = 'xlsx_composicao_carteira'),
]
