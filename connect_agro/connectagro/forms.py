from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
from .models import Product
from .models import Cart

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_producer = forms.BooleanField(label="Are you a producer?", required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Set user role
            UserProfile.objects.filter(user=user).update(is_producer=self.cleaned_data['is_producer'])
        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price']

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1})
        }

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if self.product:
            self.fields['quantity'].widget.attrs['max'] = self.product.quantity

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if self.product and quantity > self.product.quantity:
            raise forms.ValidationError("Quantity exceeds available stock.")
        return quantity

class RemoveCartItemForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label="Quantity to Remove",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'})
    )
