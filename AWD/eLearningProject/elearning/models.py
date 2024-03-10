from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Course(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses_taught')
    pdf_material = models.FileField(upload_to='course_materials/pdf', blank=True, null=True)
    video_material = models.FileField(upload_to='course_materials/videos', blank=True, null=True)
    image_material = models.ImageField(upload_to='course_materials/images', blank=True, null=True)


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('student', 'course')


class Feedback(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    rating = models.IntegerField()
    

class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_notifications', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_notifications', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

