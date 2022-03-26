from django.shortcuts import render,redirect
from admins.models import *
from django.contrib import messages

def homepage(request):
    context = {
        'activate_home':'active'
    }
    return render(request, 'homepage/home.html', context)


def contactus(request):
    if request.method == 'POST':
        data = request.POST
        Enquiries.objects.create(fullname=data['fullname'],
                                 email=data['email'],
                                 phone=data['phone'],
                                 message=data['message'])
        messages.add_message(request, messages.SUCCESS, 'Enquiry sent successfully.')
        return redirect('/contactus')

    context = {
        'activate_contactus':'active'
    }
    return render(request, 'homepage/contactus.html', context)


