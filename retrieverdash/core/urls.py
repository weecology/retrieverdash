from django.urls import path
from .views import DashboardView, DiffView

app_name = 'core'
urlpatterns = [
    path('diff/<str:filename>/', DiffView.as_view(), name='diff'),
    path('', DashboardView.as_view(), name='dashboard'),

]
