from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','vacation_days','ms_graph_id')
        read_only_fields = ('id','vacation_days','ms_graph_id')  # saldo lo maneja el sistema
