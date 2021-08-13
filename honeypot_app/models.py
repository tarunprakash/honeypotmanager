from django.db import models

# Create your models here.
class Honeypot(models.Model):
    TYPE_CHOICES = [
        ('FTP', 'CanaryFTP'),
        ('SSH', 'CanarySSH'),
        ('HTTP', 'CanaryHTTP'),
        ('MySQL', 'CanaryMySQL')
    ]
    honeypotType = models.CharField(max_length=10, choices=TYPE_CHOICES)
    honeypotIP = models.CharField(max_length=15, default='', unique=True)

    def __str__(self):
        return f'{self.honeypotType}: {self.honeypotIP} (Active: {self.activeStatus})'