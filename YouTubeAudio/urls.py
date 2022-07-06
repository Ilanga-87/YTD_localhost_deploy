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
from django.conf.urls.static import static
from django.conf import settings

from audio.views import ConvertView, SuccessView, LoadView, ConfirmationView, download_audio, \
    BlackListView, ConfirmedBL, WaitContext

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ConvertView.as_view(), name='index'),
    path('success-page-<str:slug>', SuccessView.as_view(), name='success-page'),
    path('load-audio-<str:slug>', LoadView.as_view(), name='load-page'),
    path('download-audio-<str:title>', download_audio, name='download-audio'),
    path('do-not-disturb', BlackListView.as_view(), name='add-to-blacklist'),
    path('confirm-blacklist', ConfirmationView.as_view(), name='confirm-blacklist'),
    path('confirmed', ConfirmedBL.as_view(), name='confirmed-bl'),
    path('about-us', WaitContext.as_view(), name='about-us'),
    path('faq', WaitContext.as_view(), name='faq'),
    path('privacy', WaitContext.as_view(), name='privacy'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
