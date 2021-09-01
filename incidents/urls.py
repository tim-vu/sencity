from django.urls import path
from . import views

urlpatterns = [
    path('', views.IncidentList.as_view()),

]
