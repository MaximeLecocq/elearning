from django.urls import path
from . import views

urlpatterns = [
    path('dashboard_teacher/', views.dashboard_teacher, name='dashboard_teacher'),
    path('dashboard_student/', views.dashboard_student, name='dashboard_student'),
    path('status/delete/<int:status_id>/', views.delete_status, name='delete_status'),
    path('status_teacher/delete/<int:status_teacher_id>/', views.delete_status_teacher, name='delete_status_teacher'),
]