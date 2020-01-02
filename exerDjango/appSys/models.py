from django.db import models

# Create your models here.

class Employee(models.Model):
    jobNumber =     models.CharField(max_length=16)
    name =          models.CharField(max_length=32)