from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer_profile/<int:pk>/', views.customer, name="customer"),
    path('create_order/<int:pk>', views.createorder, name="create_order"),
    path('update_order/<int:pk>/', views.updateorder, name="update_order"),
    path('delete_order/<int:pk>/', views.deleteorder, name="delete_order"),

]
