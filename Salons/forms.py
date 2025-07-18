from django import forms
from django.forms import widgets
from phonenumber_field.formfields import PhoneNumberField

from CustomUser.models import User
from Salons.models import Review


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["phone_number", "description", "name"]

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "contacts__form_iunput", "placeholder": "Введите имя"}
        )
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "contacts__form_iunput", "placeholder": "+7(999)999--99-99"}
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "contacts__form_textarea",
                "placeholder": "Ваш вопрос (необязательно)",
            }
        ),
        required=False,
    )


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["phonenumber", "avatar", "name"]
        widgets = {
            "phonenumber": widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите ваш номер телефона",
                    "style": "width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;",
                }
            ),
            "avatar": widgets.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "style": "width: 100%; padding: 10px; border-radius: 5px;",
                }
            ),
            "name": widgets.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите ваше имя",
                    "style": "width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;",
                }
            ),
        }


class AppointmentForm(forms.Form):
    phonenumber = PhoneNumberField(
        region="RU",
        widget=forms.TextInput(
            attrs={
                "class": "contacts__form_iunput",
                "placeholder": "Введите номер телефона",
                "name": "fname",
                "required": "",
            }
        ),
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "contacts__form_iunput",
                "placeholder": "Введите имя",
                "name": "fname",
                "required": "",
            }
        ),
    )
    question = forms.CharField(
        max_length=100,
        widget=forms.Textarea(
            attrs={
                "class": "contacts__form_textarea",
                "placeholder": "Вопрос(необязательно)",
                "name": "fname",
            }
        ),
        required=False,
    )


class PromoForm(forms.Form):
    promo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "contacts__form_iunput",
                "placeholder": "Введите промокод",
                "name": "fname",
            }
        ),
    )