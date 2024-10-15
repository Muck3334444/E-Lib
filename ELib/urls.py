"""
URL configuration for ELib project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from ELib.views import logoutView, signupView, search_books

urlpatterns = [
    # We are only using a single app, so we redirect all urls there
    path('', RedirectView.as_view(url='library/', permanent=True)),
    path('admin/', admin.site.urls),
    path("library/", include("library.urls")),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logoutView, name='logout'),
    path('signup/', signupView, name='signup'),
    path('search_books/', search_books, name='search_books'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)