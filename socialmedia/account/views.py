from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
# Create your views here.


class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "account/register.html", {"form":form})

    def post(self, request):
        pass
