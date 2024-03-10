from django import forms
from .models import Course,Feedback,Feedback

#form for creating a Course
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'pdf_material', 'video_material', 'image_material']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'pdf_material': 'PDF Material',
            'video_material': 'Video Material',
            'image_material': 'Image Material',
        }

# Form for creating a Feedback
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text', 'rating']

        