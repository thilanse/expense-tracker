from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Event name:{self.name}"


class Expense(models.Model):
    reason = models.CharField(max_length=255)
    date_of_expenditure = models.DateTimeField(default=timezone.now)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Expense:{self.reason}"


class Contributor(models.Model):
    name = models.CharField(max_length=50)
    total_amount = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"


class Contribution(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Contribution:{self.amount} by {self.contributor}"
