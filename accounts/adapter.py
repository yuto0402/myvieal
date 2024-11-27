import string

from allauth.account.adapter import DefaultAccountAdapter
from django.utils.crypto import get_random_string


class CustomAccountAdapter(DefaultAccountAdapter):
    def _generate_code(self):
        allowed_chars = string.digits
        return get_random_string(length=4, allowed_chars=allowed_chars)
