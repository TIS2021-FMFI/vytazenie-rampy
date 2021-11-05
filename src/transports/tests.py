import datetime

from django.test import TestCase
from .models import Transport, TransportPriority, TransportStatus, Supplier, Gate

# Create your tests here.


class TransportTestCase(TestCase):
    def test_create_valid_transport(self):
        supplier = Supplier("Zadavetel Zadavatelovsky")
        transport_priority = TransportPriority("urgent", "red", 9001)
        transport_status = TransportStatus("Na ceste", "blue", True)

        try:
            Transport(
                "MT309AO",
                "Jožko Mrkvička",
                supplier,
                datetime.date(year=1, month=2, day=3),
                datetime.date(year=1, month=3, day=5),
                True,
                True,
                transport_priority,
                transport_status,
            )
        except:
            self.fail("test_create_valid_transport() raised Exception")
