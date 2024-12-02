from allauth.account.forms import LoginForm, ResetPasswordForm, ResetPasswordKeyForm, SignupForm
from django import forms
from .models import CustomUser


class BaseCustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["autocomplete"] = "off"


class CustomSignupForm(BaseCustomForm, SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "メールアドレス"
        self.fields["username"].widget.attrs["placeholder"] = "ユーザー名"
        self.fields["password1"].widget.attrs["placeholder"] = "パスワード"
        self.fields["password2"].widget.attrs["placeholder"] = "パスワード(確認)"

"""
icon_image = forms.ImageField(required=True)

    def save(self, request):
        user = super().save(request)
        user.icon_image = self.cleaned_data.get("icon_image")
        user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "icon_image",
            "username",
            "introduction",
        )
        
"""


class CustomLoginForm(BaseCustomForm, LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].widget.attrs["placeholder"] = "メールアドレス"
        self.fields["password"].widget.attrs["placeholder"] = "パスワード"


class CustomResetPasswordForm(BaseCustomForm, ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "メールアドレス"


class CustomResetPasswordKeyForm(BaseCustomForm, ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["placeholder"] = "新しいパスワード"
        self.fields["password2"].widget.attrs["placeholder"] = "新しいパスワード(確認)"
