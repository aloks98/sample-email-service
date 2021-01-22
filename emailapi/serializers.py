from rest_framework import serializers
from .models import Email


class EmailSerializer(serializers.ModelSerializer):
    cc = serializers.ListField(default=list)
    class Meta:
        model = Email
        fields = '__all__'