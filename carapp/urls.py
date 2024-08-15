from django.urls import path
from . import views

app_name = 'carapp'

urlpatterns = [
    path('', views.homepage, name='homepage'),  # New homepage view
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
