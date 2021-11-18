from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *





# ROOM CREATION FORM
class RoomForm(ModelForm):  
    class Meta:  
        model = Room  
        exclude = ['host', 'participants']

# USER REGISTRATION FORM

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	full_name = forms.CharField(max_length=100)
	class Meta:
		model = User
		fields = ("username", "email", "full_name",  "password1", "password2")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'placeholder':('e.g yousuf_rasheed')})
		self.fields['full_name'].widget.attrs.update({'placeholder':('e.g Yousuf Rasheed')})
		self.fields['email'].widget.attrs.update({'placeholder':('Email')})
		self.fields['password1'].widget.attrs.update({'placeholder':('Password')})        
		self.fields['password2'].widget.attrs.update({'placeholder':('Confirm password')})
		
		for fieldname in ['username', 'password1', 'password2', 'email', 'full_name']:
			self.fields[fieldname].help_text = None
			self.fields[fieldname].widget.attrs.update({'style':('margin-bottom: 1rem;')})

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user