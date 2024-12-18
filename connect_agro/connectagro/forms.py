from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
from .models import Product

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
