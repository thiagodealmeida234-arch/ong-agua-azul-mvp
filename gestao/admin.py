from django.contrib import admin
from .models import Familia, Campanha, Doacao

@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ('nome_responsavel', 'telefone', 'bairro', 'ativa', 'data_cadastro')
    list_filter = ('ativa', 'bairro')
    search_fields = ('nome_responsavel', 'telefone')

@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'data_inicio', 'data_fim')
    list_filter = ('status',)

@admin.register(Doacao)
class DoacaoAdmin(admin.ModelAdmin):
    list_display = ('familia', 'campanha', 'item', 'quantidade', 'data_entrega', 'registrado_por')
    list_filter = ('campanha',)
