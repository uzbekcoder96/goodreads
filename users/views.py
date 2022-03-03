from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm, UserUpdateForm


class RegisterView(View):

    def get(self, request):
        create_form = UserCreationForm()
        context = {
            "form": create_form
        }
        return render(request, 'register.html', context)

    def post(self, request):
        create_form = UserCreationForm(data=request.POST)
        password1 = create_form['password'].value()
        password2 = create_form['confirm_password'].value() 
        if create_form.is_valid():
            if password1 != password2:
               
                context = {
                        "form": create_form
                    }
                messages.warning(request, 'Your password does not match')    
                return render(request, 'register.html', context)
                
              
            create_form.save()
            return redirect('users:login')
            
        else:
            context = {
            "form": create_form
            }
            return render(request, 'register.html', context)
            

class LoginView(View):

    def get(self, request):
        login_form = AuthenticationForm()


        return render(request, 'login.html', {'login_form': login_form})


    def post(self, request):

        login_form = AuthenticationForm(data=request.POST)
        
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, f'Welcome <<{user.username}>> to your profile')
            return redirect('books:list')
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ProfileView(LoginRequiredMixin ,View):
    def get(self, request):
        return render(request, 'profile.html', {'user':request.user})            


class LogoutView(View):
    def get(self, request):

        logout(request)
        messages.info(request, 'You have successfully logged out')
        return redirect('landing_page')
         

class ProfileUpodateView(LoginRequiredMixin, View):
    def get(self, request):

        user_update_form = UserUpdateForm(instance=request.user)

        return render(request, 'profile_edit.html', {'update_form': user_update_form})

    def post(self, request):
        user_update_form = UserUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        ) 

        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, 'You have successfully update your profile')


            return redirect('users:profile')
            
        return render(request, 'profile_edit.html', {'update_form': user_update_form})