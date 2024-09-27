# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import redirect


def user_logout(request):
    logout(request)
    return redirect('')