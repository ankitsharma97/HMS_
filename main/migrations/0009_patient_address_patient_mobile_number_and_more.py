# Generated by Django 4.2.13 on 2024-06-23 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_woundhealing'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='mobile_number',
            field=models.CharField(blank=True, default='', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='pin_code',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
    ]
