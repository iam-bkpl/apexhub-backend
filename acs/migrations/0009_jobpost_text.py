# Generated by Django 4.1 on 2023-07-06 10:23

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acs', '0008_alter_jobpost_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
