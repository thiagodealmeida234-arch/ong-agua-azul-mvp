from django import forms
from .models import Familia, Campanha, Doacao


class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        fields = ['nome_responsavel', 'telefone', 'bairro', 'numero_membros']
        widgets = {
            'nome_responsavel': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '(11) 99999-9999'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ex.: Água Azul'}),
            'numero_membros': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': '1'}),
        }


class CampanhaForm(forms.ModelForm):
    class Meta:
        model = Campanha
        fields = ['nome', 'descricao', 'data_inicio', 'data_fim']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control form-control-lg', 'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-control form-control-lg', 'type': 'date'}),
        }


class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['familia', 'campanha', 'item', 'quantidade', 'observacao']
        widgets = {
            'familia': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'campanha': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'item': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ex.: Cesta básica completa'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': '1', 'value': '1'}),
            'observacao': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['familia'].queryset = Familia.objects.filter(ativa=True)
        self.fields['campanha'].queryset = Campanha.objects.filter(status='ativa')
