# Generated by Django 4.1 on 2023-05-29 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ashop', '0003_cart_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]