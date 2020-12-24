from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect
import json
import datetime
import time

from .models import *
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from .ultils import cartData, cookieCart, guestOrder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def about(request):
    context = showMiniCart1(request)
    return render(
        request, 'shopping/about-us.html', context
    )


def contact(request):
    context = showMiniCart1(request)
    return render(
        request, 'shopping/contact-us.html', context
    )


def coming_soon(request):
    context = showMiniCart1(request)
    return render(
        request, 'shopping/coming-soon.html', context
    )


def search(request):
    message = ""
    search_form = request.GET.get('search_form', None)
    if search_form:
        all_products = Product.objects.filter(name__contains=search_form)
    else:
        message = "Your product has not found"
        all_products = Product.objects.all()
        print(all_products)
    return render(
        request=request,
        template_name='search.html',
        context={
            'products': all_products,
            'message': message
        }
    )


def index(request):
    cartItems, order, items = showMiniCart(request)
    all_products = Product.objects.all()


    return render(
        request=request,
        template_name='shopping/index-5.html',
        context={
            'products': all_products,
            'cartItems': cartItems,
            'items': items, 
            'orders': order,
         
        }
    )


def view_shop(request):
    cartItems, order, items = showMiniCart(request)
 # Search product name
    name_search = request.GET.get('name_search', None)
    if name_search:
        all_products = Product.objects.filter(name__contains=name_search)
    else:
        all_products = Product.objects.all()
    # Search category name
    # DB hiện có tên hiện xuất hiện 2 lần: GUESS, FENDI,....
    name_category = request.GET.get('name_category', None)
    if name_category:
        category = Category.objects.get(name=name_category)
        all_products = Product.objects.filter(category=category)
    all_categories = Category.objects.filter(category_parent_id__isnull=True)
    list_product_price = [int(i.price) for i in all_products]
    min_price = min(list_product_price)
    max_price = max(list_product_price)

    

    return render(
        request=request,
        template_name='shopping/shop.html',
        context={
            'categories': all_categories,
            'products': all_products,
            'min_price': min_price,
            'max_price': max_price,
            'cartItems': cartItems,
            'items': items, 
            'orders': order,
          
        }
    )


def view_product(request, product_id):

    cartItems, order, items = showMiniCart(request)

    category_data = Category.objects.filter(category_parent_id__isnull=True)
    product_data = Product.objects.get(id=product_id)
    all_products = Product.objects.all()
    product_image = ProductImage.objects.filter(product=product_id)
    return render(
        request=request,
        template_name='shopping/product-simple.html',
        context={
            'category': category_data,
            'product': product_data,
            'products': all_products,
            'product_image': product_image,
            'cartItems': cartItems,
            'items': items, 
            'orders': order
        }
    )

# def view_main(request, product_id):
    category_data = Category.objects.get(id=product_id)
    product_data = Product.objects.get(id=product_id)
    all_products = Product.objects.all()
    return render(
        request=request,
        template_name='shopping/main.html',
        context={
            'category': category_data,
            'product': product_data,
            'products': all_products
        }
    )

def showMiniCart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['orders']
    items = data['items']
    return cartItems,order,items


def register(request):
    data = cartData(request)
    cartItems = data['cartItems']

    message = ""
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            message = "Đăng ký thành công. Xin vui lòng đăng nhập"
            return redirect('login_user')
    else:
        register_form = RegisterForm()
    return render(
        request=request,
        template_name='shopping/register.html',
        context={
            'register_form': register_form,
            
            'cartItems': cartItems
        }

    )


def login_user(request):
    data = cartData(request)
    cartItems = data['cartItems']

    message = ""
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=request.POST['username'], password=request.POST['password'])
            if user:
                login(request, user)
                time.sleep(1)

                return redirect('index')
            else:
                message = "Tên đăng nhập hoặc mật khẩu không đúng."
                print("Tên đăng nhập hoặc mật khẩu không đúng.")
            print("Login succesfull")
            message = "Đăng nhập thành công !"
    else:
        login_form = LoginForm()
    return render(
        request=request,
        template_name='shopping/my-account.html',
        context={
            'login_form': login_form,
            
            'cartItems': cartItems
        }
    )


def shopping_cart(request):

    context = showMiniCart1(request)
    return render(request, 'shopping/cart.html', context)

def showMiniCart1(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['orders']
    items = data['items']
    context = {'items': items, 'orders': order, 'cartItems': cartItems}
    return context


def check_out(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['orders']
    items = data['items']

    context = {'items': items, 'orders': order, 'cartItems': cartItems}
    return render(request, 'shopping/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderDetail, created = OrderDetail.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderDetail.quantity = (orderDetail.quantity + 1)
    elif action == 'remove':
        orderDetail.quantity = (orderDetail.quantity - 1)

    orderDetail.save()

    if orderDetail.quantity <= 0:
        orderDetail.delete()

    return JsonResponse('Mặt hàng đã được thêm', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = data['form']['total']
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            mobile=data['shipping']['mobile'],
        )
    return JsonResponse('Payment complete!', safe=False)


