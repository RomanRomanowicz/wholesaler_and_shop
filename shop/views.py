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
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})


def post_message(request, id):
    """question to the store"""
    product = get_object_or_404(Product, id=id, available=True)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(product.get_absolute_url())
            subject = '{} ({}) asks a question: "{}"'.format(cd['your_name'], cd['your_email'], product.name)
            message = 'question: "{}" at {}\n\n{}\'s contents: {}'.format(product.name, post_url, cd['your_name'], cd['question'])
            send_mail(subject, message, 'cop.romanowicz@gmail.com', ['cop.romanowicz@gmail.com', cd['your_email']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'shop/product/message.html', {'product': product, 'form': form, 'sent': sent})