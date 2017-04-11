from django import forms
from django.forms import Select

from .models import Data


class CarForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['license_plate', 'category', ]
        labels = {'license_plate': 'სახელმწიფო ნომერი', 'category': 'კატეგორია'}

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
        widgets = {'category': Select(choices=category_choices)}


class DeleteCarForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = []
