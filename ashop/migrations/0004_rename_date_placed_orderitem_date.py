# Generated by Django 4.1 on 2023-06-13 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ashop', '0003_orderitem_alter_payment_payment_method_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='date_placed',
            new_name='date',
        ),
    ]
