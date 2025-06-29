from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm

from Salons.models import Salon, Specialist, ServiceType, BeautyService, ClientReview


def show_index(request):
    error = request.session.pop("error", None)
    show_popup = request.session.get("show_popup", False)

    salons = list(Salon.objects.all())
    while len(salons) < 4 and salons:
        fake_block = Salon.objects.first()
        fake_block.is_fake = True
        salons.append(fake_block)

    beauty_services = list(BeautyService.objects.all())
    while len(beauty_services) < 4 and beauty_services:
        fake_block = BeautyService.objects.first()
        fake_block.is_fake = True
        beauty_services.append(fake_block)

    reviews = list(ClientReview.objects.all())
    while len(reviews) < 4 and reviews:
        fake_block = ClientReview.objects.first()
        fake_block.is_fake = True
        reviews.append(fake_block)

    specialists = list(Specialist.objects.all())
    for specialist in specialists:  # TODO: посчитать рейтинг! (вставка звездочек)
        total_reviews = 0
        for appointment in specialist.appointments.all():
            total_reviews += appointment.clientreview_set.count()
        specialist.rating = total_reviews

    while len(specialists) < 4 and specialists:
        fake_block = Specialist.objects.first()
        fake_block.is_fake = True
        specialists.append(fake_block)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()

    context = {
        "error": error,
        "show_popup": show_popup,
        "salons": salons,
        "beauty_services": beauty_services,
        "reviews": reviews,
        "specialists": specialists,
        "form": form,
    }
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
