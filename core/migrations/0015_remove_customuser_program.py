# Generated by Django 4.1 on 2023-07-21 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_customuser_enrollment_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='program',
        ),
    ]
