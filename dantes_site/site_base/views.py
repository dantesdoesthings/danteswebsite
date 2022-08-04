from django.shortcuts import render


def index(request):
    return render(request, 'site_base/index.html')


def projects(request):
    return render(request, 'site_base/projects.html')
