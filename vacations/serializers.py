from rest_framework import serializers
from decimal import Decimal
from .models import VacationRequest
from django.contrib.auth import get_user_model

User = get_user_model()

class VacationRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = VacationRequest
        fields = ('id','user','start_date','end_date','days_requested','status','created_at','ms_event_id')
        read_only_fields = ('id','status','created_at','ms_event_id')

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')
        if start and end and end < start:
            raise serializers.ValidationError("end_date must be >= start_date")
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = validated_data.pop('user', None)

        # si hay auth se usará request.user; si no, permitimos pasar user en el payload
        if request and getattr(request, 'user', None) and request.user.is_authenticated:
            user = request.user

        if user is None:
            raise serializers.ValidationError("User must be provided (or authenticate).")

        # calcular días si no viene
        if not validated_data.get('days_requested'):
            start = validated_data['start_date']
            end = validated_data['end_date']
            days = (end - start).days + 1  # inclusive
            validated_data['days_requested'] = Decimal(str(days))

        validated_data['user'] = user
        return super().create(validated_data)
