from django import forms
from django.contrib.auth.forms import (PasswordChangeForm, UserChangeForm,
                                       UserCreationForm)
from django.utils.safestring import mark_safe

from .models import User, UserProfile


# django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
 
class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', )

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Email already used')
		return email



# class SignUpForm(UserCreationForm):                                          																						
# 	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))          
# 	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))                              																						                                                          

# 	class Meta:                                                                                         
# 		model = User                                                                                      
# 		fields = ('username', 'email', 'password', 'password2')  

# 	def clean_email(self):
# 		email = self.cleaned_data['email']
# 		if User.objects.filter(email=email).exists():
# 			raise forms.ValidationError('Email already used')
# 		return email

# 	def __init__(self, *args, **kwargs):                                    
# 		super(SignUpForm, self).__init__(*args, **kwargs)                    
# 		self.fields['username'].widget.attrs['class'] = 'form-control'            
# 		self.fields['password'].widget.attrs['class'] = 'form-control'      
# 		self.fields['password2'].widget.attrs['class'] = 'form-control'   