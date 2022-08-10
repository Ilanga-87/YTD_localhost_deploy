from django.urls import path

from .views import (
    ConvertView,
    SuccessView,
    LoadView,
    download_audio,
    BlackListView,
    ConfirmationView,
    ConfirmedBlackListView,
)

urlpatterns = [
    path('', ConvertView.as_view(), name='index'),
    path('success-page-<str:slug>', SuccessView.as_view(), name='success-page'),
    path('load-audio-<str:slug>', LoadView.as_view(), name='load-page'),
    path('download-audio-<str:title>', download_audio, name='download-audio'),
    path('do-not-disturb', BlackListView.as_view(), name='add-to-blacklist'),
    path('confirm-blacklist/<int:pk>', ConfirmationView.as_view(), name='confirm-blacklist'),
    path('confirmed/<int:pk>', ConfirmedBlackListView.as_view(), name='confirmed-bl'),
]
