from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Familia, Campanha, Doacao


class MvpOngAguaAzulTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='neia.diretora', password='SenhaForte@2026')
        self.familia = Familia.objects.create(nome_responsavel='Maria Aparecida Souza', telefone='11987654321')
        self.campanha_ativa = Campanha.objects.create(nome='Cesta Básica', data_inicio=date.today(), status='ativa')
        self.campanha_encerrada = Campanha.objects.create(nome='Agasalho', data_inicio=date.today(), status='encerrada')

    def test_rf01_redireciona_sem_login(self):
        resp = self.client.get(reverse('inicio'))
        self.assertEqual(resp.status_code, 302)

    def test_rf04_registra_doacao_valida(self):
        self.client.login(username='neia.diretora', password='SenhaForte@2026')
        resp = self.client.post(reverse('doacao_criar'), {
            'familia': self.familia.pk,
            'campanha': self.campanha_ativa.pk,
            'item': 'Cesta básica completa',
            'quantidade': 1,
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Doacao.objects.count(), 1)

    def test_rf03_bloqueia_campanha_encerrada_e_quantidade_zero(self):
        self.client.login(username='neia.diretora', password='SenhaForte@2026')
        resp = self.client.post(reverse('doacao_criar'), {
            'familia': self.familia.pk,
            'campanha': self.campanha_encerrada.pk,
            'item': 'Cobertor',
            'quantidade': 0,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Doacao.objects.count(), 0)
