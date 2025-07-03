from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import Appointment
from django.utils.timezone import now
from django.shortcuts import redirect
from datetime import datetime

from .forms import QuestionForm, ProfileUserForm

from Salons.models import Salon, Specialist, ServiceType, BeautyService, ClientReview, Review

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
        "past_appointments": past,
    })


def show_service(request):
    error = request.session.pop("error", None)
    show_popup = request.session.get("show_popup", False)
    context = {
        "error": error,
        "show_popup": show_popup
    }
    return render(request, "service.html", context=context)


def show_serviceFinaly(request):
    error = request.session.pop("error", None)
    show_popup = request.session.get("show_popup", False)
    context = {"error": error, "show_popup": show_popup}
    return render(request, "serviceFinally.html", context=context)


def ajax_load_slots(request):
    date = request.GET.get("date", None)
    date_dt = datetime.strptime(date, "%Y-%m-%d")
    specialist_id = request.GET.get("specialist_id", None)
    unavaible_slots = []
    if specialist_id:
        appointment_current_date = Appointment.objects.filter(date=date, specialist__id=specialist_id)
        unavaible_slots += appointment_current_date.values_list('slot', flat=True)
    salon = Salon.objects.first()
    current_time_slot = salon.work_start_at
    slots = {
        "Утро": [],
        "День": [],
        "Вечер": [],
    }
    print(unavaible_slots)
    unavaible_slots = {i.hour for i in unavaible_slots}
    while current_time_slot < salon.work_end_time:
        disabled = (now().time().hour + 3 >= current_time_slot.hour and now().date().day == date_dt.day)or current_time_slot.hour in unavaible_slots
        if current_time_slot.hour < 13:
            slots["Утро"].append({'slot':current_time_slot, 'disabled' : disabled})
        elif current_time_slot.hour < 16:
            slots["День"].append({'slot':current_time_slot, 'disabled' : disabled})
        else:
            slots["Вечер"].append({'slot':current_time_slot, 'disabled' : disabled})
        current_time_slot = current_time_slot.replace(hour=current_time_slot.hour + 1)

    rendered_template = render_to_string(
        "partial_slots.html",
        {"slots": slots},
        request=request
    )
    return JsonResponse({"template": rendered_template}, safe=False)

def ajax_load_salons(request):
    specialist_id = request.GET.get("specialist_id", None)
    service_id = request.GET.get("service_id", None)
    salons = Salon.objects.all()
    if specialist_id:
        salons = salons.filter(specialists__id=specialist_id).distinct()
    if service_id:
        salons = salons.filter(specialists__skills__id=service_id).distinct()
    rendered_template = render_to_string(
        "partial_salons.html",
        {"salons": salons},
        request=request,
    )
    return JsonResponse({"template": rendered_template}, safe=False)


def ajax_load_beauty_services(request):
    salon_id = request.GET.get("salon_id", None)
    specialist_id = request.GET.get("specialist_id", None)
    services = BeautyService.objects.all().select_related("service_type")
    if salon_id:
        services = services.filter(specialists__salon=salon_id).distinct()
    if specialist_id:
        services = services.filter(specialists__id=specialist_id).distinct()
    rendered_template = render_to_string(
        "partial_beauty_services.html",
        {"services": services},
        request=request,
    )
    return JsonResponse({"template": rendered_template}, safe=False)


def ajax_load_specialists(request):
    time = request.GET.get("time", None)
    date = request.GET.get("date", None)
    salon_id = request.GET.get("salon_id", None)
    service_id = request.GET.get("service_id", None)
    specialists = Specialist.objects.all()
    if salon_id:
        specialists = specialists.filter(salon__id=salon_id).distinct()
    if service_id:
        specialists = specialists.filter(skills__id=service_id).distinct()
    if time and date:
        dt_object = datetime.strptime(date.strip()+" "+time.strip()+" +0300", '%a %b %d %Y %H:%M %z')
        specialists = specialists.exclude(
            appointments__date=dt_object.strftime("%Y-%m-%d"),
            appointments__slot=dt_object.strftime('%H:%M')
            )
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
            return redirect('profile')
    else:

        form = ProfileUserForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }
    return render(request, "profile_edit.html", context=context)


@login_required
def send_review(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone_raw = request.POST.get("phone_number", "").strip()
        description = request.POST.get("description", "")
        rating = request.POST.get("rating")
        visit_date_raw = request.POST.get("dateVis")

        visit_date = None
        if visit_date_raw:
            try:
                visit_date = datetime.strptime(visit_date_raw, "%Y-%m-%d").date()
            except ValueError:
                pass

        try:
            appointment = Appointment.objects.filter(
                phone_number=phone_raw,
                date=visit_date
            ).first()

            if appointment and not hasattr(appointment, 'client_rating'):
                ClientReview.objects.create(
                    appointment=appointment,
                    phone_number=phone_raw,
                    review=description,
                    rating=rating,
                )
                return render(request, "review_success.html")
        except ValueError:
            pass

    return redirect("profile")


def send_payment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        tips_amount = request.POST.get('tips_amount')

        if appointment_id:
            appointment = get_object_or_404(Appointment, id=appointment_id)
            appointment.is_paid = True
            appointment.save()
        elif tips_amount:
            print(f"Получены чаевые: {tips_amount}")

        return redirect('payment_success')


def payment_success(request):
    return render(request, "payment_success.html")
