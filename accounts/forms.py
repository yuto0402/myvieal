from allauth.account.forms import LoginForm, ResetPasswordForm, ResetPasswordKeyForm, SignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from .adapter import CustomAccountAdapter
from .models import CustomUser

UserModel = get_user_model()


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
"""


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "icon_image",
            "username",
            "introduction",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) > 50:
            raise ValidationError("Please limit to 50 characters.")
        return username

    def clean_introduction(self):
        introduction = self.cleaned_data["introduction"]
        if len(introduction) > 500:
            raise ValidationError("Please limit to 500 characters.")
        return introduction


class CustomLoginForm(BaseCustomForm, LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].widget.attrs["placeholder"] = "メールアドレス"
        self.fields["password"].widget.attrs["placeholder"] = "パスワード"


class EmailVerificationCodeForm(forms.Form):
    email_verification_code = forms.CharField(
        label="Verification Code", max_length=4, widget=forms.TextInput(attrs={"placeholder": "認証コード(４ケタ)"})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean_email_verification_code(self):
        code = self.cleaned_data["email_verification_code"]
        stored_code = self.request.session.get("email_verification_code")
        if not stored_code or code != stored_code:
            raise ValidationError("Invalid verification code")
        return code


class EmailConfirmationForm(BaseCustomForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "メールアドレス"

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email, is_active=True):
            raise ValidationError("ユーザーが既に存在しています。")
        return email

    def send_verification_code(self, user_email, email_verification_code):
        """認証コードを含むメールを送信"""
        subject = "Your signup verification code"
        message = f"Your verification code is: {email_verification_code}"
        send_mail(subject, message, "no-reply@yourdomain.com", [user_email])

    def save(self, request):
        email = self.cleaned_data["email"]
        email_verification_code = CustomAccountAdapter._generate_code(self)
        if request.session.get("attempts"):
            del request.session["attempts"]
        request.session["email_verification_code"] = email_verification_code
        request.session["signup_email"] = email
        self.send_verification_code(email, email_verification_code)


class CustomUserCreationForm(BaseCustomForm, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "ユーザー名"
        self.fields["password1"].widget.attrs["placeholder"] = "パスワード"
        self.fields["password2"].widget.attrs["placeholder"] = "パスワード(確認)"


class CustomResetPasswordForm(BaseCustomForm, ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "メールアドレス"


class CustomResetPasswordKeyForm(BaseCustomForm, ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["placeholder"] = "新しいパスワード"
        self.fields["password2"].widget.attrs["placeholder"] = "新しいパスワード(確認)"


class CustomSetPasswordForm(BaseCustomForm, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs["placeholder"] = "新しいパスワード"
        self.fields["new_password2"].widget.attrs["placeholder"] = "新しいパスワード(確認)"


class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(
        label="Verification Code", max_length=4, widget=forms.TextInput(attrs={"placeholder": "認証コード(４ケタ)"})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean_verification_code(self):
        code = self.cleaned_data["verification_code"]
        stored_code = self.request.session.get("verification_code")
        if not stored_code or code != stored_code:
            raise ValidationError("Invalid verification code")
        return code


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "メールアドレス"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not get_user_model().objects.filter(email=email, is_active=True):
            raise ValidationError("ユーザーが存在しません。")
        if get_user_model().objects.filter(email=email, is_active=False):
            raise ValidationError("ユーザーが存在しません。")
        return email

    def send_verification_code(self, user_email, verification_code):
        """認証コードを含むメールを送信"""
        subject = "Your password reset verification code"
        message = f"Your verification code is: {verification_code}"
        send_mail(subject, message, "no-reply@yourdomain.com", [user_email])

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            verification_code = CustomAccountAdapter._generate_code(self)
            self.send_verification_code(user.email, verification_code)

            request.session["verification_code"] = verification_code
            request.session["password_reset_email"] = user_email

            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )


class EmailChangeCodeForm(forms.Form):
    email_change_code = forms.CharField(
        label="Verification Code", max_length=4, widget=forms.TextInput(attrs={"placeholder": "認証コード(４ケタ)"})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean_email_change_code(self):
        code = self.cleaned_data["email_change_code"]
        stored_code = self.request.session.get("email_change_code")
        if not stored_code or code != stored_code:
            raise ValidationError("Invalid verification code")
        return code


class EmailChangeForm(BaseCustomForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "新しいメールアドレス"

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email):
            raise ValidationError("ユーザーが既に存在しています。")
        return email

    def send_verification_code(self, user_email, email_change_code):
        """認証コードを含むメールを送信"""
        subject = "Your email change code"
        message = f"Your email change code is: {email_change_code}"
        send_mail(subject, message, "no-reply@yourdomain.com", [user_email])

    def save(self, request):
        email = self.cleaned_data["email"]
        email_change_code = CustomAccountAdapter._generate_code(self)
        request.session["email_change_code"] = email_change_code
        request.session["new_email"] = email
        self.send_verification_code(email, email_change_code)


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs["placeholder"] = "現在のパスワード"
        self.fields["new_password1"].widget.attrs["placeholder"] = "新しいパスワード"
        self.fields["new_password2"].widget.attrs["placeholder"] = "新しいパスワード(確認)"
