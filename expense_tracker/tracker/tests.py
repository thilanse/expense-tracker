from django.test import TestCase
from django.contrib.auth.models import User
from .models import Expense


class ExpenseTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username="thilanse", password="t321")
        Expense.objects.create(amount=200, reason="Badminton", user=user)
        Expense.objects.create(amount=3000, reason="Gym Fees", user=user)

    def test_retrieve_expense_1(self):
        expense1 = Expense.objects.get(reason="Badminton")
        self.assertEqual(expense1.reason, 'Badminton')
        self.assertEqual(expense1.amount, 200)
        self.assertEqual(expense1.user.username, "thilanse")

    def test_retrieve_expense_2(self):
        expense1 = Expense.objects.get(reason="Gym Fees")
        self.assertEqual(expense1.reason, 'Gym Fees')
        self.assertEqual(expense1.amount, 3000)
        self.assertEqual(expense1.user.username, "thilanse")
