from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm, ExpenseUpdateForm

import itertools
import calendar

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
  context = { 'form': form, 'expenses': get_expenses(expenses) }
  return context

def get_expenses(expenses):

  expenses_grouped_by_year = [{'year': key, 'annual_expenses': list(group)} for key, group in itertools.groupby(expenses, lambda x:x.date_of_expenditure.year)]

  for annual_expense_group in expenses_grouped_by_year:
    annual_expenses = annual_expense_group['annual_expenses']

    expenses_grouped_by_month = [{'month': key, 'month_name': calendar.month_name[key], 'monthly_expenses': list(group)} for key, group in itertools.groupby(annual_expenses, lambda x: x.date_of_expenditure.month)]

    for monthly_expense_group in expenses_grouped_by_month:
      monthly_expenses = monthly_expense_group['monthly_expenses']

      expenses_grouped_by_day = [{'day': key, 'week_day_name': get_weekday(annual_expense_group, monthly_expense_group, key), 'daily_expenses': list(group)} for key, group in itertools.groupby(monthly_expenses, lambda x: x.date_of_expenditure.day)]
      monthly_expense_group['monthly_expenses'] = expenses_grouped_by_day

    annual_expense_group['annual_expenses'] = expenses_grouped_by_month


  return expenses_grouped_by_year
  

def get_weekday(annual_expense_group, monthly_expense_group, day):
  weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  weekday_idx = calendar.weekday(annual_expense_group['year'], monthly_expense_group['month'], day)
  return weekdays[weekday_idx]
