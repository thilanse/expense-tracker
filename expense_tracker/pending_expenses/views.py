from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tracker.models import Expense, Tag
from tracker.forms import ExpenseForm
from datetime import date, datetime


@login_required
def home(request):

    form = ExpenseForm()
    expenses = get_pending_expenses(request)

    pending_expenses = []
    completed_expenses = []
    for expense in expenses:
        if expense.purchased:
            completed_expenses.append(expense)
        else:
            pending_expenses.append(expense)
    
    total_pending_cost = sum(expense.amount for expense in pending_expenses)
    total_completed_cost = sum(expense.amount for expense in completed_expenses)

    context = {
        "pending_expenses": pending_expenses,
        "completed_expenses": completed_expenses,
        "total_pending": total_pending_cost,
        "total_completed": total_completed_cost,
        "form": form,
    }

    return render(request, "pending_expenses.html", context)


def add_pending_expense(request):
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

            expense.purchased = False
            expense.is_pending = True

            expense.save()

    return redirect('pending-expenses')


def get_pending_expenses(request):
    pending_expenses = Expense.objects.filter(user=request.user, is_pending=True)

    return pending_expenses

def complete(request, pk):

    expense = Expense.objects.get(pk=pk)
    expense.purchased = True
    expense.date_of_expenditure = datetime.now()
    expense.save()

    return redirect('pending-expenses')

def undo(request, pk):

    expense = Expense.objects.get(pk=pk)
    expense.purchased = False
    expense.save()

    return redirect('pending-expenses')