from django.contrib.auth import get_user_model


class SessionChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        previous_email = request.session.get("signup_email")
        response = self.get_response(request)
        new_email = request.session.get("signup_email")
        if previous_email != new_email and previous_email:
            user_model = get_user_model()
            user = user_model.objects.filter(email=previous_email, is_active=False).first()
            if user:
                user.delete()

        return response
