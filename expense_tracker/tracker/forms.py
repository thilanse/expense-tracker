from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'reason', 'date_of_expenditure']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'add-form-field', 'placeholder': 'Amount'}),
            'reason': forms.TextInput(attrs={'class': 'add-form-field mt-3 mb-3', 'placeholder': 'Reason'}),
            'date_of_expenditure': forms.DateInput(attrs={'type': 'date', 'class': 'add-form-field'})
        }


class ExpenseUpdateForm(forms.ModelForm):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'update-form-field'}), label='')
    reason = forms.CharField(widget=forms.TextInput(attrs={'class': 'update-form-field'}), label='')
    date_of_expenditure = forms.DateField(widget=forms.DateInput(attrs={'class': 'update-form-field', 'type': 'date'}),
                                          label='')

    class Meta:
        model = Expense
        fields = ['amount', 'reason', 'date_of_expenditure']
