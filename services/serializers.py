from rest_framework import serializers
from .models import Request,Service,Cost,Document
from django.utils import timezone

class RequestSerializers(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Request
        # fields = ['id','unit_name','unit_property','added_on']
        exclude = ['added_by']
    


class ServiceSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Service
        exclude = ['added_by']
class CostSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Cost
        exclude = ['added_by']
class DocumentSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Document
        exclude = ['added_by']