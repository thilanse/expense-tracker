from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):

  class Meta:
    model = Expense
    fields = ['amount', 'reason']
    widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ExpenseUpdateForm(forms.ModelForm):

  amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control mb-2 mr-sm-2'}), label='')
  reason = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2 mr-sm-2'}), label='')

  class Meta:
    model = Expense
    fields = ['amount', 'reason']
