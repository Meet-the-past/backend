from rest_framework import serializers
from .models import *

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = images
        fields=('id', 'converted_url')

class PhotoResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = images
        fields=( 'converted_url', 'origin_url')


class TaskIdSerializer(serializers.Serializer):
    task_id = serializers.CharField(help_text="task_id")
    