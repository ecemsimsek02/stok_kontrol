from django import forms
from .models import Disinfectant, Material, DisinfectantRecipe

class DisinfectantForm(forms.ModelForm):
    class Meta:
        model = Disinfectant
        fields = ['name', 'quantity_in_stock']


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'quantity_in_stock', 'unit']


class DisinfectantRecipeForm(forms.ModelForm):
    class Meta:
        model = DisinfectantRecipe
        fields = ['disinfectant', 'material', 'quantity']
