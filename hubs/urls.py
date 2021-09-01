from django.urls import path
from . import views

urlpatterns = [
    path('hubs/', views.HubList.as_view()),
    path('hubs/<int:pk>/', views.HubDetail.as_view()),
    path('hubs/<int:id>/modules/<int:module_pk>/', views.HubEnabledModules.as_view()),
    path('modules/', views.ModuleList.as_view()),
    path('modules/settings/', views.ModuleSettingList.as_view()),
    path('modules/settings/<int:pk>', views.ModuleSettingDetail.as_view()),
    path('modules/settings/changed/<int:unix_timestamp>', views.ModuleSettingChanged.as_view())
]
