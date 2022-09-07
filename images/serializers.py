from rest_framework import serializers
from .models import *

class imagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = images
        fields=('id', 'converted_url')
