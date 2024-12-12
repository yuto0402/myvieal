import string

from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string


class CustomAccountAdapter(DefaultAccountAdapter):
    def _generate_code(self):
        allowed_chars = string.digits
        return get_random_string(length=4, allowed_chars=allowed_chars)

    def generate_unique_username():
        users = get_user_model()
        username = "dummy0"
        counter = 1
        while users.objects.filter(username=username).exists():
            username = f"dummy{counter}"
            counter += 1
        return username
