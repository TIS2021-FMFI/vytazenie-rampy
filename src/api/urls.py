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
    path(
        "carriers/create/",
        views.CarrierCreate.as_view(),
        name="api-carriers-create",
    ),
    path(
        "suppliers/create/",
        views.SupplierCreate.as_view(),
        name="api-suppliers-create",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
