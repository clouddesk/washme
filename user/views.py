from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


@login_required
def logout_view(request):
    """Finishing working session"""
    logout(request)
    return HttpResponseRedirect(reverse('main:main'))


def register(request):
    """Registers new user"""
    if request.method != 'POST':
        # Show blank registration form
        user_form = UserCreationForm()

    else:
        # Process filled form data
        user_form = UserCreationForm(data=request.POST)

        if user_form.is_valid():
            new_user = user_form.save()

            # Perform login and redirect to homepage
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('main:main'))

    context = {'user_form': user_form}
    return render(request, 'user/register.html', context)
