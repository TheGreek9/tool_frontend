from django.db import models


class TestModel(models.Model):
    firstname = models.CharField(max_length=256, blank=True)
    middlename = models.CharField(max_length=256, blank=True)
    lastname = models.CharField(max_length=256, blank=True)
    dob = models.DateField(blank=True)
    street1address1 = models.CharField(max_length=256, blank=True)
    street2address1 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    state = models.CharField(max_length=256, blank=True)
    zip = models.CharField(max_length=5, blank=True)
    phone1 = models.CharField(max_length=256, blank=True)
    phone2 = models.CharField(max_length=256, blank=True)
    phone3 = models.CharField(max_length=256, blank=True)
    phone4 = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)
