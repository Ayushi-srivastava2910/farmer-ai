from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.view_reports, name='reports'), 
    path('generate-report/', views.generate_report, name='generate_report'),
    path('download-report/<int:report_id>/', views.download_report, name='download_report'),
]