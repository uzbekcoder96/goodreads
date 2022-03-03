
from django import forms
from django.shortcuts import redirect
from django.core.mail import send_mail
from .models import CustomUser



class UserCreationForm(forms.ModelForm):
    # username = forms.CharField(max_length=150)
    # email = forms.EmailField()
    # first_name = forms.CharField(max_length=150)
    # last_name = forms.CharField(max_length=150)
    # password = forms.CharField(max_length=128)    
    confirm_password =  forms.CharField(max_length=128)
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')
        
    
    def save(self, commit=True):
        user = super().save(commit)    
        user.set_password(self.cleaned_data['password'])
        user.save()
        
        # send_mail(
        #     "Welcome to goodreads clone",
        #     f"Hi, {user.username}. Wlcome to Goodreads clone enjoy and relax with readeing",
        #     'faridtinchlikov@gmail.com',
        #     [user.email],
        #     print('email send')
        # )
        print("sending email")
        return user        
    # def save(self):
    #     username = self.cleaned_data['username']
    #     first_name = self.cleaned_data['first_name']
    #     last_name = self.cleaned_data['last_name']
    #     email = self.cleaned_data['email']
    #     password = self.cleaned_data['password']

    #     user = User.objects.create(
    #         username=username,
    #         first_name=first_name,
    #         last_name=last_name,
    #         email=email
    #     )
    #     user.set_password(password)
    #     user.save()

    #     return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')
 