from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("transports/", views.TransportList.as_view(), name="api-transports-list"),
    path(
        "transports/<int:pk>/",
        views.TransportUpdate.as_view(),
        name="api-transports-update",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
