from django.shortcuts import render

from company.views import photo_list


def main(request):
    """ Homepage"""

    return render(request, 'main/index.html')