from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Data
from .forms import CarForm, DeleteCarForm

from django.contrib.auth.decorators import login_required


@login_required
def view_my_cars(request):
    """Returns information on all my cars"""
    my_cars = Data.objects.filter(owner=request.user)

    context = {'my_cars': my_cars}
    return render(request, 'car/my_cars.html', context)


@login_required
def new_car(request):
    """Creates new car"""
    if request.method != 'POST':
        # creating blank form
        car_form = CarForm()
    else:
        # data is being submitted via POST, process data.
        car_form = CarForm(request.POST)
        if car_form.is_valid():
            my_new_car = car_form.save(commit=False)
            my_new_car.owner = request.user
            my_new_car.save()

            return HttpResponseRedirect(reverse('car:view_my_cars'))

    context = {'car_form': car_form}
    return render(request, 'car/new_car.html', context)


@login_required
def delete_car(request, car_id):
    car_to_delete = get_object_or_404(Data, id=car_id)

    if car_to_delete.owner == request.user:
        if request.method == 'POST':
            form = DeleteCarForm(request.POST, instance=car_to_delete)

            if form.is_valid(): # checks CSRF
                car_to_delete.delete()
                return HttpResponseRedirect(reverse('car:view_my_cars'))

        else:
            form = DeleteCarForm(instance=car_to_delete)

    context = {'form': form}
    return render(request, 'car/my_cars.html', context)