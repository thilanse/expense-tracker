from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Expense(models.Model):
    amount = models.FloatField()
    reason = models.CharField(max_length=100)
    date_of_expenditure = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rs. {self.amount} spent on {self.reason}"
