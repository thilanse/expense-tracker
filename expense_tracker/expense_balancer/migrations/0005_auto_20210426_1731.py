# Generated by Django 3.1.5 on 2021-04-26 17:31

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_balancer', '0004_contributor_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
