from django.shortcuts import render,redirect
from .form import LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@csrf_exempt
def LoginView(request):
    context = {
    "form":LoginForm()
    }
    if request.method == "POST":
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            username = str(list(data.values())[0])
            print(username)
            password = str(list(data.values())[1])
            print(password)
            user = authenticate(request, username= username,password=password)
            print(user)
            if user:
                login(request, user)
                # Redirect to a success page.
                print("sucessful!!")
                return render(request,"login1.html",context)
            else:
                messages.error(request, 'Incorrect password and email')
                #form.AddModelError("", "Invalid login attempt.")
                #a = str("Invalid")
                #context[a]= a

    return render(request,"login.html",context)


def Logout(request):

    context = {}
    logout(request)

    return render(request,"index.html", context)

def Change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/login1/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {'form': form})
