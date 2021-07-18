from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_tag = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Expense(models.Model):
    amount = models.FloatField()
    reason = models.CharField(max_length=100)
    date_of_expenditure = models.DateTimeField(default=timezone.now)
    purchased = models.BooleanField(default=True)
    is_pending = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"Rs. {self.amount} spent on {self.reason}"
