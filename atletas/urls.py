from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_atletas, name='lista_atletas'),
    path('atleta/<int:id_atleta>/', views.detalhe_atleta, name='detalhe_atleta'),
    path('atleta/<int:id_atleta>/editar/', views.editar_estatisticas, name='editar_estatisticas'),
    path('atleta/<int:id_atleta>/ajustar/', views.ajustar_estatistica, name='ajustar_estatistica'),
    path('atleta/novo/', views.cadastrar_atleta, name='cadastrar_atleta'),
    path('atleta/<int:id_atleta>/excluir/', views.excluir_atleta, name='excluir_atleta'),
    path('atleta/<int:id_atleta>/editar-nome/', views.editar_atleta, name='editar_atleta'),
    path('atleta/<int:id_atleta>/criar-estatisticas/', views.criar_estatisticas, name='criar_estatisticas'),
]