from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from .models import *
from .forms import OrderForm
from .filters import OrderFilter


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending, 'total_customers': total_customers}
    return render(request, 'account/dashboard.html', context)


def products(request):
    product = Product.objects.all()
    return render(request, 'account/products.html', {'products': product})


def customer(request, pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    order_count = orders.count()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    context = {'customer': customers, 'orders': orders,
               'order_count': order_count, 'my_filter': my_filter}
    return render(request, 'account/customer.html', context)


def createorder(request, pk):
    order_form_set = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customers = Customer.objects.get(id=pk)
    formset = order_form_set(queryset=Order.objects.none(), instance=customers)
    if request.method == 'POST':
        formset = order_form_set(request.POST, instance=customers)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'account/order_form.html', context)


def updateorder(request, pk):
    form = OrderForm()
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'account/order_form.html', context)


def deleteorder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'account/delete.html', context)
