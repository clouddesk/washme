from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import CarWash, Box, CarWashPhoto

from .forms import CarWashForm, BoxForm, PhotoForm, DeletePhotoForm

from django.core.serializers import serialize


def view_car_washes(request):
    """Returns list of Car Washes"""
    car_washes = CarWash.objects.order_by('date_added')

    context = {'car_washes': car_washes}
    return render(request, 'company/view_car_washes.html', context)


def view_car_wash(request, car_wash_id):
    """Returns information on selected Car Wash"""
    car_wash = CarWash.objects.get(phone=car_wash_id)
    boxes = car_wash.box_set.all()
    photos = CarWashPhoto.objects.filter(carwash=car_wash)

    context = {'car_wash': car_wash, 'boxes': boxes, 'photos': photos}
    return render(request, 'company/view_car_wash.html', context)


@login_required
def new_car_wash(request):
    """Creates new car wash"""
    if request.method != 'POST':
        # creating blank form
        form = CarWashForm()
    else:
        # data is being submitted via POST, process data.
        form = CarWashForm(request.POST)
        if form.is_valid():
            new_car_wash = form.save(commit=False)
            new_car_wash.user = request.user
            new_car_wash.save()
            return HttpResponseRedirect(reverse('company:view_car_washes'))

    context = {'form': form}
    return render(request, 'company/new_car_wash.html', context)


@login_required
def new_box(request, company_id):
    """add box to carwash company"""
    profile = CarWash.objects.get(id=company_id)
    if request.method != 'POST':
        # create blank form
        form = BoxForm()
    else:
        form = BoxForm(data=request.POST)
        if form.is_valid():
            new_box = form.save(commit=False)
            new_box.company = profile
            new_box.save()
            return HttpResponseRedirect(reverse('company:company', args=[company_id]))

    context = {'form': form, 'company': profile}
    return render(request, 'company/new_box.html', context)


@login_required
def edit_box(request, box_id):
    """This is to edit existing box status"""
    box = Box.objects.get(id=box_id)
    company = box.company

    if request.method != 'POST':
        # blank form is being created
        form = BoxForm(instance=box)
    else:
        # process modified data
        form = BoxForm(instance=box, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('company:company', args=[company.id]))

    context = {'box': box, 'form': form}
    return render(request, 'company/edit_box.html', context)


def company_dataset(request):
    companies = serialize('geojson', CarWash.objects.all())
    return HttpResponse(companies, content_type='json')


def photo_list(request, car_wash_id):
    mycarwash = CarWash.objects.get(phone=car_wash_id)
    photos = CarWashPhoto.objects.filter(carwash=mycarwash)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_photo = form.save()
            uploaded_photo.user = request.user
            uploaded_photo.carwash = mycarwash
            uploaded_photo.save()
            return redirect('company:photo_list', car_wash_id)
    else:
        form = PhotoForm()

    context = {'form': form, 'photos': photos, 'carwash': mycarwash}
    return render(request, 'company/car_wash_photos.html', context)


@login_required
def photo_delete(request, car_wash_id):
    photo_to_delete = get_object_or_404(CarWashPhoto, carwash=car_wash_id)

    if photo_to_delete.user == request.user:
        if request.method == 'POST':
            delete_form = DeletePhotoForm(request.POST, instance=photo_to_delete)

            if delete_form.is_valid():  # checks CSRF
                photo_to_delete.delete()
                return HttpResponseRedirect(reverse('company:photo_list', args=[car_wash_id]))

        else:
            delete_form = DeletePhotoForm(instance=photo_to_delete)

    context = {'delete_form': delete_form}
    return render(request, 'company/car_wash_photos.html', context)
