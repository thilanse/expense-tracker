from django import forms
from .models import PendingExpense


class PendingExpenseForm(forms.ModelForm):
    class Meta:
        model = PendingExpense
        fields = ['reason', 'amount']
