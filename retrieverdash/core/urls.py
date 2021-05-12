from django.urls import path
from .views import DashboardView, DiffView, DataSetView

app_name = 'core'
urlpatterns = [
    path('dataset/<str:dataset_name>/', DataSetView.as_view(), name='dataset'),
    path('diff/<str:filename>/', DiffView.as_view(), name='diff'),
    path('', DashboardView.as_view(), name='dashboard'),
]
