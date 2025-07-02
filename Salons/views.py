from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .forms import QuestionForm

from Salons.models import Salon, Specialist, ServiceType, BeautyService, ClientReview

RATING = {
    0: '☆☆☆☆☆',
    1: '★☆☆☆☆',
    2: '★★☆☆☆',
    3: '★★★☆☆',
    4: '★★★★☆',
    5: '★★★★★',
}


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
        total_rating = 0
        for appointment in specialist.appointments.all():
            if appointment.client_rating:
                total_reviews += 1
                total_rating += int(appointment.client_rating.rating)
        if total_reviews == 0:
            total_rating = RATING.get(0)
        else:
            total_rating = RATING.get(total_rating // total_reviews)

        specialist.rating = total_reviews
        specialist.total_rating = total_rating

    while len(specialists) < 4 and specialists:
        fake_block = Specialist.objects.first()
        fake_block.is_fake = True
        specialists.append(fake_block)

    form = QuestionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
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
    context = {
        "error": error,
        "show_popup": show_popup,
    }
    return render(request, "service.html", context=context)


def show_serviceFinaly(request):
    error = request.session.pop("error", None)
    show_popup = request.session.get("show_popup", False)
    context = {"error": error, "show_popup": show_popup}
    return render(request, "serviceFinally.html", context=context)


def ajax_load_salons(request):
    salons = Salon.objects.all()
    rendered_template = render_to_string(
        "partial_salons.html",
        {"salons": salons},
        request=request,
    )
    return JsonResponse({"template": rendered_template}, safe=False)


def ajax_load_beauty_services(request):
    salon_id = request.GET.get("salon_id", None)
    services = BeautyService.objects.all().select_related("service_type")
    if salon_id:
        services = services.filter(specialists__salon=salon_id)
    rendered_template = render_to_string(
        "partial_beauty_services.html",
        {"services": services},
        request=request,
    )
    return JsonResponse({"template": rendered_template}, safe=False)


def ajax_load_specialists(request):
    time = request.GET.get("time", None)
    print(time)
    salon_id = request.GET.get("salon_id", None)
    specialists = Specialist.objects.all()
    if salon_id:
        specialists = specialists.filter(salon__id=salon_id)
    rendered_template = render_to_string(
        "partial_specialists.html",
        {"specialists": specialists},
        request=request,
    )
    return JsonResponse({"template": rendered_template}, safe=False)
