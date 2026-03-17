from django.shortcuts import render
from django.views.generic import TemplateView


class AboutPage(TemplateView):
    template_name = 'pages/about.html'

    
class RulesPage(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    template = 'pages/404.html'
    context = {}
    return render(request, template_name=template, context=context, status=404)


def server_error(request):
    template = 'pages/500.html'
    context = {}
    return render(request, template_name=template, context=context, status=500)


def csrf_error(request, exception):
    template = 'pages/403csrf.html'
    context = {}
    return render(request, template_name=template, context=context, status=403)
