from django.shortcuts import render


def data_generator(request):
    return render(request, 'dantes_data_generator/data_generator.html')
