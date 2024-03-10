from rest_framework import serializers
from .models import Course,Enrollment,Feedback

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','title','description','instructor']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id','student','course','rating']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id','student','course','enrollment_date']


        