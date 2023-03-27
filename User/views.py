from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
# Create your views here.


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user:login"))
    return render(request, "user/login.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("inventory:index"))
        else:
            return render(request, "user/login.html", {
                "message": "Invalid Credentials"
            })
    return render(request, "user/login.html")


def logout_view(request):
    logout(request)
    return render(request, "user/login.html",{
        "message": "Logged Out."
    })


def signup_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, "Registration successful.")
            return HttpResponseRedirect(reverse("user:login"))
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="user/register.html",
                  context={"register_form":form})

