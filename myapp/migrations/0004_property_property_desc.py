# Generated by Django 3.0 on 2021-11-18 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_property'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='property_desc',
            field=models.TextField(default=''),
        ),
    ]
