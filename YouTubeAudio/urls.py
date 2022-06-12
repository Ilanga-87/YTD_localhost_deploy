"""YouTubeAudio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from audio.views import ConvertView, SuccessView, LoadView, NewView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', get_link, name='get_link'),
    path('', ConvertView.as_view(), name='index'),
    path('success-page-<str:slug>', SuccessView.as_view(), name='success-page'),
    path('new-page', NewView.as_view()),
    path('load-audio-<str:slug>', LoadView.as_view(), name='load-page')

]
