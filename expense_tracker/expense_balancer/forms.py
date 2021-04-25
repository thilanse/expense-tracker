from django import forms
from .models import Event, Expense, Contributor, Contribution


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['reason']


class ContributorForm(forms.ModelForm):
    class Meta:
        model = Contributor
        fields = ['name']
        exclude = ("event",)


class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['amount']
