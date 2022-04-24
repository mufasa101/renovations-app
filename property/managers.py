from django.db.models import Q,Count
from django.db import models
class GeneralQuerySet(models.QuerySet):

    def select_option_units(self,lookups=None,except_unit=None):
        
        if except_unit:
            data=self.filter(lookups | Q(id=except_unit)).order_by("unit_number")
        else:
            data=self.filter(lookups).order_by("unit_number")

        output= ['<option selected="" disabled="">Select a property</option>']
        for row in data: 
            output.append(f'<option data-subtext="{row.property_name}" value="{row.id}">unit #{row.unit_number} </option>')    
        output.append(f'<option class="add_property text-primary fancy_text4" data-subtext="Add a new property" >Click to add</option>')   
        return output
class UnitManager(models.Manager):
    def get_queryset(self):
        return GeneralQuerySet(self.model,using=self.db)
   
    def select_option_units(self,status=None,user=None,is_system_admin=False,except_unit=None):
        query = Q()

        if status is not None:
            query &= Q(occupancy_status=status)
        if not is_system_admin:
            print("-------------",user)
            query &= Q(added_by=user)
        


        return self.get_queryset().select_option_units(lookups=query,except_unit=except_unit)