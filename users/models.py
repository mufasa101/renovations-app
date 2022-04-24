from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
# from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    is_system_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=True)
    # notifications = ArrayField(models.CharField(max_length=500), blank=True,null=True)
    objects = UserManager()




class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True,related_name="profile_user")
    name = models.CharField(max_length=50, blank=True,null=True)
    phone_number = models.BigIntegerField(blank=True,null=True)
    position = models.CharField(max_length=50, blank=True,null=True)
#   default="Eastate agent"
    experience = models.IntegerField(default=1)         
    description = models.CharField(max_length=750,blank=True, null=True)
    country=models.CharField(max_length=50,default="Kenya")
    country_code=models.CharField(max_length=50,blank=True, null=True)
    city=models.CharField(max_length=50,default="Nairobi")
    state=models.CharField(max_length=50, null=True,blank=True)
    
    location = models.CharField(max_length=150, blank=True,null=True)
    facebook = models.URLField(max_length = 200, blank=True,null=True)
    twitter = models.URLField(max_length = 200, blank=True,null=True)
    linkedin = models.URLField(max_length = 200, blank=True,null=True)
    youtube = models.URLField(max_length = 200, blank=True,null=True)
    name = models.CharField(max_length=50, blank=True,null=True)
    image=models.ImageField(upload_to='profile',default="profile/no_profile.jpg")
    added_on = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='admin_added_by',null=True)


    @property
    def get_full_name(self):
        return self.name
    @property
    def get_first_name(self):
        return self.name.split()[0]
    @property
    def get_last_name(self):
        if self.name.split()[1]:
            return self.name.split()[1]
        return self.name.split()[0]