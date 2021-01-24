from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Expense
from .forms import ExpenseForm

def home(request):
  if request.method == 'POST':
    form = ExpenseForm(request.POST)
    form.instance.user = request.user

    if form.is_valid():
      form.save()
      return redirect('tracker-home')

  else:
    form = ExpenseForm()

  expenses = Expense.objects.order_by('-date_of_expenditure')
  context = { 'form': form, 'expenses': expenses }
  return render(request, 'tracker/home.html', context)
