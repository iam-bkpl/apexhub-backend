# Generated by Django 4.1 on 2023-06-28 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_customuser_enrollment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_authorized_to_external',
            field=models.BooleanField(default=False),
        ),
    ]
