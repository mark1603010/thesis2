
from django.contrib.auth.forms import UserCreationForm
from home.models import User
from django.core.validators import ValidationError
from django import forms
from django.core.mail import send_mail
from util.Util import random_string_generator, send_email_generic
class SignUpForm(UserCreationForm):
   email = forms.EmailField(required=True,label='Email',error_messages={'exists': 'Oops! Email already exist'})
   class Meta:
      model = User 
      fields = ('username', 'email', 'password1', 'password2',)

   def save(self, commit=True):
        user = super().save(commit=False)
        clean_email = self.cleaned_data["email"]
        verification_token = random_string_generator(12)
        user.email = clean_email
        user.email_verification_token = verification_token
        if commit:
            user.save()
            # send email verification
            self.verify_email(clean_email, verification_token)
        return user

   def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']

   def verify_email(self, email, token):
       url = "http://128.199.86.130:8000/verify-email/{}".format(token)
       msg = "<p>Thanks for signing up to MUSEO Tu' Agusan.</p>"
       msg += "<p>Please click the link below for emaiil verification.</p>"
       msg += "<p>&nbsp;</p>"
       msg += '<p><a href="{0}">{0}</a></p>'.format(url)
       msg += "<p>&nbsp;</p>"
       msg += "<p>Thanks</p>"
       send_email_generic(msg, email)