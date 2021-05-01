from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Expense, Contributor, Contribution
from .forms import EventForm, ExpenseForm, ContributorForm, ContributionForm

HOME_TEMPLATE = 'expense_balancer/expense_balancer.html'


@login_required
def home(request):
    context = get_example_context(request)

    return render(request, HOME_TEMPLATE, context)


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()

    form = EventForm()

    context = {
        'event_form': form,
        **get_example_context(request)
    }
    return render(request, HOME_TEMPLATE, context)


@login_required
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
        **get_example_context(request)
    }
    return render(request, HOME_TEMPLATE, context)


@login_required
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
        **get_example_context(request)
    }
    return render(request, HOME_TEMPLATE, context)


@login_required
def add_contribution(request, pk):
    current_expense = Expense.objects.get(id=pk)

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

    # Extract contributors for selected event and create choices for contributors form field
    contributors = Contributor.objects.filter(event=current_expense.event)
    choices = [[contributor.id, contributor.name] for contributor in contributors]

    form = ContributionForm()
    form.fields['contributor'].choices = choices

    context = {
        'contribution_form': form,
        'selected_id': pk,
        **get_example_context(request)
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

    total_amount = sum(expense['total_amount'] for expense in expense_list)

    return expense_list, total_amount


def get_event_transfers(contributors, total_amount):
    cost_per_person = total_amount / len(contributors)

    balances = []
    for contributor in contributors:
        balance = contributor['total_amount'] - Decimal(cost_per_person)
        balances.append({'contributor': contributor['name'], 'balance': int(balance)})

    return _determine_money_transfers(balances)


def _determine_money_transfers(balances):
    balances.sort(key=lambda x: x['balance'])

    creditors = []
    debtors = []
    for balance in balances:
        if balance['balance'] < 0:
            creditors.append(balance)
        else:
            debtors.append(balance)

    creditors.sort(key=lambda x: x['balance'])
    debtors.sort(key=lambda x: x['balance'], reverse=True)

    transfers = []
    for creditor in creditors:
        for debtor in debtors:
            if creditor['balance'] != 0 and debtor['balance'] != 0:
                payment_balance = int(creditor['balance'] + debtor['balance'])
                transfer = {
                    'from': creditor['contributor'],
                    'to': debtor['contributor']
                }
                if payment_balance <= 0:
                    transfer['amount'] = debtor['balance']
                    debtor['balance'] = 0
                    creditor['balance'] = payment_balance
                else:
                    transfer['amount'] = creditor['balance'] * -1
                    debtor['balance'] = payment_balance
                    creditor['balance'] = 0

                transfers.append(transfer)

    return transfers


def get_example_context(request):
    events = Event.objects.filter(user=request.user).order_by('-date_created')
    context = {}
    event_list = []
    for event in events:
        expenses, event_total = get_event_expenses(event)
        contributors = get_event_contributors(event)
        transfers = get_event_transfers(contributors, event_total) if len(contributors) > 0 else []
        event_dict = {
            'id': event.id,
            'name': event.name,
            'contributors': contributors,
            'expenses': expenses,
            'total_amount': event_total,
            'transfers': transfers
        }

        event_list.append(event_dict)

    context['events'] = event_list

    return context


@login_required
def delete_event(request, pk):
    event_to_delete = Event.objects.get(id=pk)
    event_to_delete.delete()
    return redirect('expense-balancer')


@login_required
def delete_event_confirmation(request, pk):
    context = {
        'delete_event_confirmation': True,
        'selected_id': pk,
        **get_example_context(request)
    }
    return render(request, HOME_TEMPLATE, context)


@login_required
def delete_expense(request, pk):
    expense_to_delete = Expense.objects.get(id=pk)

    # Update total amounts for contributors
    contributions = Contribution.objects.filter(expense=expense_to_delete)
    for contribution in contributions:
        contribution.contributor.total_amount -= contribution.amount
        contribution.contributor.save()

    expense_to_delete.delete()
    return redirect('expense-balancer')


@login_required
def delete_expense_confirmation(request, pk):
    context = {
        'delete_expense_confirmation': True,
        'selected_id': pk,
        **get_example_context(request)
    }
    return render(request, HOME_TEMPLATE, context)
