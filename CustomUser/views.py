from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def login_view(request):
    previous_page = request.GET.get('from')
    if request.method == 'POST':
        phonenumber = request.POST.get('phonenumber')
        user = authenticate(request, phonenumber=phonenumber)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            request.session['error'] = 'Invalid phonenumber'
            request.session['show_popup'] = True
            return redirect(previous_page)
    return render(request, 'notes.html')


def logout_view(request):
    logout(request)
    previous_page = request.GET.get('from')
    return redirect(previous_page)
