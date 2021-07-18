# Generated by Django 3.1.5 on 2021-07-18 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20210620_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='is_pending',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='expense',
            name='purchased',
            field=models.BooleanField(default=True),
        ),
    ]