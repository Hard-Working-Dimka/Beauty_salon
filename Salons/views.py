from django.shortcuts import render
from django import forms
from phonenumber_field.formfields import PhoneNumberField


# Create your views here.

def show_index(request):
    error = request.session.pop('error', None)
    show_popup = request.session.get('show_popup', False)
    context = {'error': error, 'show_popup': show_popup}
    return render(request, 'index.html', context=context)

def show_notes(request):
    return render(request, 'notes.html' )

def show_popup(request):
    return render(request, 'popup.html')

def show_service(request):
    return render(request, 'service.html' )

def show_serviceFinaly(request):
    return render(request, 'serviceFinally.html' )