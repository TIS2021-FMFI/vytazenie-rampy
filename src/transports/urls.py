from django.urls import path
from .views import form, week, day, TableView, view_based_on_user_group, export

urlpatterns = [
    path("", view_based_on_user_group, name="view_based_on_user_group"),
    path("form/", form, name="form-creation"),
    path("form/<int:pk>", form, name="form"),
    path("tyzden/", week, name="week"),
    path("den/", day, name="day"),
    path("tabulka/", TableView.as_view(), name="table"),
    path("export/<str:_format>/", export, name="export"),
]
