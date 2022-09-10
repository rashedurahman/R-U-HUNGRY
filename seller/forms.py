from django import forms
from django.contrib.auth.models import User 
from seller.models import Menu, Restaurant

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        # exclude = ['is_available']


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'


