from unicodedata import category
from django.db import models
from django.conf import settings
from property.models import Unit
import datetime


User=settings.AUTH_USER_MODEL



class Request(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE,null=True,blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name='assigned_to')
    request_id = models.CharField(max_length=35,null=True,blank=True)

    request_type = models.CharField(max_length=35,default="non resident")
    priority = models.CharField(max_length=35,default="normal")
    name = models.CharField(max_length=35,null=True,blank=True)
    category = models.CharField(max_length=35)
    description=models.TextField(null=True,blank=True)
    reported_on = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    begun_on = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    solved_on = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)

    budget_start = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    budget_end = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    budget_amount=models.IntegerField(default=0)

    status=models.CharField(max_length=35,default="not started")
    urgency=models.CharField(max_length=20,default="not urgent")

    authorized_enter=models.CharField(max_length=20,default="anytime")
    authorized_enter_start = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    authorized_enter_end = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    special_instructions=models.TextField(null=True,blank=True)
    
    authorized_alarm=models.CharField(max_length=20,default="No")
    authorized_pet=models.CharField(max_length=20,default="No")
    urgency=models.CharField(max_length=20,default="not urgent")
    
    opened=models.BooleanField(default=False)
    added_by_category = models.CharField(max_length=35,default="admin")
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='request_added_by')
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    @property
    def since(self):
        date_diff=( datetime.date.today() - self.reported_on).days     
        return date_diff
    @property
    def budget_days(self):
        date_diff="-----"
        if self.budget_start and self.budget_end:
            diff=(self.budget_end - self.budget_start).days     
            date_diff=f'{diff} days'
        return date_diff
    def save(self,*args,**kwargs):
        # if not self.request.id:
        #     self.request.id="SWO"

        if self.category != "custom":
            self.name=self.category
        return super().save(*args,**kwargs)


 
class Service(models.Model):
    maintenance = models.ForeignKey(Request, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name='service_assigned_to')
    scheduled_date=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    date_in=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    time_in=models.CharField(default="8:00 AM", null=True,blank=True,max_length=10)
    time_out=models.CharField(default="12:15 PM", null=True,blank=True,max_length=10)
    status=models.CharField(max_length=35,default="not started")
    arrived=models.CharField(max_length=35,default="no")
    
    random_maintenance_id=models.CharField(max_length=50, null=True,blank=True)
    action_notes=models.TextField(null=True,blank=True)

    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='service_added_by')
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return f"{self.date_in}, {self.status}"
    @property
    def late_by(self):
        if self.date_in and self.scheduled_date:
            diff=(self.date_in - self.scheduled_date).days     
            date_diff=f'{diff} days'
        return date_diff
class Cost(models.Model):
    maintenance = models.ForeignKey(Request, on_delete=models.CASCADE)
    cost_type=models.CharField(max_length=35,default="materials")
    cost_name=models.CharField(null=True,blank=True,max_length=35)
    random_maintenance_id=models.CharField(max_length=50, null=True,blank=True)

    cost_number=models.IntegerField(default=1)
    cost_description=models.TextField(null=True,blank=True)
    cost_total=models.IntegerField()
    paid=models.CharField(max_length=10,default="not paid")
    paid_date=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    paid_by=models.CharField(max_length=10,default="us")
    ref_no=models.CharField(max_length=45,null=True,blank=True)
    paid_through=models.CharField(max_length=25,default="cash")
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='cost_added_by')
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return f"{self.cost_type}, {self.cost_name} {self.cost_total}"
class Document(models.Model):
    maintenance = models.ForeignKey(Request, on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='requests',null=True,blank=True)
    video=models.URLField( max_length=200,null=True,blank=True )
    random_maintenance_id=models.CharField(max_length=50, null=True,blank=True)
    name=models.CharField(null=True,blank=True,max_length=35)
    category=models.CharField(null=True,blank=True,max_length=35)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='document_added_by')
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return f"{self.name} {self.name}"



