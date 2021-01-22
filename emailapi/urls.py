from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from emailapi import views

urlpatterns = [
    path('emails/', views.email_functions),
    path('emails/<int:pk>', views.email_details),
]

urlpatterns = format_suffix_patterns(urlpatterns)