from django.db import models
from django.conf import settings

# Create your models here.
class Equation(models.Model):
    id = models.AutoField(primary_key=True)
    equation = models.CharField(max_length=255)
    solution = models.CharField(max_length=255)
    type =  models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.equation
