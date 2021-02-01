from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm, ExpenseUpdateForm

import itertools
import calendar
import datetime

HOME_TEMPLATE = 'tracker/home.html'

@login_required
def home(request):
  return render(request, HOME_TEMPLATE, get_home_context())

def add_expense(request):
  if request.method == 'POST':
    form = ExpenseForm(request.POST)
    form.instance.user = request.user

    if form.is_valid():
      form.save()
  return redirect('tracker-home')


def update_expense(request, pk):
  expense_to_update = Expense.objects.get(id=pk)
  if request.method == 'POST':
    update_form = ExpenseUpdateForm(request.POST, instance=expense_to_update)

    if update_form.is_valid():
      update_form.save()
      return redirect('tracker-home')
  else:
    update_form = ExpenseUpdateForm(instance=expense_to_update)

  context = get_home_context()
  context['update_id'] = pk
  context['update_form'] = update_form

  return render(request, HOME_TEMPLATE, context)

def confirm_delete_expense(request, pk):

  context = get_home_context()
  context['delete_id'] = pk

  return render(request, HOME_TEMPLATE, context)

def delete_expense(request, pk):
  expense_to_delete = Expense.objects.get(id=pk)
  expense_to_delete.delete()
  return redirect('tracker-home')


def get_home_context():
  """
  Creates context required for home page.
  ie, the form and the list of expenses

  """

  form = ExpenseForm()
  expenses = Expense.objects.order_by('-date_of_expenditure')
  expenses = get_expenses(expenses)
  current_annual_total, current_month_total, previous_annual_total, previos_month_total = get_month_cost(expenses)

  context = { 
    'form': form, 
    'expenses': expenses,
    'current_annual_cost': current_annual_total,
    'current_month_cost': current_month_total, 
    'previous_annual_cost': previous_annual_total,
    'previous_month_cost': previos_month_total
  }
  return context

def get_expenses(expenses):

  expenses_grouped_by_year = [{'year': key, 'annual_expenses': list(group)} for key, group in itertools.groupby(expenses, lambda x:x.date_of_expenditure.year)]

  for annual_expense_group in expenses_grouped_by_year:
    annual_expenses = annual_expense_group['annual_expenses']

    expenses_grouped_by_month = [{'month': key, 'month_name': calendar.month_name[key], 'monthly_expenses': list(group)} for key, group in itertools.groupby(annual_expenses, lambda x: x.date_of_expenditure.month)]

    for monthly_expense_group in expenses_grouped_by_month:
      monthly_expenses = monthly_expense_group['monthly_expenses']

      expenses_grouped_by_day = [get_daily_expense(key, list(group), annual_expense_group, monthly_expense_group) for key, group in itertools.groupby(monthly_expenses, lambda x: x.date_of_expenditure.day)]
      monthly_expense_group['monthly_expenses'] = expenses_grouped_by_day
      monthly_expense_group['total_monthly_cost'] = sum(daily_expense['total_daily_cost'] for daily_expense in expenses_grouped_by_day)

    annual_expense_group['annual_expenses'] = expenses_grouped_by_month
    annual_expense_group['total_annual_cost'] = sum(monthly_expense['total_monthly_cost'] for monthly_expense in expenses_grouped_by_month)


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
  monthly_expense = next((expense for expense in annual_expense['annual_expenses'] if expense['month'] == month), None)

  if monthly_expense is None:
    monthly_expense = { 'total_monthly_cost': 0.0 }

  return annual_expense, monthly_expense

def get_month_cost(expenses):

  request_date = datetime.date.today().replace(day=1)
  current_annual_expense, current_monthly_expense = get_specific_month_cost(expenses, request_date.year, request_date.month)

  previous = (request_date - datetime.timedelta(days=1))
  _ , previous_month_cost = get_specific_month_cost(expenses, previous.year, previous.month)

  previous_year = request_date.replace(month=1) - datetime.timedelta(days=1)
  previous_annual_cost , _ = get_specific_month_cost(expenses, previous_year.year, previous_year.month)


  return current_annual_expense['total_annual_cost'], current_monthly_expense['total_monthly_cost'], previous_annual_cost['total_annual_cost'], previous_month_cost['total_monthly_cost']