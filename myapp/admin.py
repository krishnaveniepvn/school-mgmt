from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'user', 'current_class', 'parent_name', 'parent_phone']
    list_filter = ['current_class', 'gender', 'is_active']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'parent_name']
    list_per_page = 20

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'qualification', 'specialization', 'is_active']
    list_filter = ['qualification', 'gender', 'is_active']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name']
    list_per_page = 20

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'academic_year', 'room_number', 'capacity']
    list_filter = ['academic_year']
    search_fields = ['name', 'section']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits']
    search_fields = ['name', 'code']

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ['class_obj', 'subject']
    list_filter = ['class_obj__academic_year']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'subject', 'status']
    list_filter = ['date', 'status', 'subject']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    list_per_page = 20

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'class_obj', 'subject', 'start_date', 'end_date']
    list_filter = ['exam_type', 'class_obj__academic_year']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'marks_obtained', 'entered_at']
    list_filter = ['exam__exam_type', 'exam__class_obj__academic_year']
    list_per_page = 20