from django.urls import path

from .views import form

app_name = "transports"
urlpatterns = [path("form/", form, name="form")]
