# Generated by Django 4.1 on 2023-06-14 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ashop', '0006_alter_orderitem_buyer_alter_payment_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='ashop.product'),
        ),
    ]