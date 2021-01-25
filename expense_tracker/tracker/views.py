from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm, ExpenseUpdateForm

@login_required
def home(request):
  form = ExpenseForm()
  expenses = Expense.objects.order_by('-date_of_expenditure')
  context = { 'form': form, 'expenses': expenses }
  return render(request, 'tracker/home.html', context)

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

  form = ExpenseForm()
  expenses = Expense.objects.order_by('-date_of_expenditure')
  context = { 
    'expenses': expenses, 
    'update_id': pk, 
    'update_form': update_form,
    'form': form
  }
  return render(request, 'tracker/home.html', context)

def confirm_delete_expense(request, pk):
  form = ExpenseForm()
  expenses = Expense.objects.order_by('-date_of_expenditure')
  context = { 
    'expenses': expenses, 
    'delete_id': pk, 
    'form': form
  }
  return render(request, 'tracker/home.html', context)

def delete_expense(request, pk):
  expense_to_delete = Expense.objects.get(id=pk)
  expense_to_delete.delete()
  return redirect('tracker-home')
