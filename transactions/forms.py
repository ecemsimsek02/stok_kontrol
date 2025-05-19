from django import forms
from .models import Purchase


class BootstrapMixin(forms.ModelForm):
    """
    A mixin to add Bootstrap classes to form fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class PurchaseForm(BootstrapMixin, forms.ModelForm):
    """
    A form for updating only the delivery status of a Purchase.
    """
    class Meta:
        model = Purchase
        fields = ['delivery_status']
        widgets = {
            'delivery_status': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }
