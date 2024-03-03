"""
URL configuration for taskmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView
from django.urls import include, path, reverse_lazy

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls", namespace="tasks")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            success_url=reverse_lazy("accounts:password_change_done"),
            template_name="accounts/password_change_form.html",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeView.as_view(template_name="accounts/password_change_done.html"),
        name="password_change_done",
    ),
]
