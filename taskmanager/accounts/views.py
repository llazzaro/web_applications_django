from accounts.forms import CustomAuthenticationForm
from accounts.services import auth as auth_service
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import redirect, render


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("accounts:login")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def token_generation_view(request: HttpRequest):
    token = auth_service.generate_token(request.user)
    jwt_token = auth_service.issue_jwt_token(request.user)
    return render(request, "accounts/token_display.html", {"token": token, "jwt_token": jwt_token})


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
