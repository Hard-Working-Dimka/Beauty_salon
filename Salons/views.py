from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import Appointment
from django.utils.timezone import now

from .forms import QuestionForm, ProfileUserForm

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
    for specialist in specialists:
        total_reviews = 0
        total_rating = 0
        for appointment in specialist.appointments.all():
            if hasattr(appointment, 'client_rating'):
                total_reviews += 1
                total_rating += int(appointment.client_rating.rating)
        if total_reviews == 0:
            total_rating_display = RATING.get(0)
        else:
            total_rating_display = RATING.get(total_rating // total_reviews)

        specialist.rating = total_reviews
        specialist.total_rating = total_rating_display

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


@login_required
def show_notes(request):
    today = now().date()
    user_phone = request.user.phonenumber

    all_appointments = Appointment.objects.filter(
        phone_number=user_phone
    ).select_related('specialist', 'service', 'Promo', 'specialist__salon')

    upcoming = all_appointments.filter(date__gte=today).order_by('date', 'slot')
    past = all_appointments.filter(date__lt=today).order_by('-date', '-slot')

    return render(request, "notes.html", {
        "upcoming_appointments": upcoming,
        "past_appointments": past
    })


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


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    else:

        form = ProfileUserForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }
    return render(request, "profile_edit.html", context=context)
