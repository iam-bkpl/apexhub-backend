# Generated by Django 4.1 on 2023-06-17 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
