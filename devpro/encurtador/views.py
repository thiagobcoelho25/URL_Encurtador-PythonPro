from devpro.encurtador.models import UrlRedirect
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.

def redirecionar(requisição, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    return redirect(url_redirect.destino)

def relatorios(requisição, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    url_reduzida = requisição.build_absolute_uri(f'/{slug}')
    contexto = {'reduce': url_redirect, 'url_reduzida' : url_reduzida}
    return render(requisição, 'encurtador/relatorio.html', contexto)
