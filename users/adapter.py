from allauth.account.adapter import DefaultAccountAdapter
# from django.contrib.auth.models import User
from .models import AdminProfile
# from userpreferences.models import UserPreference

class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        """
        # Do not persist the user yet so we pass commit=False
        # (last argument)
        print("request --------------")
        print(request)
        print("request --------------")
        print("form --------------")
        print(form)
        print("form --------------")
        user = super(AccountAdapter, self).save_user(request, user, form, commit=False)       
        user.is_system_admin=False
        user.is_employee=True
        user.is_tenant=False
        user.save()

    
            #client user
        client = AdminProfile()
        client.user = user
        first_name=form.cleaned_data.get('first_name')
        last_name=form.cleaned_data.get('last_name')
        name=f'{first_name} {last_name}' 
        client.name = name
        print("First Name:",first_name)
        print("Last Name:",last_name)
        print("Name:",name)
        client.email = form.cleaned_data.get('email')
        client.save()
 