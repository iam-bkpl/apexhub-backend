# Generated by Django 4.1 on 2023-06-27 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_external_user_remove_student_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True),
        ),
    ]
