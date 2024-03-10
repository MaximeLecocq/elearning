from django.shortcuts import render,redirect, get_object_or_404
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Post
from users.models import User


def is_teacher(user):
    return user.is_teacher

@login_required
@user_passes_test(is_teacher)
def dashboard_teacher(request):
    current_user = request.user
    status_teacher = Post.objects.filter(user=current_user)
    if request.method=='POST':
        teacher_form = PostCreateForm(data=request.POST, files=request.FILES)
        if teacher_form.is_valid():
            new_item = teacher_form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return redirect('dashboard_teacher')
    else:
        teacher_form = PostCreateForm(data=request.GET)
    return render(request, 'elearning/dashboard_teacher.html',{'status_teacher':status_teacher,'teacher_form':teacher_form})


def is_student(user):
    return user.is_student

@login_required
@user_passes_test(is_student)
def dashboard_student(request):
    current_user = request.user
    status = Post.objects.filter(user=current_user)
    if not request.user.is_student:
        return redirect('dashboard_teacher')
    if request.method == 'POST':
        student_form = PostCreateForm(request.POST)
        if student_form.is_valid():
            status_update = student_form.save(commit=False)
            status_update.user = request.user
            status_update.save()
            return redirect('dashboard_student')
    else:
        student_form = PostCreateForm(data=request.GET)
    return render(request, 'elearning/dashboard_student.html', {'status': status,'student_form': student_form})


def delete_status(request, status_id):
    # Retrieve the status object using the status_id
    status = get_object_or_404(Post, pk=status_id)

    # Check if the current user is the author of the status
    if request.user == status.user:
        # If the user is the author, delete the status
        status.delete()
    
    # Redirect the user back to the dashboard
    return redirect('dashboard_student')


def delete_status_teacher(request, status_teacher_id):
    # Retrieve the status object using the status_id
    status_teacher = get_object_or_404(Post, pk=status_teacher_id)

    # Check if the current user is the author of the status
    if request.user == status_teacher.user:
        # If the user is the author, delete the status
        status_teacher.delete()
    
    # Redirect the user back to the dashboard
    return redirect('dashboard_teacher')