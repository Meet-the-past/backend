from rest_framework import serializers
from .models import *

class imagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields=('id', 'converted_url')
