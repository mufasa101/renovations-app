
# Register your models here.
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Unit





@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display=('id','property_name','unit_number','unit_type','added_through')
    list_filter=('property_name','unit_number','unit_type')
    search_fields=['property_name','unit_number','unit_type']