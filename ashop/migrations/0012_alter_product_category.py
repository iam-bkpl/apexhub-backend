# Generated by Django 4.1 on 2023-07-16 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ashop', '0011_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, related_name='products', to='ashop.category'),
        ),
    ]
