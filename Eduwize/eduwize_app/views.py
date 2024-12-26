from django.shortcuts import render
from django.db.models.signals import post_save 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Student, Course, Enrollment, StudyMaterial, Quiz, Question, PerformanceAnalysis, Notification, Feedback, AIChatbot, AIRecommendation, Tags, ActivityLog , StudentFile
import uuid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StudentFileForm , StudentForm 


@receiver(post_save, sender=User)
def create_or_update_student_profile(sender, instance, created, **kwargs):
    if created:
        # Generate a unique student ID (e.g., UUID or any custom logic)
        student_id = str(uuid.uuid4())[:9]  # Truncated UUID
        Student.objects.create(user=instance, student_id=student_id)
    else:
        # Update the existing Student profile if the User instance is updated
        try:
            instance.student.save()
        except Student.DoesNotExist:
            # Optionally handle cases where the Student instance doesn't exist
            Student.objects.create(user=instance, student_id=str(uuid.uuid4())[:9])

@login_required
def profile(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        student = None  # Handle the case where there's no Student profile

    return render(request, 'eduwize_app/profile.html', {'student': student})



# Student Views
class StudentListView(ListView):
    model = Student
    template_name = 'eduwize_app/student_list.html'
    context_object_name = 'students'

class StudentDetailView(DetailView):
    model = Student
    template_name = 'eduwize_app/student_detail.html'
    context_object_name = 'student'

class StudentCreateView(CreateView):
    model = Student
    template_name = 'eduwize_app/student_form.html'
    fields = ['name', 'level', 'student_id', 'profile_picture', 'bio']
    success_url = reverse_lazy('eduwize_app:student-list')

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'eduwize_app/student_form.html'
    fields = ['name', 'level', 'student_id', 'profile_picture', 'bio']
    success_url = reverse_lazy('eduwize_app:student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'eduwize_app/student_confirm_delete.html'
    success_url = reverse_lazy('eduwize_app:student-list')


# Course Views
class CourseListView(ListView):
    model = Course
    template_name = 'eduwize_app/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'eduwize_app/course_detail.html'
    context_object_name = 'course'

class CourseCreateView(CreateView):
    model = Course
    template_name = 'eduwize_app/course_form.html'
    fields = ['name', 'description', 'level', 'thumbnail', 'duration']
    success_url = reverse_lazy('eduwize_app:course-list')

class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'eduwize_app/course_form.html'
    fields = ['name', 'description', 'level', 'thumbnail', 'duration']
    success_url = reverse_lazy('eduwize_app:course-list')

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'eduwize_app/course_confirm_delete.html'
    success_url = reverse_lazy('eduwize_app:course-list')


# Enrollment Views
class EnrollmentListView(ListView):
    model = Enrollment
    template_name = 'eduwize_app/enrollment_list.html'
    context_object_name = 'enrollments'

class EnrollmentDetailView(DetailView):
    model = Enrollment
    template_name = 'eduwize_app/enrollment_detail.html'
    context_object_name = 'enrollment'

class EnrollmentCreateView(CreateView):
    model = Enrollment
    template_name = 'eduwize_app/enrollment_form.html'
    fields = ['student', 'course']
    success_url = reverse_lazy('eduwize_app:enrollment-list')

class EnrollmentUpdateView(UpdateView):
    model = Enrollment
    template_name = 'eduwize_app/enrollment_form.html'
    fields = ['student', 'course']
    success_url = reverse_lazy('eduwize_app:enrollment-list')

class EnrollmentDeleteView(DeleteView):
    model = Enrollment
    template_name = 'eduwize_app/enrollment_confirm_delete.html'
    success_url = reverse_lazy('eduwize_app:enrollment-list')


# Study Material Views
class StudyMaterialListView(ListView):
    model = StudyMaterial
    template_name = 'eduwize_app/study_material_list.html'
    context_object_name = 'study_materials'

class StudyMaterialDetailView(DetailView):
    model = StudyMaterial
    template_name = 'eduwize_app/study_material_detail.html'
    context_object_name = 'study_material'

class StudyMaterialCreateView(CreateView):
    model = StudyMaterial
    template_name = 'eduwize_app/study_material_form.html'
    fields = ['title', 'description', 'file', 'course', 'resource_type']
    success_url = reverse_lazy('eduwize_app:study-materials-list')

class StudyMaterialUpdateView(UpdateView):
    model = StudyMaterial
    template_name = 'eduwize_app/study_material_form.html'
    fields = ['title', 'description', 'file', 'course', 'resource_type']
    success_url = reverse_lazy('eduwize_app:study-materials-list')

class StudyMaterialDeleteView(DeleteView):
    model = StudyMaterial
    template_name = 'eduwize_app/study_material_confirm_delete.html'
    success_url = reverse_lazy('eduwize_app:study-materials-list')


# Quiz Views
class QuizListView(ListView):
    model = Quiz
    template_name = 'eduwize_app/quiz_list.html'
    context_object_name = 'quizzes'

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'eduwize_app/quiz_detail.html'
    context_object_name = 'quiz'

class QuizCreateView(CreateView):
    model = Quiz
    template_name = 'eduwize_app/quiz_form.html'
    fields = ['course', 'title', 'description', 'duration', 'score', 'pass_percentage']
    success_url = reverse_lazy('eduwize_app:quiz-list')

class QuizUpdateView(UpdateView):
    model = Quiz
    template_name = 'eduwize_app/quiz_form.html'
    fields = ['course', 'title', 'description', 'duration', 'score', 'pass_percentage']
    success_url = reverse_lazy('eduwize_app:quiz-list')

class QuizDeleteView(DeleteView):
    model = Quiz
    template_name = 'eduwize_app/quiz_confirm_delete.html'
    success_url = reverse_lazy('eduwize_app:quiz-list')


# Question Views
class QuestionListView(ListView):
    model = Question
    template_name = 'eduwize_app/question_list.html'
    context_object_name = 'questions'

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'eduwize_app/question_detail.html'
    context_object_name = 'question'

class QuestionCreateView(CreateView):
    model = Question
    template_name = 'eduwize_app/question_form.html'
    fields = ['quiz', 'question_text', 'options', 'correct_answers', 'correct_answer', 'question_type']
    success_url = reverse_lazy('eduwize_app:question-list')

class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'eduwize_app/question_form.html'
    fields = ['quiz', 'question_text', 'options', 'correct_answers', 'correct_answer', 'question_type']
    success_url = reverse_lazy('eduwize_app:question-list')

class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'eduwize_app/question_confirm_delete.html'
    success_url = reverse_lazy('eduwize_app:question-list')


# Performance Analysis Views
class PerformanceListView(ListView):
    model = PerformanceAnalysis
    template_name = 'eduwize_app/performance_list.html'
    context_object_name = 'performances'

class PerformanceDetailView(DetailView):
    model = PerformanceAnalysis
    template_name = 'eduwize_app/performance_detail.html'
    context_object_name = 'performance'


# Notification Views
class NotificationsListView(ListView):
    model = Notification
    template_name = 'eduwize_app/notifications_list.html'
    context_object_name = 'notifications'


# Feedback Views
class FeedbackFormView(CreateView):
    model = Feedback
    template_name = 'eduwize_app/feedback_form.html'
    fields = ['student', 'feedback', 'rating']
    success_url = reverse_lazy('eduwize_app:home')


# AI Chatbot Views
class AIChatbotView(CreateView):
    model = AIChatbot
    template_name = 'eduwize_app/ai_chatbot_form.html'
    fields = ['question', 'answer']
    success_url = reverse_lazy('eduwize_app:ai-chatbot')


# AI Recommendation Views
class AIRecommendationsView(ListView):
    model = AIRecommendation
    template_name = 'eduwize_app/ai_recommendations_list.html'
    context_object_name = 'ai_recommendations'


# Tags Views
class TagsListView(ListView):
    model = Tags
    template_name = 'eduwize_app/tags_list.html'
    context_object_name = 'tags'


# Activity Log Views
class ActivityLogView(ListView):
    model = ActivityLog
    template_name = 'eduwize_app/activity_log_list.html'
    context_object_name = 'activity_logs'


# Home Page View
class HomePageView(ListView):
    model = Course
    template_name = 'eduwize_app/home.html'
    context_object_name = 'courses'
    paginate_by = 10
    ordering = ['-created_at']
    queryset = Course.objects.all()
    allow_empty = True
    extra_context = {'title': 'Home Page'}
    success_url = reverse_lazy('eduwize_app:home')

class NotificationsListView(ListView):
    model = Notification
    template_name = 'eduwize_app/notifications_list.html'
    context_object_name = 'notifications'


def student_files_upload(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        for file in files:
            StudentFile.objects.create(student=request.user.student, file=file)
            return HttpResponse('Files uploaded successfully')
    else:
        form = StudentFileForm()
    return render(request, 'upload.html', {'form': form})
