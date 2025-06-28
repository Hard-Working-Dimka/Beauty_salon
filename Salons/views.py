from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from Salons.models import Salon, Specialist, ServiceType


def show_index(request):
    error = request.session.pop("error", None)
    show_popup = request.session.get("show_popup", False)
    salons = list(Salon.objects.all())
    while len(salons) < 4:
        salons.append(Salon.objects.first())

    context = {"error": error, "show_popup": show_popup, "salons": salons}
    return render(request, "index.html", context=context)


def show_notes(request):
    return render(request, "notes.html")


def show_service(request):
    error = request.session.pop("error", None)
    show_popup = request.session.get("show_popup", False)
    salons = Salon.objects.all()
    service_types = ServiceType.objects.all().prefetch_related("services")
    specialists = Specialist.objects.all()
    context = {
        "error": error,
        "show_popup": show_popup,
        "salons": salons,
        "service_types": service_types,
        "specialists": specialists,
    }
    return render(request, "service.html", context=context)


def show_serviceFinaly(request):
    error = request.session.pop("error", None)
    show_popup = request.session.get("show_popup", False)
    context = {"error": error, "show_popup": show_popup}
    return render(request, "serviceFinally.html", context=context)
