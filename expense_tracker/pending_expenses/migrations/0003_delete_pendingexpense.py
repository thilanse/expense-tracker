# Generated by Django 3.1.5 on 2021-07-18 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pending_expenses', '0002_pendingexpense_purchased'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PendingExpense',
        ),
    ]
