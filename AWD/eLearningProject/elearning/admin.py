from django.contrib import admin
from .models import Course,Enrollment,Feedback

admin.site.site_header = "Animation School"
admin.site.site_title = "Animation School"
admin.site.index_title = "Manage Animation Courses"

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rating')
    search_fields =('rating',)
admin.site.register(Feedback, FeedbackAdmin)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date')
    search_fields =('student',)
admin.site.register(Enrollment, EnrollmentAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'image_material')
    search_fields =('title',)
admin.site.register(Course, CourseAdmin)