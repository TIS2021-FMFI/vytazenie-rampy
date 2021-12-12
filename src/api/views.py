from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from transports.models import Transport
from transports.utils import TransportChangeTracker
from .serializers import TransportSerializer


class TransportList(APIView):
    """
    List all transports scheduled in between requested timestamps. Used by fullcalendar.io library.
    """

    def get(self, request, format=None):
        start, end = request.GET.get("start", False), request.GET.get("end", False)
        if not start or not end:
            return Response(status.HTTP_400_BAD_REQUEST)

        # TODO: zobrazit iba nezrusene prepravy
        transports = Transport.find_objects_between_timestamps(start, end)
        serializer = TransportSerializer(transports, many=True)
        return Response(serializer.data)


class TransportUpdate(APIView):
    """
    Update transport's processing datetimes. Used by fullcalendar.io library.
    """

    def get_object(self, pk):
        try:
            return Transport.objects.get(pk=pk)
        except Transport.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        transport = self.get_object(pk)
        serializer = TransportSerializer(transport, data=request.data, partial=True)

        if serializer.is_valid():
            tracker = TransportChangeTracker(
                serializer.validated_data, transport, self.request.user, True
            )

            if not tracker.is_valid():
                return Response(
                    {"status": False, "msg": "Prepravu sa nepodarilo upraviť."}
                )

            tracker.track()
            return Response({"status": True, "msg": "Preprava bola úspešne upravená."})

        return Response({"status": False, "msg": "Prepravu sa nepodarilo upraviť."})
