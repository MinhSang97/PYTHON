from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Product

def view_products(request):
    products = Product.objects.all()
    return render(request, 'snacks/products.html', {'products': products})
