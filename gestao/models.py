from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Familia(models.Model):
    nome_responsavel = models.CharField('Nome do responsável', max_length=100)
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    bairro = models.CharField('Bairro', max_length=60, blank=True)
    numero_membros = models.PositiveIntegerField(
        'Número de membros',
        null=True,
        blank=True,
        validators=[MinValueValidator(1, message='O número de membros deve ser maior que zero.')]
    )
    ativa = models.BooleanField('Ativa', default=True)
    data_cadastro = models.DateField('Data de cadastro', auto_now_add=True)

    class Meta:
        verbose_name = 'Família'
        verbose_name_plural = 'Famílias'
        ordering = ['nome_responsavel']

    def __str__(self):
        return f"{self.nome_responsavel} ({self.telefone or 'Sem telefone'})"


class Campanha(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('encerrada', 'Encerrada'),
    ]

    nome = models.CharField('Nome da campanha', max_length=100)
    descricao = models.CharField('Descrição', max_length=300, blank=True)
    data_inicio = models.DateField('Data de início')
    data_fim = models.DateField('Data final', null=True, blank=True)
    status = models.CharField('Status', max_length=15, choices=STATUS_CHOICES, default='ativa')

    class Meta:
        verbose_name = 'Campanha'
        verbose_name_plural = 'Campanhas'
        ordering = ['-data_inicio', 'nome']

    def clean(self):
        if self.data_fim and self.data_inicio and self.data_fim < self.data_inicio:
            raise ValidationError({'data_fim': 'A data final não pode ser anterior à data de início.'})

    def __str__(self):
        return f"{self.nome} [{self.get_status_display()}]"


class Doacao(models.Model):
    familia = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name='doacoes', verbose_name='Família')
    campanha = models.ForeignKey(Campanha, on_delete=models.PROTECT, related_name='doacoes', verbose_name='Campanha')
    item = models.CharField('Item entregue', max_length=120)
    quantidade = models.PositiveIntegerField(
        'Quantidade',
        validators=[MinValueValidator(1, message='Informe uma quantidade maior que zero.')]
    )
    observacao = models.CharField('Observação', max_length=250, blank=True)
    data_entrega = models.DateTimeField('Data da entrega', auto_now_add=True)
    registrado_por = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Registrado por')

    class Meta:
        verbose_name = 'Doação'
        verbose_name_plural = 'Doações'
        ordering = ['-data_entrega']

    def clean(self):
        if self.campanha_id and self.campanha.status != 'ativa':
            raise ValidationError({'campanha': 'Somente campanhas ativas aceitam novas doações.'})
        if self.familia_id and not self.familia.ativa:
            raise ValidationError({'familia': 'Não é possível registrar doação para família inativa.'})

    def __str__(self):
        return f"{self.familia.nome_responsavel} - {self.quantidade}x {self.item}"
