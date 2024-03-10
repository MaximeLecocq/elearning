from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Enrollment, Feedback,Notification
from .forms import CourseForm, FeedbackForm
from users.models import User
from .utils import create_course_enrollment_notification
from rest_framework import viewsets
from .serializers import CourseSerializer,FeedbackSerializer, EnrollmentSerializer

######################################################################################
#################################### static pages ####################################
######################################################################################
def homepage(request):
    return render(request, 'staticpages/homepage.html')

def about(request):
    return render(request, 'staticpages/about.html')

def lessons(request):
    return render(request, 'staticpages/lessons.html')

def contact(request):
    return render(request, 'staticpages/contact.html')


######################################################################################
#################### Check if the user is a teacher or a student #####################
######################################################################################
def is_teacher(user):
    return user.is_teacher

def is_student(user):
    return user.is_student



######################################################################################
##################### Functions for creating and viewing courses #####################
######################################################################################

# View function for creating a course
@login_required
@user_passes_test(is_teacher)
def create_course(request):
    if request.method == 'POST':
        createform = CourseForm(request.POST, request.FILES)
        if createform.is_valid():
            course = createform.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('courses_list')
    else:
        createform = CourseForm()
    return render(request, 'elearning/create_course.html', {'createform': createform})


# View function to display a list of courses
@login_required
def courses_list(request):
    if request.user.is_teacher:
        courses = Course.objects.filter(instructor=request.user)
    else:
        enrolled_course_ids = Enrollment.objects.filter(student=request.user).values_list('course__id', flat=True)
        available_courses = Course.objects.exclude(id__in=enrolled_course_ids)
        enrolled_courses = Course.objects.filter(id__in=enrolled_course_ids)
        courses = enrolled_courses | available_courses
    return render(request, 'elearning/courses_list.html', {'courses': courses})


# View function for displaying course details
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    feedback_form = FeedbackForm()
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.student = request.user
            feedback.course = course
            feedback.save()
            return redirect('course_detail', course_id=course_id)

    feedbacks = Feedback.objects.filter(course=course)
    return render(request, 'elearning/course_detail.html', {'course': course, 'enrolled': enrolled, 'feedbacks': feedbacks, 'feedback_form': feedback_form})



######################################################################################
############################## Function for notification #############################
######################################################################################

# Function for displaying notifications
@login_required
@user_passes_test(is_teacher)
def notification_list(request):
    notifications = Notification.objects.all()
    context = {'notifications': notifications}
    return render(request, 'elearning/notification_list.html', context)



######################################################################################
############################## Functions for enrollment ##############################
######################################################################################

# Function for enrolling in a course
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user
    # Check if the student is already enrolled in the course
    if Enrollment.objects.filter(student=student, course=course).exists():
        # Redirect to a page indicating that the student is already enrolled
        return redirect('enrollment_already_exists', course_id=course_id)
    else:
        # If not already enrolled, create a new enrollment
        Enrollment.objects.create(student=student, course=course)
        create_course_enrollment_notification(course, student)
        return redirect('enrollment_confirmation', course_id=course_id)


# Function for displaying a page indicating that the student is already enrolled
@login_required
def enrollment_already_exists(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'elearning/enrollment_already_exists.html', {'course': course})


# responsible for rendering the confirmation page after the student successfully enrolls in a course
@login_required
def enrollment_confirmation(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'elearning/enrollment_confirmation.html', {'course': course})


# Function for displaying enrolled courses
@login_required
def enrolled_courses(request):
    enrolled_courses = Course.objects.filter(enrollment__student=request.user)
    return render(request, 'elearning/enrolled_courses.html', {'enrolled_courses': enrolled_courses})


# Function for dropping a course
@login_required
@user_passes_test(is_student)
def drop_course(request, course_id):
    enrollment = get_object_or_404(Enrollment, student=request.user, course_id=course_id)
    enrollment.delete()
    return redirect('courses_list')




######################################################################################
#################### Functions for searching and viewing students ####################
######################################################################################

@user_passes_test(is_teacher)
def course_students(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrolled_students = Enrollment.objects.filter(course=course).select_related('student')
    return render(request, 'elearning/course_students.html', {'course': course, 'enrolled_students': enrolled_students})

# Function for searching students and other teachers
@user_passes_test(is_teacher)
def search_results(request):
    query = request.GET.get('query')
    if query:
        # Search for students by username
        students = User.objects.filter(username__icontains=query, is_student=True)
        # Search for teachers by username
        teachers = User.objects.filter(username__icontains=query, is_teacher=True)
    else:
        students = []
        teachers = []
    return render(request, 'elearning/search_results.html', {'students': students, 'teachers': teachers})


@login_required
@user_passes_test(is_teacher)
def list_students(request):
    students = User.objects.filter(is_student=True)
    student_data = []
    for student in students:
        courses_enrolled = Enrollment.objects.filter(student=student)
        enrolled_courses = ", ".join([enrollment.course.title for enrollment in courses_enrolled])
        student_data.append({
            'username': student.username,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'enrolled_courses': enrolled_courses
        })
    return render(request, 'elearning/list_students.html', {'students': student_data})



@login_required
def remove_student(request, course_id, student_id):
    enrollment = get_object_or_404(Enrollment, course_id=course_id, student_id=student_id)
    if request.method == 'POST':
        enrollment.delete()
        return redirect('course_students', course_id=course_id)
    return render(request, 'elearning/course_students.html')



######################################################################################
########################## Class based view for serializers ##########################
######################################################################################

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
