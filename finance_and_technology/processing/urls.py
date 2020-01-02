from django.urls import path
from . import views

app_name = 'processing'

urlpatterns = [
    path('buscar_fundo/', views.buscaFundo_view, name = 'buscar_fundo'),
    path('escolher_fundo/', views.escolherFundo_view, name = 'escolher_fundo'),
]
