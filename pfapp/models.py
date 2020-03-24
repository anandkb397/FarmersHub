from django.db import models

class Acctype(models.Model):
    acctypes = models.CharField(max_length=30)
    roles = models.CharField(max_length=30)

class Person(models.Model):
    email = models.CharField(max_length=30)
    pwd = models.CharField(max_length=30)
    type = models.CharField(max_length=30)

class Fruits(models.Model):
    name = models.CharField(max_length=30)
    price = models.CharField(max_length=30)
    image = models.FileField(upload_to='static/images')

    def __str__(self):
        return self.name