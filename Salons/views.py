from django.shortcuts import render

def show_index(request):
    return render(request, 'index.html' )

def show_notes(request):
    return render(request, 'notes.html' )

def show_popup(request):
    return render(request, 'popup.html' )

def show_service(request):
    return render(request, 'service.html' )

def show_serviceFinaly(request):
    return render(request, 'serviceFinally.html' )