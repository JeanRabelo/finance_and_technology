from django.urls import path
from . import views

app_name = 'processing'

urlpatterns = [
    path('buscar_fundo/', views.buscaFundo_view, name = 'buscar_fundo'),
    path('escolher_fundo/', views.escolherFundo_view, name = 'escolher_fundo'),
    path('fundo_178347/', views.fundo178347_view, name = 'fundo_178347'),
]
