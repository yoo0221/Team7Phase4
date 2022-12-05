from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('createuser/', views.create_user, name='create_user'),
    path('shopregister/', views.shop_register, name='shop-register'),
    path('logout/', views.logout, name='logout'),
    path('createshop/', views.create_shop, name='create_shop')
]