from django.contrib import admin
from .models import (
    ServiceType,
    BeautyService,
    Salon,
    Review,
    Specialist,
    Promo,
    Appointment,
    ClientReview
)


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(BeautyService)
class BeautyServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    pass


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    pass


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass


@admin.register(ClientReview)
class ClientReviewAdmin(admin.ModelAdmin):
    pass
