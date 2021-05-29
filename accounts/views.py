from django.forms.widgets import NullBooleanSelect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from accounts import forms 
from accounts import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate, 
    login as userlogin,
    logout as userlogout
)


# Create your views here.
def signup(request):
    signupForm = forms.SignUpForm() 
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        if password != confirmPassword:
            return HttpResponse('Password didnt matched')
        else:
            try:
                user = User.objects.create_user(
                    username = username,
                    password = password
                )
                
                user.save()
                userlogin(request,user)
                # Save User Type Also 
                if request.POST.get('button1') is not None:
                    user_type = models.UserProfile(user = user,isVolunteer=True)
                    user_type.save()
                elif request.POST.get('button2') is not None:
                    user_type = models.UserProfile(user = user,isUser=True)
                    user_type.save()
                else :
                    return HttpResponse("Something Went Wrong")
                
                # User Created Successfully 
                return redirect('updateprofile',pk = user_type.pk)
            except:
                return HttpResponse("Something Went Wrong")
    
    context = {
        "signupForm" : signupForm
    }

    return render(request,'accounts/signup.html',context)


def login(request):
    loginForm = forms.LoginForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
                request,
                username = username,
                password = password 
            )
        if user is not None:
            userlogin(request,user)
            usertype = models.UserProfile.objects.get(user=user)
            if user.is_authenticated and usertype.isVolunteer:
                #redirect to volunteer dashboard
                return redirect('vhome')
            elif user.is_authenticated and usertype.isUser:
                #redirect to user dashboard
                return redirect('uhome')
        else:
            return redirect('login')
    
    context = {
        "loginForm": loginForm
    }
    return render(request,'accounts/login.html',context)

def logout(request):
    userlogout(request)
    return redirect('login')

@login_required
def updateprofile(request,pk):
    user = models.UserProfile.objects.get(pk=pk)
    initial = {
        "name" : user.name,
        "contact" : user.contact,
        "address": user.address,
        "city" : user.city,
        "state" : user.state,
        "pincode" : user.pincode
    }
    profileForm = forms.ProfileForm(initial=initial)
    if request.method =="POST":
        user.name = request.POST.get('name')
        user.contact = request.POST.get('contact')
        user.address = request.POST.get('address')
        user.city = request.POST.get('city')
        user.state = request.POST.get('state')
        user.pincode = request.POST.get('pincode')
        user.save()
        # return to dashboard
        if user.isVolunteer:
            # redirect to volunteer dashboard
            return redirect('vhome')
        else:
            # redirect to user dashboard
            return redirect('uhome')
    context = {
        "profileForm" : profileForm ,
        "name" : user.name
    }
    return render(request,'accounts/updateprofile.html',context)



def home(request):
    return render(request,'accounts/home.html')