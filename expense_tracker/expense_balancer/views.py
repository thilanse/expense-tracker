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
        form = ContributorForm(request.POST)
        if form.is_valid():
            contributor_form = form.save(commit=False)
            contributor_form.event = current_event
            contributor_form.save()
            return redirect('expense-balancer')

    context = {
        'contributor_form': ContributorForm(),
        'selected_id': pk,
        **get_example_context()
    }
    return render(request, HOME_TEMPLATE, context)


def add_expense(request, pk):
    if request.method == 'POST':
        current_event = Event.objects.get(id=pk)
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense_form = form.save(commit=False)
            expense_form.event = current_event
            expense_form.save()
            return redirect('expense-balancer')

    context = {
        'expense_form': ExpenseForm(),
        'selected_id': pk,
        **get_example_context()
    }
    return render(request, HOME_TEMPLATE, context)


def add_contribution(request, expense_pk):
    current_expense = Expense.objects.get(id=expense_pk)

    if request.method == 'POST':
        form = ContributionForm(request.POST)

        if form.is_valid():

            # Retrieve selected contributor
            contributor_name = form.cleaned_data['contributor']
            contributor = Contributor.objects.filter(name=contributor_name, event=current_expense.event).first()

            # Update total amount for contributor
            contributor.total_amount += form.cleaned_data['amount']
            contributor.save()

            # Save contribution
            contribution_form = form.save(commit=False)
            contribution_form.expense = current_expense
            contribution_form.contributor = contributor
            contribution_form.save()
            return redirect('expense-balancer')

        else:
            print("form is invalid")

    # Extract contributors for selected event and create choices for contributors form field
    contributors = Contributor.objects.filter(event=current_expense.event)
    choices = [[contributor.id, contributor.name] for contributor in contributors]
    # choices = ["", "-----"] + choices
    form = ContributionForm()
    form.fields['contributor'].choices = choices
    form.fields['contributor'].initial = "-----"

    context = {
        'contribution_form': form,
        'selected_id': expense_pk,
        **get_example_context()
    }
    return render(request, HOME_TEMPLATE, context)


def get_event_contributors(event):
    contributors = Contributor.objects.filter(event=event)
    contributor_list = []
    for contributor in contributors:
        contributor_dict = {
            'id': contributor.id,
            'name': contributor.name,
            'total_amount': contributor.total_amount
        }
        contributor_list.append(contributor_dict)

    return contributor_list


def format_contributions(contributions):
    contribution_list = []
    for contribution in contributions:
        contribution_dict = {
            'id': contribution.id,
            'amount': contribution.amount,
            'contributor': contribution.contributor.name
        }
        contribution_list.append(contribution_dict)

    return contribution_list


def get_event_expenses(event):
    expenses = Expense.objects.filter(event=event)
    expense_list = []
    for expense in expenses:
        contributions = Contribution.objects.filter(expense=expense)
        expense_dict = {
            'id': expense.id,
            'reason': expense.reason,
            'date_of_expenditure': expense.date_of_expenditure,
            'total_amount': sum(contribution.amount for contribution in contributions),
            'contributions': format_contributions(contributions)
        }
        expense_list.append(expense_dict)

    return expense_list


def get_example_context():
    events = Event.objects.all().order_by('-date_created')
    context = {}
    event_list = []
    for event in events:
        event_dict = {
            'id': event.id,
            'name': event.name,
            'contributors': get_event_contributors(event),
            'expenses': get_event_expenses(event)
        }
        event_list.append(event_dict)

    context['events'] = event_list

    # context = {
    #     "events": [
    #         {
    #             "id": 1,
    #             "name": "Trip to Nuwara Eliya | April 2021",
    #             "contributors": [
    #                 {
    #                     "name": "Thilan",
    #                     "total_amount": 5000
    #                 },
    #                 {
    #                     "name": "Gayathri",
    #                     "total_amount": 25000
    #                 },
    #                 {
    #                     "name": "Kaveen",
    #                     "total_amount": 0
    #                 }
    #             ],
    #             "expenses": [
    #                 {
    #                     "id": 1,
    #                     "reason": "Hotel Cost",
    #                     "total_amount": 30000,
    #                     "contributions": [
    #                         {
    #                             "amount": 5000,
    #                             "contributor": "Thilan"
    #                         },
    #                         {
    #                             "amount": 25000,
    #                             "contributor": "Gayathri"
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     ]
    # }
    return context