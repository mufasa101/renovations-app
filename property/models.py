from django.db import models
from django.conf import settings
from django.urls import reverse
from .managers import UnitManager


User=settings.AUTH_USER_MODEL

class Unit(models.Model):
    unit_number=models.IntegerField()
    property_name = models.CharField(max_length=75,blank=True, null=True)
    unit_designation = models.CharField(max_length=75,blank=True, null=True)
    unit_type = models.CharField(max_length=35)
    unit_category = models.CharField(max_length=35,blank=True, null=True)
    random_value = models.CharField(max_length=65,blank=True, null=True)

    move_out_date = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    move_in_date = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    made_ready_date = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    days_vacant=models.IntegerField(default=0)

    priror_rent=models.IntegerField(default=0)
    net_renovated_rent=models.IntegerField(default=0)
    monthly_net_increase=models.IntegerField(default=0)
    annualized_increase=models.IntegerField(default=0)

    country=models.CharField(max_length=50,default="United States")
    city=models.CharField(max_length=50,default="California")
    state=models.CharField(max_length=50, null=True,blank=True)
    neighborhood=models.CharField(max_length=50, null=True,blank=True)
    zip=models.CharField(max_length=10, null=True,blank=True)
    added_through=models.CharField(max_length=10, default="manual")

    # paint_contractor=models.IntegerField(default=0)
    # resurface=models.IntegerField(default=0)
    # cabinets=models.IntegerField(default=0)
    # cabinets_hardware=models.IntegerField(default=0)

    # quartz_counter_top=models.IntegerField(default=0)
    # appliance_package=models.IntegerField(default=0)
    # carpet=models.IntegerField(default=0)
    # flooring=models.IntegerField(default=0)

    # tub_tile=models.IntegerField(default=0)
    # hardware=models.IntegerField(default=0)
    # lighting=models.IntegerField(default=0)

    # blinds=models.IntegerField(default=0)

    # misc=models.IntegerField(default=0)
    total_renovation_costs=models.IntegerField(default=0)
    annualized_return=models.IntegerField(default=0)
    
    # date_completed=models.IntegerField(default=0)
    comments = models.TextField(blank=True, null=True)

    owned_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name='unit_owned_by')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name='unit_added_by')
    added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    

    objects=UnitManager()

    def __str__(self):
        return f"{self.unit_number},"
    def save(self,*args,**kwargs):
        # if not self.request.id:
        #     self.request.id="SWO"

        if self.move_out_date and self.move_in_date:
            diff=(self.move_in_date - self.move_out_date).days     
            self.days_vacant=diff


        return super().save(*args,**kwargs)
    class Meta:
         verbose_name_plural = "Units"
         ordering = ['unit_number']
    # def get_absolute_url(self):
    #     return reverse("property:unit-detail", args=[self.id])





# class Property_category(models.Model):



