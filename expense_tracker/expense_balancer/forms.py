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

    # This is a reference to show that model forms can be initialized with parameters

    # def __init__(self, contributor_choices, *args, **kwargs):
    #     super(ContributionForm, self).__init__(*args, **kwargs)
    #     self.fields['contributor'].choices = contributor_choices

    class Meta:
        model = Contribution
        fields = ['amount', 'contributor']
