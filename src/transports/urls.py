from django.urls import path

from .views import form, week

app_name = "transports"
urlpatterns = [
    path("form/", form, name="form-creation"),
    path("form/<int:pk>", form, name="form"),
    path('tyzden/', week, name="week")
]
