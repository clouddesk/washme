from django.db import models
from django.contrib.auth.models import User


class Data(models.Model):

    sedan = 1
    hatchback = 2
    suv = 3
    big_suv = 4
    category_choices = (
        (sedan, 'სედანი'),
        (hatchback, 'ჰეჩბექი'),
        (suv, 'ჯიპი'),
        (big_suv, 'დიდი ჯიპი'),
    )

    owner = models.ForeignKey(User, null=True)
    license_plate = models.CharField(max_length=7)
    category = models.IntegerField(choices=category_choices, default=sedan)
    date_added = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'data'

    def __str__(self):
        return self.license_plate
