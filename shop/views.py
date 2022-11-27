from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddProductForm
from .models import Category, Product
from .forms import EmailPostForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, category_slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})


"""zapytanie do sprzedającego"""


def post_message(request):

    send_mail('wiadomość testowa', 'proszę nie zwracać uwagi', 'cop.testow@gmail.com', ['rr.romanowicz@gmail.com'], fail_silently=False)
    return render(request, 'shop/product/message.html')