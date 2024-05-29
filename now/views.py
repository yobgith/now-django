from django.shortcuts import render
from store.models import Product


def accueil(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products':products,
    }
    return render(request, 'accueil.html', context)
