from .models import Notification

def create_course_enrollment_notification(course, student):
    Notification.objects.create(
        sender=student,
        recipient=course.instructor,
        course=course,
        message=f"Student {student.username} has enrolled in your course '{course.title}'.",

    )