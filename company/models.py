from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class CarWash(models.Model):
    phone = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User)
    status = models.BooleanField(default=False)
    location = models.PointField(srid=4326, null=True)
    available = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Box(models.Model):
    carwash = models.ForeignKey(CarWash, null=True)
    name = models.CharField(max_length=150)
    status = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'boxes'

    def __str__(self):
        return self.name


@receiver(post_save, sender=Box)
def after_editing_box(sender, instance, **kwargs):
    boxes = Box.objects.filter(carwash=instance.carwash)
    carwash = CarWash.objects.get(id=instance.carwash.id)
    availability = 0
    for box in boxes:
        if box.available:
            availability += 1
    if availability > 0:
        carwash.available = True
    else:
        carwash.available = False
    carwash.save()


class CarWashPhoto(models.Model):
    file = models.ImageField()
    user = models.ForeignKey(User, null=True)
    carwash = models.ForeignKey(CarWash, null=True)
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

