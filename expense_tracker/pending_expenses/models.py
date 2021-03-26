from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PendingExpense(models.Model):
    amount = models.FloatField()
    reason = models.CharField(max_length=100)
    date_of_expenditure = models.DateTimeField(default=timezone.now)
    purchased = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reason} for Rs. {self.amount}"
