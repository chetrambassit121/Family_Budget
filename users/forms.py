# from django import forms
# from django.contrib.auth.forms import (PasswordChangeForm, UserChangeForm,
#                                        UserCreationForm)
# from django.utils.safestring import mark_safe
# from .models import User


# class SignUpForm(UserCreationForm):                   
# 	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))        
# 	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))                                                                    
# 	# first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))                                                                    
# 	# last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))  
	
# 	class Meta:                                                                                         
# 		model = User                                                                                      
# 		fields = ('email', 'username', 'password1', 'password2')  

# 	def clean_email(self):
# 		email = self.cleaned_data['email']
# 		if User.objects.filter(email=email).exists():
# 			raise forms.ValidationError('Email already exists')
# 		return email

# 	def __init__(self, *args, **kwargs):                                    
# 		super(SignUpForm, self).__init__(*args, **kwargs)               
# 		self.fields['email'].widget.attrs['class'] = 'form-control'            
# 		self.fields['username'].widget.attrs['class'] = 'form-control'
# 		# self.fields['first_name'].widget.attrs['class'] = 'form-control'            
# 		# self.fields['last_name'].widget.attrs['class'] = 'form-control'            
# 		self.fields['password1'].widget.attrs['class'] = 'form-control'      
# 		self.fields['password2'].widget.attrs['class'] = 'form-control'   
















# from django import forms
# from django.contrib.auth.forms import (PasswordChangeForm, UserChangeForm,
#                                        UserCreationForm)
# from django.utils.safestring import mark_safe

# from .models import User, UserProfile


# # django.contrib.auth.models import User
# # from django.contrib.auth.forms import UserCreationForm
 
# class SignUpForm(UserCreationForm):
# 	class Meta:
# 		model = User
# 		fields = ('username', 'email', 'password1', 'password2', )

# 	def clean_email(self):
# 		email = self.cleaned_data['email']
# 		if User.objects.filter(email=email).exists():
# 			raise forms.ValidationError('Email already used')
# 		return email



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