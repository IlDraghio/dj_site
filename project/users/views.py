from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

def registration_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        for fieldname in ['username', 'password1', 'password2']:
            form.fields[fieldname].help_text = None
        print(form.errors)
        if form.is_valid():
            login(request,form.save())
            print("utente salvato")
            return redirect("home")
    else:
        print("utente non salvato",request.method)
        form = UserCreationForm()
        for fieldname in ['username', 'password1', 'password2']:
            form.fields[fieldname].help_text = None
    return render(request,'registration/registration.html',{"form" : form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request,'login/login.html',{"form" : form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
