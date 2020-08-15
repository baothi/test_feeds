from django import forms
from .models import *
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','type' :'text'}),
            'description': forms.Textarea(attrs={'class': 'form-control','type' :'text'}),
            'website': forms.TextInput(attrs={'class': 'form-control','type' :'text'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'publish': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
        	'name' : forms.Select(attrs={'class': 'form-control'})
        }