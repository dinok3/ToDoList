from django.shortcuts import render,redirect
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"You have been successfully registered!")
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST,request.FILES,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,f"You have been successfully updated your profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form =  ProfileUpdateForm(instance=request.user.profile)
    context = {
        "u_form":user_form,
        "p_form":profile_form,

    }
    return render(request, "users/profile.html",context)