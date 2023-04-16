from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.main),
    path('homepage/', views.homepage_view),
    path('webcam_feed/', views.webcam_feed, name='webcam_feed'),
    path('mobilecam_feed/', views.mobilecam_feed, name='mobilecam_feed')
]