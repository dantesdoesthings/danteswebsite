from django.shortcuts import render


def index(request):
    return render(request, 'dantes_site/index.html')


def projects(request):
    return render(request, 'dantes_site/projects.html')
