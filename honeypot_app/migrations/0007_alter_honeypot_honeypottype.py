# Generated by Django 3.2.6 on 2021-08-13 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('honeypot_app', '0006_alter_honeypot_honeypottype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='honeypot',
            name='honeypotType',
            field=models.CharField(choices=[('FTP', 'CanaryFTP'), ('SSH', 'CanarySSH'), ('HTTP', 'CanaryHTTP'), ('MySQL', 'CanaryMySQL')], max_length=10),
        ),
    ]