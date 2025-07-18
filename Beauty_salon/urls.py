"""
URL configuration for Beauty_salon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from Salons.views import (
    ajax_load_beauty_services,
    ajax_load_salons,
    ajax_load_slots,
    ajax_load_specialists,
    edit_profile,
    payment_success,
    send_payment,
    send_review,
    show_index,
    show_notes,
    show_service,
    show_serviceFinaly,
)

urlpatterns = [
    path("users/", include("CustomUser.urls")),
    path("admin/", admin.site.urls),
    path("", show_index, name="main"),
    path("notes/", show_notes, name="profile"),
    path("service/", show_service, name="service"),
    path(
        "serviceF/<int:service_id>/<specialist_id>/<str:time>/<str:date>/",
        show_serviceFinaly,
        name="serviceFinally",
    ),
    path("ajax_load_salons/", ajax_load_salons, name="ajax_load_salons"),
    path(
        "ajax_load_beauty_services/",
        ajax_load_beauty_services,
        name="ajax_load_beauty_services",
    ),
    path("ajax_load_specialists/", ajax_load_specialists, name="ajax_load_specialists"),
    path("ajax_load_slots/", ajax_load_slots, name="ajax_load_slots"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("send-review/", send_review, name="send_review"),
    path("send_payment/", send_payment, name="send_payment"),
    path("payment_success/", payment_success, name="payment_success"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
