from django.urls import path
from rest_framework import permissions, generics
from rest_framework.views import APIView

from alerts.serializer import AlertVideoSerializer


class AlertVideoView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AlertVideoSerializer


urls = [
    path('alert-video', AlertVideoView.as_view())
]
