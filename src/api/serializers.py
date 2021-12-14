from rest_framework import serializers

from transports.models import Carrier, Supplier, Transport, TransportPriority, TransportStatus


class TransportPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportPriority
        fields = "__all__"


class TransportStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportStatus
        fields = "__all__"

class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = "__all__"

    def create(self, validated_data):
        return Carrier.objects.create(**validated_data)

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"

    def create(self, validated_data):
        return Supplier.objects.create(**validated_data)

class TransportSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField()
    carrier = serializers.StringRelatedField()
    gate = serializers.StringRelatedField()
    transport_priority = TransportPrioritySerializer()
    transport_status = TransportStatusSerializer()
    color = serializers.CharField()

    class Meta:
        model = Transport
        exclude = ["created", "modified"]
