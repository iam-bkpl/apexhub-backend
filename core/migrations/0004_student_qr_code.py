# Generated by Django 4.1 on 2023-06-04 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_student_enrollment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes'),
        ),
    ]
