# Generated by Django 4.1 on 2023-06-13 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ashop', '0004_rename_date_placed_orderitem_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
