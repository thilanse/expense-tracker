from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tracker.models import Expense, Tag
from tracker.forms import ExpenseForm


@login_required
def home(request):

    form = ExpenseForm()
    pending_expenses = get_pending_expenses(request)
    
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