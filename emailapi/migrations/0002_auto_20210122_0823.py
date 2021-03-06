# Generated by Django 3.0.5 on 2021-01-22 08:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='email',
            name='to',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), size=None),
        ),
    ]
