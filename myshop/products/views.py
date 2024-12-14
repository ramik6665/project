from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm, ReviewForm
from .models import Product, CarouselImage, Category, Cart, CartItem, Favorite

from django.contrib.auth import authenticate, login, logout


def home_page(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    images = CarouselImage.objects.all()
    products_by_category = {category: category.products.first() for category in categories}
    context = {
        'products': products,
        'images': images,
        'categories': categories,
        'products_by_category': products_by_category,
    }
    return render(request, 'products/index.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'products/login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'products/register.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def category_view(request):
    categories = Category.objects.all()
    return render(request, 'products/base.html', {'categories': categories})


def category_page(request, pk):
    sort_query = request.GET.get('sort')
    category = Category.objects.get(pk=pk)
    products = Product.objects.filter(category=category)

    if sort_query:
        posts = products.order_by(sort_query)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/catalog.html', context)

def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


def update_cart_item(request, pk, action):
    cart_item = CartItem.objects.get(pk=pk)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1

    cart_item.save()

    return redirect('view_cart')


def remove_from_cart(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    cart_item.delete()
    return redirect('view_cart')


def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = sum(item.total_price() for item in items)
    return render(request, 'products/view_cart.html', {'cart': cart, 'items': items, 'total_price': total_price})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
    return render(request, 'products/product_detail.html', {
        'product': product,
        'is_favorite': is_favorite,
    })


def search(request):
    query = request.GET.get('q')
    products = []
    if query:
        products = Product.objects.filter(name__icontains=query)

    context = {
        'products': products,
        'query': query
    }
    return render(request, 'products/search_page.html', context)


def add_review(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'products/product_detail.html', {'product': product, 'review_form': form})

def add_to_favorites(request, pk):
    product = Product.objects.get(pk=pk)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect('favorites_list')

def remove_from_favorites(request, pk):
    product = Product.objects.get(pk=pk)
    favorite = Favorite.objects.filter(user=request.user, product=product).first()
    if favorite:
        favorite.delete()
    return redirect('favorites_list')

def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'products/favorites_list.html', {'favorites': favorites})