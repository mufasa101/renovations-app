from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,AdminProfile


@receiver(post_save, sender=User)
def admin_profile(sender,instance,created, **kwargs):
    print('sender',sender)
    print('created',created)
    print('Admin profile----------')

    if created:
        AdminProfile.objects.create(user=instance)
        if instance.is_superuser:
            instance.is_system_admin=True
            instance.is_employee=False
            instance.save()
        elif instance.is_employee:
            instance.is_system_admin=False
            instance.is_employee=True
            instance.save()
       
    else:

        print("data was not updated")
