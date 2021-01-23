from django.shortcuts import render
from .models import Expense

def home(request):
  expenses = Expense.objects.all()
  context = { 'expenses': expenses }
  return render(request, 'tracker/home.html', context)
