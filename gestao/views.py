from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views import View
from django.db.models import Sum
from django.core.paginator import Paginator
from .models import Familia, Campanha, Doacao
from .forms import FamiliaForm, CampanhaForm, DoacaoForm


class AcessoLoginView(LoginView):
    template_name = 'gestao/login.html'
    redirect_authenticated_user = True


class AcessoLogoutView(LogoutView):
    next_page = 'login'


class InicioView(LoginRequiredMixin, View):
    def get(self, request):
        contexto = {
            'total_familias': Familia.objects.filter(ativa=True).count(),
            'campanhas_ativas': Campanha.objects.filter(status='ativa').count(),
            'campanha_destaque': Campanha.objects.filter(status='ativa').first(),
        }
        return render(request, 'gestao/inicio.html', contexto)


class FamiliaListaView(LoginRequiredMixin, View):
    def get(self, request):
        busca = request.GET.get('q', '').strip()
        familias_qs = Familia.objects.filter(ativa=True)
        if busca:
            familias_qs = familias_qs.filter(nome_responsavel__icontains=busca)
        paginator = Paginator(familias_qs, 15)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request, 'gestao/familia_lista.html', {'page_obj': page_obj, 'busca': busca})


class FamiliaCriarView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'gestao/familia_form.html', {'form': FamiliaForm()})

    def post(self, request):
        form = FamiliaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome_responsavel']
            tel = form.cleaned_data['telefone']
            if Familia.objects.filter(nome_responsavel__iexact=nome, telefone=tel, ativa=True).exists():
                messages.warning(request, 'Atenção: já existe uma família ativa cadastrada com este nome e telefone.')
            form.save()
            messages.success(request, 'Família cadastrada com sucesso.')
            return redirect('familia_lista')
        return render(request, 'gestao/familia_form.html', {'form': form})


class FamiliaInativarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        familia = get_object_or_404(Familia, pk=pk)
        familia.ativa = False
        familia.save()
        messages.info(request, f'Família "{familia.nome_responsavel}" marcada como inativa (histórico preservado).')
        return redirect('familia_lista')


class CampanhaListaView(LoginRequiredMixin, View):
    def get(self, request):
        campanhas = Campanha.objects.all()
        return render(request, 'gestao/campanha_lista.html', {'campanhas': campanhas})


class CampanhaCriarView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'gestao/campanha_form.html', {'form': CampanhaForm()})

    def post(self, request):
        form = CampanhaForm(request.POST)
        if form.is_valid():
            campanha = form.save()
            messages.success(request, f'Campanha "{campanha.nome}" criada com sucesso.')
            return redirect('campanha_resumo', pk=campanha.pk)
        return render(request, 'gestao/campanha_form.html', {'form': form})


class CampanhaEncerrarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        campanha = get_object_or_404(Campanha, pk=pk)
        campanha.status = 'encerrada'
        campanha.save()
        messages.info(request, f'Campanha "{campanha.nome}" encerrada.')
        return redirect('campanha_resumo', pk=campanha.pk)


class CampanhaResumoView(LoginRequiredMixin, View):
    def get(self, request, pk):
        campanha = get_object_or_404(Campanha, pk=pk)
        doacoes_qs = Doacao.objects.filter(campanha=campanha).select_related('familia', 'registrado_por')
        total_itens = doacoes_qs.aggregate(total=Sum('quantidade'))['total'] or 0
        paginator = Paginator(doacoes_qs, 15)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request, 'gestao/campanha_resumo.html', {
            'campanha': campanha,
            'total_itens': total_itens,
            'page_obj': page_obj,
        })


class DoacaoCriarView(LoginRequiredMixin, View):
    def get(self, request):
        initial = {}
        campanha_id = request.GET.get('campanha')
        if campanha_id:
            initial['campanha'] = campanha_id
        form = DoacaoForm(initial=initial)
        return render(request, 'gestao/doacao_form.html', {'form': form})

    def post(self, request):
        form = DoacaoForm(request.POST)
        if form.is_valid():
            doacao = form.save(commit=False)
            doacao.registrado_por = request.user
            doacao.save()
            messages.success(request, 'Doação registrada com sucesso!')
            return redirect('campanha_resumo', pk=doacao.campanha.pk)
        return render(request, 'gestao/doacao_form.html', {'form': form})
