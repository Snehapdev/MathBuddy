from django.db import models

# Create your models here.
class Equation(models.Model):
    id = models.AutoField(primary_key=True)
    equation = models.CharField(max_length=255)
    solution = models.CharField(max_length=255)
    #user_id = models.ForeignKey('Users', on_delete=models.CASCADE)

    def __str__(self):
        return self.equation