from django.contrib import admin
from .models import (
    ServiceType,
    BeautyService,
    Salon,
    BeautyServiceInSalon,
    Review,
    Specialist,
    EXTENSIONpromo,
    Appointment,
    SpecialistSkills,
    SpecialistV2,
    WorkScheduleV2,
    EXTENSIONreview
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


@admin.register(BeautyServiceInSalon)
class BeautyServiceInSalonAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    pass


@admin.register(EXTENSIONpromo)
class EXTENSIONpromoAdmin(admin.ModelAdmin):
    pass


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass


@admin.register(SpecialistSkills)
class SpecialistSkillsAdmin(admin.ModelAdmin):
    pass


@admin.register(SpecialistV2)
class SpecialistV2Admin(admin.ModelAdmin):
    pass


@admin.register(WorkScheduleV2)
class WorkScheduleV2Admin(admin.ModelAdmin):
    pass


@admin.register(EXTENSIONreview)
class EXTENSIONreviewAdmin(admin.ModelAdmin):
    pass
