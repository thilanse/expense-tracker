from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Expense, Tag
from .forms import ExpenseForm, ExpenseUpdateForm

import itertools
import calendar
import datetime

HOME_TEMPLATE = 'home.html'


@login_required
def home(request):
    return render(request, HOME_TEMPLATE, get_home_context(request))


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        form.instance.user = request.user

        if form.is_valid():
            amount = form.cleaned_data['amount']
            reason = form.cleaned_data['reason']
            date_of_expenditure = form.cleaned_data['date_of_expenditure']

            expense = Expense.objects.create(
                amount=amount,
                reason=reason,
                date_of_expenditure=date_of_expenditure,
                user=request.user
            )

            for tag in request.POST['tagsString'].split(","):
                tag = tag.strip().lower()
                tag, _ = Tag.objects.get_or_create(name=tag)
                expense.tags.add(tag)

            expense.save()

    return redirect('tracker-home')


@login_required
def update_expense(request, pk):
    expense_to_update = Expense.objects.get(id=pk)
    if request.method == 'POST':
        update_form = ExpenseUpdateForm(request.POST, instance=expense_to_update)

        if update_form.is_valid():
            update_form.save()
            return redirect('tracker-home')
    else:
        update_form = ExpenseUpdateForm(instance=expense_to_update)

    context = get_home_context(request)
    context['update_id'] = pk
    context['update_form'] = update_form

    return render(request, HOME_TEMPLATE, context)


@login_required
def confirm_delete_expense(request, pk):
    context = get_home_context(request)
    context['delete_id'] = pk

    return render(request, HOME_TEMPLATE, context)


@login_required
def delete_expense(request, pk):
    expense_to_delete = Expense.objects.get(id=pk)
    expense_to_delete.delete()
    return redirect('tracker-home')


def get_home_context(request):
    """
    Creates context required for home page.
    ie, the form and the list of expenses

    """

    form = ExpenseForm()
    expenses = Expense.objects.filter(user=request.user).order_by('-date_of_expenditure')
    expenses = get_expenses(expenses)
    current_annual_total, current_month_total, previous_annual_total, previous_month_total = get_month_cost(expenses)
    tag_expenses = get_tag_expenses()

    context = {
        'form': form,
        'expenses': expenses,
        'current_annual_cost': current_annual_total,
        'current_month_cost': current_month_total,
        'previous_annual_cost': previous_annual_total,
        'previous_month_cost': previous_month_total,
        'tag_expenses_aggregate': tag_expenses
    }
    return context

def get_tag_expenses():

    tags = Tag.objects.all()

    tag_details = []
    for tag in tags:
        tag_total = Expense.objects.filter(tags__in=[tag]).aggregate(Sum('amount'))
        print(tag_total)
        if tag_total['amount__sum']:
            tag_info = {}
            tag_info['tag'] = tag.name
            tag_info['total'] = tag_total['amount__sum']
            tag_details.append(tag_info)

    tag_details = sorted(tag_details, key=lambda x: x['total'], reverse=True)

    for detail in tag_details:
        print(detail['tag'], detail['total'])

    return tag_details


def get_expenses(expenses):
    expenses_grouped_by_year = [{'year': key, 'annual_expenses': list(group)} for key, group in
                                itertools.groupby(expenses, lambda x: x.date_of_expenditure.year)]

    for annual_expense_group in expenses_grouped_by_year:
        annual_expenses = annual_expense_group['annual_expenses']

        expenses_grouped_by_month = [
            {'month': key, 'month_name': calendar.month_name[key], 'monthly_expenses': list(group)} for key, group in
            itertools.groupby(annual_expenses, lambda x: x.date_of_expenditure.month)]

        for monthly_expense_group in expenses_grouped_by_month:
            monthly_expenses = monthly_expense_group['monthly_expenses']

            expenses_grouped_by_day = [get_daily_expense(key, list(group), annual_expense_group, monthly_expense_group)
                                       for key, group in
                                       itertools.groupby(monthly_expenses, lambda x: x.date_of_expenditure.day)]
            monthly_expense_group['monthly_expenses'] = expenses_grouped_by_day
            monthly_expense_group['total_monthly_cost'] = sum(
                daily_expense['total_daily_cost'] for daily_expense in expenses_grouped_by_day)

        annual_expense_group['annual_expenses'] = expenses_grouped_by_month
        annual_expense_group['total_annual_cost'] = sum(
            monthly_expense['total_monthly_cost'] for monthly_expense in expenses_grouped_by_month)

    return expenses_grouped_by_year


def get_weekday(annual_expense_group, monthly_expense_group, day):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_idx = calendar.weekday(annual_expense_group['year'], monthly_expense_group['month'], day)
    return weekdays[weekday_idx]


def get_total_cost(expenses):
    return sum(expense.amount for expense in expenses)


def get_daily_expense(day, expenses, annual_expense_group, monthly_expense_group):
    daily_expense_object = {
        'day': day,
        'week_day_name': get_weekday(annual_expense_group, monthly_expense_group, day),
        'total_daily_cost': get_total_cost(expenses),
        'daily_expenses': expenses
    }

    return daily_expense_object


def get_specific_month_cost(expenses, year, month):
    annual_expense = next((expense for expense in expenses if expense['year'] == year), None)

    if annual_expense is not None:
        monthly_expense = next((expense for expense in annual_expense['annual_expenses'] if expense['month'] == month),
                               None)

        if monthly_expense is None:
            monthly_expense = {'total_monthly_cost': 0.0}
    else:
        monthly_expense = {'total_monthly_cost': 0.0}
        annual_expense = {'total_annual_cost': 0.0}

    return annual_expense, monthly_expense


def get_month_cost(expenses):
    request_date = datetime.date.today().replace(day=1)
    current_annual_expense, current_monthly_expense = get_specific_month_cost(expenses, request_date.year,
                                                                              request_date.month)

    previous = (request_date - datetime.timedelta(days=1))
    _, previous_month_cost = get_specific_month_cost(expenses, previous.year, previous.month)

    previous_year = request_date.replace(month=1) - datetime.timedelta(days=1)
    previous_annual_cost, _ = get_specific_month_cost(expenses, previous_year.year, previous_year.month)

    return current_annual_expense['total_annual_cost'], current_monthly_expense['total_monthly_cost'], \
           previous_annual_cost['total_annual_cost'], previous_month_cost['total_monthly_cost']
