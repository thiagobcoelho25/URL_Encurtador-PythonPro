from devpro.encurtador.models import UrlLog, UrlRedirect
from django.shortcuts import redirect, render
from django.db.models.functions import TruncDate
from django.db.models import Count

# Create your views here.

def redirecionar(requisição, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    UrlLog.objects.create(
        origem = requisição.META.get('HTTP_REFERER'),
        user_agent = requisição.META.get('HTTP_USER_AGENT'),
        host = requisição.META.get('HTTP_HOST'),
        ip = requisição.META.get('REMOTE_ADDR'),
        url_redirect = url_redirect
    )
    return redirect(url_redirect.destino)

def relatorios(requisição, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    url_reduzida = requisição.build_absolute_uri(f'/{slug}')
    redirecionamentos_por_data = list(
        UrlRedirect.objects.filter(
            slug=slug
        ).annotate(
            data=TruncDate('logs__criado_em')
        ).annotate(
            cliques=Count('data')
        ).order_by('data')
    )
    
    contexto = {'reduce': url_redirect,
    'url_reduzida' : url_reduzida,
    'redirecionamentos_por_data': redirecionamentos_por_data,
    'total_cliques': sum(r.cliques for r in redirecionamentos_por_data)}

    return render(requisição, 'encurtador/relatorio.html', contexto)
