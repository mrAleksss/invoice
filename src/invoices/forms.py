from django import forms
from .models import Invoice
from django.core.exceptions import ValidationError



class InvoiceForm(forms.ModelForm):
    completion_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='дата підписання')
    issue_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='дата отримання замовлення')
    payment_day = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='дата оплати')
    class Meta:
        model = Invoice
        fields = ('receiver', 'number', 'completion_date', 'issue_date', 'payment_day')
        
        labels = {
            'receiver':'отримувач',
            'number': 'номер договору',
        }
        
        
    def clean_number(self):
        number = self.cleaned_data.get('number')
        if len(number) < 10:
            raise ValidationError('Занадто короткий номер договору')
        else:
            return number
        

