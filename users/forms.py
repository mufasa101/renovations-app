from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')

    def signup(self, request, user):
        user = super(CustomSignupForm, self).save(request)
        print("fffffffffffffffforms")
        print(user)
        user.last_name = self.cleaned_data['last_name']
        user.first_name =  self.cleaned_data['first_name']

        user.save()
        return user