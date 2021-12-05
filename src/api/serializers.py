from rest_framework import serializers

from transports.models import Transport, TransportPriority, TransportStatus


class TransportPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportPriority
        fields = '__all__'

class TransportStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportStatus
        fields = '__all__'

class TransportSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField()
    carrier = serializers.StringRelatedField()
    gate = serializers.StringRelatedField()
    transport_priority = TransportPrioritySerializer()
    transport_status = TransportStatusSerializer()
    color = serializers.CharField()

    class Meta:
        model = Transport
        exclude = ['created', 'modified']

