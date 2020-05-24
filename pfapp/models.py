from django.db import models
from datetime import date


class Acctype(models.Model):
    u_id = models.ForeignKey('Person', on_delete=models.CASCADE)
    acctypes = models.CharField(max_length=30)

class Person(models.Model):
    email = models.CharField(max_length=30)
    pwd = models.CharField(max_length=30)
    type = models.CharField(max_length=30)

class user_details(models.Model):
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    phoneno = models.CharField(max_length=13)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)


class User_locations(models.Model):
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    locality = models.CharField(max_length=30)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

class Fruits(models.Model):
    name = models.CharField(max_length=30)
    price = models.CharField(max_length=30)
    image = models.FileField(upload_to='static/images')

    def __str__(self):
        return self.name

class products(models.Model):
    name = models.CharField(max_length=30)

class available_contract(models.Model):
    product = models.ManyToManyField(products)
    quantity = models.IntegerField()
    quantity_unit = models.CharField(max_length=15)
    duration = models.IntegerField()
    duration_unit = models.CharField(max_length=10)
    frequency = models.IntegerField()
    frequency_unit = models.CharField(max_length=10)
    price = models.IntegerField()
    price_unit = models.CharField(max_length=30)
    Person = models.ForeignKey('Person', on_delete=models.CASCADE)

