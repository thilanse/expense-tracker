from django.contrib import admin
from .models import Expense, Tag

admin.site.register(Expense)
admin.site.register(Tag)
