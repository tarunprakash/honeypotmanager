# Generated by Django 3.2.5 on 2021-07-21 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('honeypot_app', '0003_honeypot_activestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='honeypot',
            name='honeypotIP',
            field=models.CharField(default='', max_length=15, unique=True),
        ),
    ]
