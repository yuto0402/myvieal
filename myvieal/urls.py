from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="myvieal/example.html"), name="index"),
    path("2", TemplateView.as_view(template_name="myvieal/example2.html"), name="index2"),
    path("cat", TemplateView.as_view(template_name="myvieal/example_img.html"), name="index3"),
    path("base", TemplateView.as_view(template_name="myvieal/base.html"), name="index4"),
    # ↑これらはちゃんと動くかどうかのテストです。消していいよ
]
