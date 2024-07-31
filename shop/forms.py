from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Order, UserInfo
from django.utils import timezone
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserInfo
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.amount = 1000.00  
        if commit:
            user.save()
        return user

class UserProfileForm(UserChangeForm):
    password1 = forms.CharField(label='新密码', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='确认新密码', widget=forms.PasswordInput, required=False)

    class Meta:
        model = UserInfo
        fields = ['image', 'username', 'email', 'address', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs.update({'class': 'custom-file-input', 'accept': 'image/*'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password1 != password2:
            self.add_error('password2', '两次输入的密码不一致')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')

        if password1:
            user.set_password(password1)

        if commit:
            user.save()
        return user

class PurChaseForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'zip_code', 'tel','quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['zip_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['tel'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        
    def save(self, commit=True):
        order = super().save(commit=False)
        order.order_date = timezone.now()
        order.status = 'Pending'
        if commit:
            order.save()
        return order

class CartOrderForm(forms.ModelForm):
    cart_ids = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Order
        fields = ['address', 'zip_code', 'tel']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['zip_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['tel'].widget.attrs.update({'class': 'form-control'})

    def clean_cart_ids(self):
        cart_ids_str = self.cleaned_data.get('cart_ids', '')
        cart_ids = [int(id) for id in cart_ids_str.split(',') if id]
        return cart_ids
