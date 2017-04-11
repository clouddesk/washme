from PIL import Image
from django import forms
from django.core.files import File

from .models import CarWash, Box, CarWashPhoto
from leaflet.forms.widgets import LeafletWidget


class CarWashForm(forms.ModelForm):
    class Meta:
        model = CarWash
        fields = ['name', 'location', 'phone']
        labels = {'name': 'სამრეცხაოს დასახელება', 'location': 'სამრეცხაოს მდებარეობა',
                  'phone': 'ხელმძღვანელი პირის მობილური ტელეფონის ნომერი'}
        widgets = {'location': LeafletWidget()}


class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['name', 'available']
        labels = {'name': 'სახელი', 'available': 'სტატუსი'}


class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = CarWashPhoto
        fields = ('file', 'x', 'y', 'width', 'height', 'description',)
        labels = {'file': 'ფაილი', 'description': 'აღწერა'}
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo


class DeletePhotoForm(forms.ModelForm):
    class Meta:
        model = CarWashPhoto
        fields = []
