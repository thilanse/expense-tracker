# Generated by Django 3.1.5 on 2021-06-20 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20210620_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='parent_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tracker.tag'),
        ),
    ]
