from django.urls import path
from . import views

app_name = 'processing'

urlpatterns = [
    path('inputs/', views.inputs_view, name = 'inputs'),
    path('results/', views.resultadoSoma_view, name = 'resultado_soma'),
]
