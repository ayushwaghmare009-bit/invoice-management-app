from django import forms 
from .models import invoice

class invoiceForm(forms.ModelForm):
    class Meta:
        model=invoice
        fields=['customer_name','invoice_number','amount','is_paid']
        widgets={
            'customer_name':forms.TextInput(attrs={'class':'form-control'}),
            'invoice_number':forms.TextInput(attrs={'class':'form-control'}),
            'amount':forms.NumberInput(attrs={'class':'form-control'}),
            'is_paid':forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

    def clean_amount(self):
        amount=self.cleaned_data.get('amount')
        if amount==0:
            raise forms.ValidationError('amount must be greater than zero')
        return amount       