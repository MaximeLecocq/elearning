from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .views import confirm_delete_profile, delete_profile,profile_deleted
urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('register/',views.register,name='register'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('profile/delete/confirm/', confirm_delete_profile, name='confirm_delete_profile'),
    path('profile/delete/', delete_profile, name='delete_profile'),
    path('profile/deleted/', profile_deleted, name='profile_deleted'),
]