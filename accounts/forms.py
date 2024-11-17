from allauth.account.forms import SignupForm
from django import forms


class BaseCustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"
            field.widget.attrs["placeholder"] = ""


class CustomSignupForm(BaseCustomForm, SignupForm):
    icon_image = forms.ImageField(required=True)

    def save(self, request):
        user = super().save(request)
        user.icon_image = self.cleaned_data.get("icon_image")
        user.save()
        return user
