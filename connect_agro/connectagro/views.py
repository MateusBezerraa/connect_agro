from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse
from .models import UserProfile, Product, Inventory
from .forms import ProductForm, UserRegistrationForm

class CustomLoginView(LoginView):
    """
    Custom LoginView to redirect users based on their role.
    """
    def get_success_url(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        if user_profile.is_producer:
            return reverse('product_list')  # Redirect to product management for producers
        return reverse('producer_list')  # Redirect to producers list for consumers


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    return render(request, 'home.html')

@login_required
def product_list(request):
    if not request.user.userprofile.is_producer:
        return HttpResponseForbidden("You do not have permission to view this page.")
    products = Product.objects.filter(created_by=request.user)
    return render(request, 'product_list.html', {'products': products})

@login_required
def product_create(request):
    if not request.user.userprofile.is_producer:
        return HttpResponseForbidden("You do not have permission to create products.")
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    if not request.user.userprofile.is_producer:
        return HttpResponseForbidden("You do not have permission to edit this product.")
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})


@login_required
def producer_list(request):
    producers = UserProfile.objects.filter(is_producer=True)
    return render(request, 'producer_list.html', {'producers': producers})

@login_required
def producer_page(request, username):
    producer = get_object_or_404(UserProfile, user__username=username)
    products = Product.objects.filter(created_by=producer.user)
    return render(request, 'producer_page.html', {'producer': producer, 'products': products})
