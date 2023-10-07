from django.urls import path

from .views import (
    ConvertView,
    SuccessView,
    LoadView,
    download_audio,
    SilentListView,
    ConfirmationView,
    ConfirmedSilentListView,
)

urlpatterns = [
    path('', ConvertView.as_view(), name='index'),
    path('success-page-<str:slug>', SuccessView.as_view(), name='success-page'),
    path('load-audio-<str:slug>', LoadView.as_view(), name='load-page'),
    path('download-audio-<str:title>', download_audio, name='download-audio'),
    path('do-not-disturb', SilentListView.as_view(), name='add-to-silent-list'),
    path('confirm-silent-list/<int:pk>', ConfirmationView.as_view(), name='confirm-silent-list'),
    path('confirmed/<int:pk>', ConfirmedSilentListView.as_view(), name='confirmed-silent-list'),
]
