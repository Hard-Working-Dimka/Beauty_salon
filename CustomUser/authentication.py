from django.contrib.auth import get_user_model
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException


class NoPasswordBackend:
    def authenticate(self, request, phonenumber=None):
        User = get_user_model()
        try:
            phonenumber = PhoneNumber.from_string(phonenumber)
        except NumberParseException:
            return None
        if phonenumber.is_valid():
            try:
                user = User.objects.get(phonenumber=phonenumber)
            except User.DoesNotExist:
                user = User(phonenumber=phonenumber)
                user.save()
            return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
