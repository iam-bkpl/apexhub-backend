# Generated by Django 4.1 on 2023-07-01 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ashop', '0009_delete_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
    ]