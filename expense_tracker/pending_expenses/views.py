from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tracker.models import Expense
from tracker.forms import ExpenseForm


@login_required
def home(request):

    form = ExpenseForm()
    pending_expenses = get_pending_expenses(request)
    
    # total_cost = sum([item['amount'] for item in pending_expenses])

    total_cost = sum(expense.amount for expense in pending_expenses)

    context = {
        "pending_expenses": pending_expenses,
        "total": total_cost,
        "form": form,
    }

    return render(request, "pending_expenses.html", context)


def add_pending_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        form.instance.user = request.user

        if form.is_valid():
            form.instance.purchased = False
            form.instance.is_pending = True
            form.save()

    return redirect('pending-expenses')


def get_pending_expenses(request):
    pending_expenses = Expense.objects.filter(user=request.user, is_pending=True)

    # expenses = []
    # for expense in pending_expenses:
    #     item = {}
    #     item['expense'] = expense.reason
    #     item['amount'] = expense.amount
    #     item['purchased'] = expense.purchased
    #     expenses.append(item)

    expenses = pending_expenses

    return pending_expenses