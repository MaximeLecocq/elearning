from django.urls import path
from . import views
from django.contrib.auth import views
from .views import enroll_course, enrollment_confirmation, enrolled_courses, drop_course, enrollment_already_exists, remove_student,notification_list

from elearning import views

urlpatterns = [
    path('', views.homepage, name = 'homepage'),
    path('about/', views.about, name = 'about'),
    path('lessons/', views.lessons, name = 'lessons'),
    path('contact/', views.contact, name = 'contact'),
    path('courses/', views.courses_list, name='courses_list'),
    path('course/<int:course_id>/enrollment_confirmation/', enrollment_confirmation, name='enrollment_confirmation'),
    path('create/', views.create_course, name='create_course'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('enrolled_courses/', enrolled_courses, name='enrolled_courses'),
    path('course/<int:course_id>/drop/', drop_course, name='drop_course'),
    path('enrollment-already-exists/<int:course_id>/', enrollment_already_exists, name='enrollment_already_exists'),
    path('course/<int:course_id>/students/', views.course_students, name='course_students'),
    path('search/', views.search_results, name='search_results'),
    path('list_students/', views.list_students, name='list_students'),
    path('list_students/', views.list_students, name='list_students'),
    path('course/<int:course_id>/students/', views.course_students, name='course_students'),
    path('course/<int:course_id>/remove_student/<int:student_id>/', views.remove_student, name='remove_student'),
    path('notification_list/', views.notification_list, name='notification_list'),
]