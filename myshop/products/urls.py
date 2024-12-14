from django.urls import path
from .views import (login_view, register_view, home_page, user_logout, category_page, view_cart,
                    product_detail, add_to_cart, remove_from_cart, update_cart_item, search, add_review,
                    add_to_favorites, remove_from_favorites, favorites_list)

urlpatterns = [
    path('', home_page, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', user_logout, name='logout'),
    path('categories/<int:pk>/', category_page, name='category'),
    path('view_cart/', view_cart, name='view_cart'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:pk>/<str:action>/', update_cart_item, name='update_cart_item'),
    path('search/', search, name='search'),
    path('product/<int:pk>/add_review/', add_review, name='add_review'),
    path('add_to_favorites/<int:pk>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:pk>/', remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', favorites_list, name='favorites_list'),
]
