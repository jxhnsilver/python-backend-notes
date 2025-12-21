from django.shortcuts import render


def home_view(request):
    """Главная страница"""
    return render(request, 'home/index.html')