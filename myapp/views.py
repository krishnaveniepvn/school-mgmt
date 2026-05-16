from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *
from .forms import *

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = Class.objects.count()
    total_subjects = Subject.objects.count()
    
    recent_attendances = Attendance.objects.all().order_by('-date')[:5]
    recent_grades = Grade.objects.all().order_by('-entered_at')[:5]
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
        'recent_attendances': recent_attendances,
        'recent_grades': recent_grades,
    }
    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'accounts/profile.html', {'form': form})

# Student Views
@login_required
def student_list(request):
    students = Student.objects.all()
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'students/list.html', {'page_obj': page_obj})

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/detail.html', {'student': student})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student created successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    
    return render(request, 'students/form.html', {'form': form})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/form.html', {'form': form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.user.delete()  # This will also delete the student due to CASCADE
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    
    return render(request, 'students/delete.html', {'student': student})

# Teacher Views
@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/list.html', {'teachers': teachers})

@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teachers/detail.html', {'teacher': teacher})

@login_required
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher created successfully!')
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    
    return render(request, 'teachers/form.html', {'form': form})

@login_required
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher updated successfully!')
            return redirect('teacher_detail', pk=teacher.pk)
    else:
        form = TeacherForm(instance=teacher)
    
    return render(request, 'teachers/form.html', {'form': form})

@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.user.delete()
        messages.success(request, 'Teacher deleted successfully!')
        return redirect('teacher_list')
    
    return render(request, 'teachers/delete.html', {'teacher': teacher})

# Class Views
@login_required
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'classes/list.html', {'classes': classes})

@login_required
def class_detail(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    students = Student.objects.filter(current_class=class_obj)
    subjects = ClassSubject.objects.filter(class_obj=class_obj)
    return render(request, 'classes/detail.html', {
        'class_obj': class_obj,
        'students': students,
        'subjects': subjects
    })

@login_required
def class_create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class created successfully!')
            return redirect('class_list')
    else:
        form = ClassForm()
    
    return render(request, 'classes/form.html', {'form': form})

@login_required
def class_update(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class updated successfully!')
            return redirect('class_detail', pk=class_obj.pk)
    else:
        form = ClassForm(instance=class_obj)
    
    return render(request, 'classes/form.html', {'form': form})

# Subject Views
@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'classes/subject_list.html', {'subjects': subjects})

@login_required
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully!')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    
    return render(request, 'classes/subject_form.html', {'form': form})

# Attendance Views
@login_required
def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-date')
    return render(request, 'attendance/list.html', {'attendances': attendances})

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.marked_by = request.user
            attendance.save()
            messages.success(request, 'Attendance marked successfully!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    
    return render(request, 'attendance/mark.html', {'form': form})

@login_required
def bulk_attendance(request):
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            class_obj = form.cleaned_data['class_obj']
            subject = form.cleaned_data['subject']
            date = form.cleaned_data['date']
            
            students = Student.objects.filter(current_class=class_obj)
            
            for student in students:
                status = request.POST.get(f'status_{student.id}', 'absent')
                remarks = request.POST.get(f'remarks_{student.id}', '')
                
                Attendance.objects.update_or_create(
                    student=student,
                    class_obj=class_obj,
                    subject=subject,
                    date=date,
                    defaults={
                        'status': status,
                        'remarks': remarks,
                        'marked_by': request.user
                    }
                )
            
            messages.success(request, 'Bulk attendance marked successfully!')
            return redirect('attendance_list')
    else:
        form = BulkAttendanceForm()
    
    return render(request, 'attendance/bulk.html', {'form': form})

# Exam Views
@login_required
def exam_list(request):
    exams = Exam.objects.all().order_by('-start_date')
    return render(request, 'grades/exam_list.html', {'exams': exams})

@login_required
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam created successfully!')
            return redirect('exam_list')
    else:
        form = ExamForm()
    
    return render(request, 'grades/exam_form.html', {'form': form})

# Grade Views
@login_required
def grade_list(request):
    grades = Grade.objects.all().order_by('-exam__start_date')
    return render(request, 'grades/grade_list.html', {'grades': grades})

@login_required
def grade_entry(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade entered successfully!')
            return redirect('grade_list')
    else:
        form = GradeForm()
    
    return render(request, 'grades/grade_form.html', {'form': form})

@login_required
def bulk_grade_entry(request):
    if request.method == 'POST':
        form = BulkGradeForm(request.POST)
        if form.is_valid():
            exam = form.cleaned_data['exam']
            students = Student.objects.filter(current_class=exam.class_obj)
            
            for student in students:
                marks = request.POST.get(f'marks_{student.id}')
                if marks:
                    Grade.objects.update_or_create(
                        student=student,
                        exam=exam,
                        defaults={
                            'marks_obtained': marks,
                        }
                    )
            
            messages.success(request, 'Bulk grades entered successfully!')
            return redirect('grade_list')
    else:
        form = BulkGradeForm()
    
    return render(request, 'grades/bulk_grade_form.html', {'form': form})

@login_required
def student_report_card(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    grades = Grade.objects.filter(student=student).select_related('exam')
    
    return render(request, 'grades/report_card.html', {
        'student': student,
        'grades': grades
    })