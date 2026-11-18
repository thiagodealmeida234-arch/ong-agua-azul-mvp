from django.urls import path
from . import views

urlpatterns = [
    path('entrar/', views.AcessoLoginView.as_view(), name='login'),
    path('sair/', views.AcessoLogoutView.as_view(), name='logout'),
    path('', views.InicioView.as_view(), name='inicio'),
    path('familias/', views.FamiliaListaView.as_view(), name='familia_lista'),
    path('familias/nova/', views.FamiliaCriarView.as_view(), name='familia_criar'),
    path('familias/<int:pk>/inativar/', views.FamiliaInativarView.as_view(), name='familia_inativar'),
    path('campanhas/', views.CampanhaListaView.as_view(), name='campanha_lista'),
    path('campanhas/nova/', views.CampanhaCriarView.as_view(), name='campanha_criar'),
    path('campanhas/<int:pk>/', views.CampanhaResumoView.as_view(), name='campanha_resumo'),
    path('campanhas/<int:pk>/encerrar/', views.CampanhaEncerrarView.as_view(), name='campanha_encerrar'),
    path('doacoes/nova/', views.DoacaoCriarView.as_view(), name='doacao_criar'),
]
