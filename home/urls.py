from home.forms import LoginForm
from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about-us$', views.about, name='about_us'),
    url(r'^contact-us$', views.contact, name='contact_us'),
    url(r'^coming-soon$', views.coming_soon, name='coming_soon'),
    url(r'^search$', views.search, name='search_form'),
    url(r'^shop$', views.view_shop, name='view_shop'),
    path('product/<int:product_id>', views.view_product, name='detail'),
    # path('main/<int:product_id>', views.view_main, name='main'),
    path('register/', views.register, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    url(r'^logout$', auth_views.LogoutView.as_view(next_page='/'), name='logout_user'),
    # path('add-to-cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),
    path('checkout/', views.check_out, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process-order/', views.processOrder, name='procees_order'),
]
