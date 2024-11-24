# Create your views here.

from django.views.generic import ListView

from accounts.models import CustomUser


class Following(ListView):
    model = CustomUser
    template_name = "myvieal/following.html"

    def get_queryset(self):
        # returnしたのを宣言するとruff-checkにやめろと言われた
        return self.request.user.following.all()
