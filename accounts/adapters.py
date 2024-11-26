import random

from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def generate_emailconfirmation_key(self, emailconfirmation):
        """
        Generates a custom email confirmation code.
        Here, we create a 4-digit numeric code.
        """
        print("確認用")
        return "".join(random.choices("0123456789", k=4))
