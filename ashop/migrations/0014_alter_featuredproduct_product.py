# Generated by Django 4.1 on 2023-07-16 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ashop', '0013_featuredproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featuredproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ashop.product'),
        ),
    ]