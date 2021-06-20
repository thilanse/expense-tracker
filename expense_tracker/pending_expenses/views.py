from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PendingExpense
from .forms import PendingExpenseForm


@login_required
def home(request):

    form = PendingExpenseForm()
    pending_expenses = get_pending_expenses(request)
    # pending_expenses = [
    #     {
    #         "id": 1,
    #         "expense": "Car stereo system",
    #         "amount": 15000,
    #         "purchased": False
    #     },
    #     {
    #         "id": 2,
    #         "expense": "Sunglasses",
    #         "amount": 8000,
    #         "purchased": False
    #     },
    #     {
    #         "id": 3,
    #         "expense": "Splippers",
    #         "amount": 2000,
    #         "purchased": False
    #     },
    #     {
    #         "id": 4,
    #         "expense": "Shoes",
    #         "amount": 6000,
    #         "purchased": False
    #     }
    # ]

    total_cost = sum([item['amount'] for item in pending_expenses])

    context = {
        "pending_expenses": pending_expenses,
        "total": total_cost,
        "form": form,
    }

    return render(request, "pending_expenses.html", context)


def add_pending_expense(request):
    if request.method == 'POST':
        form = PendingExpenseForm(request.POST)
        form.instance.user = request.user

        if form.is_valid():
            form.save()

    return redirect('pending-expenses')


def get_pending_expenses(request):
    pending_expenses = PendingExpense.objects.filter(user=request.user)

    expenses = []
    for expense in pending_expenses:
        item = {}
        item['expense'] = expense.reason
        item['amount'] = expense.amount
        item['purchased'] = expense.purchased
        expenses.append(item)

    return expenses