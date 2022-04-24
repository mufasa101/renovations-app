from rest_framework import serializers
from .models import Unit
from django.utils import timezone

class UnitSerializers(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Unit
        # fields = ['id','unit_name','unit_property','added_on']
        exclude = ['added_by']
    



