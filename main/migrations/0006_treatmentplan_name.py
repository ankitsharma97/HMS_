# Generated by Django 4.2.13 on 2024-06-23 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_treatment_treatmentplan_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='treatmentplan',
            name='name',
            field=models.CharField(default='Treatment Plan', max_length=100),
        ),
    ]