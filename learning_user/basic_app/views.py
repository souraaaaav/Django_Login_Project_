from django.shortcuts import render
from .forms import user_form,UserProfileInfo_form
from .models import UserProfileInfo
# Create your views here.

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,'basic_app/index.html',{'title':'Home'})

def user_registration(request):
    
    registered = False

    if request.method == 'POST': 
        userForm = user_form(data=request.POST)
        profileForm=UserProfileInfo_form(data=request.POST)

        if userForm.is_valid() and profileForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            profile=profileForm.save(commit=False)
            profile.user=user
            
            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()
            registered=True
        
        else:
            print(user_form.errors,profileForm.errors)

    else:
        userForm=user_form()
        profileForm=UserProfileInfo_form()

    return render(request,'basic_app/registration.html',{'userForm':userForm,'profileForm':profileForm,'registered':registered,'title':'registration'})    



def user_login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("NOT ACTIVE!")

        else:
            print('Failed username- {} & password- {}'.format(username,password)) 
            return HttpResponse("Invalid login details")

    else:
        return render(request,'basic_app/login.html',{'title':'login'})        

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))