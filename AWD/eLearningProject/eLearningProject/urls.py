from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from rest_framework import routers
from elearning.views import CourseViewSet,FeedbackViewSet,EnrollmentViewSet
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register('courses',CourseViewSet)
router.register('feedbacks',FeedbackViewSet)
router.register('enrollment',EnrollmentViewSet)
router.register('users',UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('elearning.urls')),
    path('users/', include('users.urls')),
    path('rooms/',include('chatapp.urls')),
    path('post/',include('post.urls')),
    path('api/',include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

