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
    dob = models.DateField(max_length=8)

    def age(self):
        today = date.today()

        try:
            birthday = self.dob.replace(year=today.year)
        # raised when birth date is February 29 and the current year is not a leap year
        except ValueError:
            birthday = self.dob.replace(year=today.year, day=born.day-1)

        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

class User_locations(models.Model):
    location = models.CharField(max_length=30)
    u_id = models.ForeignKey('Person', on_delete=models.CASCADE)

class Fruits(models.Model):
    name = models.CharField(max_length=30)
    price = models.CharField(max_length=30)
    image = models.FileField(upload_to='static/images')

    def __str__(self):
        return self.name