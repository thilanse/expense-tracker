from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Expense, Contributor, Contribution
from .forms import EventForm, ExpenseForm, ContributorForm, ContributionForm

HOME_TEMPLATE = 'expense_balancer/expense_balancer.html'


@login_required
def home(request):
    context = get_example_context()

    return render(request, HOME_TEMPLATE, context)


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()

    form = EventForm()

    context = {
        'event_form': form,
        **get_example_context()
    }
    return render(request, HOME_TEMPLATE, context)


def add_contributor(request, pk):
    if request.method == 'POST':
        current_event = Event.objects.get(id=pk)
        print(current_event)
        form = ContributorForm(request.POST)
        if form.is_valid():
            contributor_form = form.save(commit=False)
            contributor_form.event = current_event
            print(form.cleaned_data)
            contributor_form.save()

            return redirect('expense-balancer')

    form = ContributorForm()

    context = {
        'contributor_form': form,
        **get_example_context()
    }
    return render(request, HOME_TEMPLATE, context)


def add_expense(request, pk):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()

    form = ExpenseForm()

    context = {
        'expense_form': form,
        **get_example_context()
    }
    return render(request, HOME_TEMPLATE, context)


def get_example_context():
    context = {
        "events": [
            {
                "id": 1,
                "name": "Trip to Nuwara Eliya | April 2021",
                "contributors": [
                    {
                        "name": "Thilan",
                        "total_amount": 5000
                    },
                    {
                        "name": "Gayathri",
                        "total_amount": 25000
                    },
                    {
                        "name": "Kaveen",
                        "total_amount": 0
                    }
                ],
                "expenses": [
                    {
                        "reason": "Hotel Cost",
                        "total_amount": 30000,
                        "contributions": [
                            {
                                "amount": 5000,
                                "contributor": "Thilan"
                            },
                            {
                                "amount": 25000,
                                "contributor": "Gayathri"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return context
