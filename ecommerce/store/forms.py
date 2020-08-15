from django import forms
from django.forms import ModelForm

from .models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['creator','is_hide','created']
        widgets = {
            'title'         :forms.TextInput(attrs={'class':'form-control','placeholder':'Product name ...'}),
            'description'   :forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            'price'         :forms.NumberInput(attrs={'class':'form-control','min':'1','placeholder':'$$ USD'}),
            'quantity'      :forms.NumberInput(attrs={'class':'form-control','min':'1','placeholder':'Quantity ...'}),
            'category'      :forms.Select(attrs={'class':'form-control'})
        }
