from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.dispatch import receiver
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.utils.decorators import method_decorator
from .models import Student, Course, Enrollment, StudyMaterial, Quiz, Question, PerformanceAnalysis, Notification, Feedback, AIChatbot, AIRecommendation, Tags, ActivityLog, StudentFile, ExamPaper, StudyLevelChoices
import uuid
import json
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db import connections
from django.db.utils import OperationalError
from django.views.decorators.cache import never_cache
from django.db.models import Count, Avg, Max, Sum
from .forms import StudentFileForm, StudentForm, ExamPaperForm, ProfileUpdateForm

# Admin check decorator
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Admin required decorator for class-based views
def admin_required(view_func):
    decorated_view = user_passes_test(is_admin, login_url='users:login')(view_func)
    return decorated_view


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
        messages.error(request, "No student profile found. Please contact an administrator.")
        return redirect('eduwize_app:home')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=student, user=request.user)
        if form.is_valid():
            # Update User model fields
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Save the student profile
            student_profile = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                student_profile.profile_picture = request.FILES['profile_picture']
            student_profile.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect('eduwize_app:profile')
    else:
        form = ProfileUpdateForm(instance=student, user=request.user)

    # Calculate additional context data
    completed_courses = Enrollment.objects.filter(
        student=student,
        completed_at__isnull=False
    ).count()

    # Get average score from performance analysis
    avg_score = PerformanceAnalysis.objects.filter(
        student=student
    ).aggregate(Avg('score'))['score__avg']

    if avg_score is not None:
        avg_score = round(avg_score)
    else:
        avg_score = 0

    context = {
        'student': student,
        'form': form,
        'completed_courses': completed_courses,
        'avg_score': avg_score
    }

    return render(request, 'eduwize_app/profile.html', context)

@login_required
def settings_view(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        student = None
        messages.error(request, "No student profile found. Please contact an administrator.")
        return redirect('eduwize_app:home')

    if request.method == 'POST':
        # Handle password update
        if 'update_password' in request.POST:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not request.user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            elif len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Keep user logged in
                messages.success(request, "Your password has been updated successfully!")

        # Handle notification settings
        elif 'update_notifications' in request.POST:
            # In a real app, you would save these to a user preferences model
            email_notifications = 'email_notifications' in request.POST
            assignment_reminders = 'assignment_reminders' in request.POST
            course_updates = 'course_updates' in request.POST

            # For now, just show a success message
            messages.success(request, "Notification settings updated successfully!")

        # Handle privacy settings
        elif 'update_privacy' in request.POST:
            # In a real app, you would save these to a user preferences model
            public_profile = 'public_profile' in request.POST
            show_courses = 'show_courses' in request.POST
            show_achievements = 'show_achievements' in request.POST

            # For now, just show a success message
            messages.success(request, "Privacy settings updated successfully!")

        # Handle AI settings
        elif 'update_ai_settings' in request.POST:
            # In a real app, you would save these to a user preferences model
            ai_recommendations = 'ai_recommendations' in request.POST
            ai_feedback = 'ai_feedback' in request.POST
            ai_model = request.POST.get('ai_model')

            # For now, just show a success message
            messages.success(request, "AI settings updated successfully!")

    return render(request, 'eduwize_app/settings.html', {'student': student})



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = is_admin(self.request.user)
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'eduwize_app/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = is_admin(self.request.user)
        return context

@method_decorator(admin_required, name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    template_name = 'eduwize_app/course_form.html'
    fields = ['name', 'description', 'level', 'thumbnail', 'duration', 'prerequisites', 'tags']
    success_url = reverse_lazy('eduwize_app:course-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Course '{form.instance.name}' was created successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the course. Please check the form and try again.")
        return super().form_invalid(form)

@method_decorator(admin_required, name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'eduwize_app/course_form.html'
    fields = ['name', 'description', 'level', 'thumbnail', 'duration', 'prerequisites', 'tags']
    success_url = reverse_lazy('eduwize_app:course-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Course '{form.instance.name}' was updated successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the course. Please check the form and try again.")
        return super().form_invalid(form)

@method_decorator(admin_required, name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'eduwize_app/course_confirm_delete.html'
    success_url = reverse_lazy('eduwize_app:course-list')

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        course_name = course.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Course '{course_name}' was deleted successfully.")
        return response


# Enrollment Views
class EnrollmentListView(ListView):
    model = Enrollment
    template_name = 'eduwize_app/enrollment_list.html'
    context_object_name = 'enrollments'

class EnrollmentDetailView(DetailView):
    model = Enrollment
    template_name = 'eduwize_app/enrollment_detail.html'
    context_object_name = 'enrollment'

from django.urls import reverse

class EnrollmentCreateView(CreateView):
    model = Enrollment
    template_name = 'eduwize_app/enrollment_form.html'
    fields = ['course']  # Remove 'student' field

    def form_valid(self, form):
        # Automatically assign the current user as the student
        form.instance.student = self.request.user.student
        enrollment = form.save()
        course_id = enrollment.course.pk
        return redirect(reverse('eduwize_app:course-detail', kwargs={'pk': course_id}))

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
    fields = ['course', 'title', 'description', 'duration', 'max_score', 'pass_percentage']
    success_url = reverse_lazy('eduwize_app:quiz-list')

class QuizUpdateView(UpdateView):
    model = Quiz
    template_name = 'eduwize_app/quiz_form.html'
    fields = ['course', 'title', 'description', 'duration', 'max_score', 'pass_percentage']
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
    fields = ['quiz', 'question_text', 'options', 'correct_answers', 'question_type']
    success_url = reverse_lazy('eduwize_app:question-list')

class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'eduwize_app/question_form.html'
    fields = ['quiz', 'question_text', 'options', 'correct_answers', 'question_type']
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add real statistics for the performance dashboard
        context['total_quizzes_taken'] = PerformanceAnalysis.objects.count()

        # Calculate average score
        avg_score = PerformanceAnalysis.objects.aggregate(Avg('score'))['score__avg']
        context['average_score'] = round(avg_score) if avg_score else 0

        # Get highest score
        highest_score = PerformanceAnalysis.objects.aggregate(Max('score'))['score__max']
        context['highest_score'] = highest_score if highest_score else 0

        # Calculate total time spent (in hours)
        # Note: This assumes time_taken is stored as a DurationField
        total_time = PerformanceAnalysis.objects.filter(time_taken__isnull=False).aggregate(
            Sum('time_taken')
        )['time_taken__sum']

        if total_time:
            # Convert to hours and round to 1 decimal place
            total_hours = total_time.total_seconds() / 3600
            context['total_time_spent'] = f"{total_hours:.1f}h"
        else:
            context['total_time_spent'] = "0h"

        # Get top performing students
        top_students = Student.objects.annotate(
            avg_score=Avg('performanceanalysis__score')
        ).filter(avg_score__isnull=False).order_by('-avg_score')[:5]
        context['top_students'] = top_students

        # Get most attempted quizzes
        most_attempted_quizzes = Quiz.objects.annotate(
            attempt_count=Count('performanceanalysis')
        ).order_by('-attempt_count')[:5]
        context['most_attempted_quizzes'] = most_attempted_quizzes

        return context

class PerformanceDetailView(DetailView):
    model = PerformanceAnalysis
    template_name = 'eduwize_app/performance_detail.html'
    context_object_name = 'performance'


# Notification Views
class NotificationsListView(ListView):
    model = Notification
    template_name = 'eduwize_app/notifications_list.html'
    context_object_name = 'notifications'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # If user is authenticated, only show their notifications
        if self.request.user.is_authenticated:
            try:
                queryset = queryset.filter(student=self.request.user.student)
            except:
                # If user doesn't have a student profile, show no notifications
                queryset = Notification.objects.none()
        else:
            # If user is not authenticated, show no notifications
            queryset = Notification.objects.none()

        # Order by created_at (newest first)
        queryset = queryset.order_by('-created_at')

        return queryset

    def post(self, request, *args, **kwargs):
        # Handle mark all as read functionality
        if 'mark_all_read' in request.POST:
            if request.user.is_authenticated:
                try:
                    # Get all unread notifications for this user
                    unread_notifications = Notification.objects.filter(
                        student=request.user.student,
                        is_read=False
                    )

                    # Mark them all as read
                    unread_notifications.update(is_read=True)

                    messages.success(request, "All notifications marked as read.")
                except:
                    messages.error(request, "Failed to mark notifications as read.")

            # Redirect back to notifications page
            return redirect('eduwize_app:notifications-list')

        return super().get(request, *args, **kwargs)


# Feedback Views
class FeedbackFormView(CreateView):
    model = Feedback
    template_name = 'eduwize_app/feedback_form.html'
    fields = ['student', 'feedback', 'rating']
    success_url = reverse_lazy('eduwize_app:home')


# AI Chatbot Views
@method_decorator(login_required, name='dispatch')
class AIChatbotView(View):
    template_name = 'eduwize_app/ai_chatbot_form.html'

    # Knowledge base for NCV curriculum
    knowledge_base = {
        "Mathematics": {
            "NQF Level 2": "Basic arithmetic, algebra, and geometry.",
            "NQF Level 3": "Intermediate algebra, trigonometry, and statistics.",
            "NQF Level 4": "Advanced algebra, calculus, and probability."
        },
        "English": {
            "NQF Level 2": "Basic reading, writing, and communication skills.",
            "NQF Level 3": "Intermediate reading, writing, and communication skills.",
            "NQF Level 4": "Advanced reading, writing, and communication skills."
        },
        "Life Orientation": {
            "NQF Level 2": "Basic life skills, personal development, and career guidance.",
            "NQF Level 3": "Intermediate life skills, personal development, and career guidance.",
            "NQF Level 4": "Advanced life skills, personal development, and career guidance."
        }
    }
    # Add more subjects and topics to the knowledge base
    knowledge_base["Electrical Engineering"] = {
        "NQF Level 2": "Basic electrical circuits, components, and safety.",
        "NQF Level 3": "Intermediate electrical circuits, digital electronics, and programming.",
        "NQF Level 4": "Advanced electrical circuits, power systems, and control systems."
    }
    knowledge_base["Mechanical Engineering"] = {
        "NQF Level 2": "Basic mechanical principles, tools, and safety.",
        "NQF Level 3": "Intermediate mechanical principles, manufacturing processes, and CAD.",
        "NQF Level 4": "Advanced mechanical principles, thermodynamics, and machine design."
    }

    def get(self, request):
        # Get previous chat messages for this user
        previous_messages = []

        # If user is authenticated and has a student profile
        if request.user.is_authenticated:
            try:
                # Get the last 10 chat messages
                chatbot_messages = AIChatbot.objects.filter(
                    student=request.user.student
                ).order_by('-created_at')[:10]

                # Format messages for the template
                for message in reversed(list(chatbot_messages)):
                    previous_messages.append({
                        'is_user': True,
                        'text': message.question,
                        'timestamp': message.created_at.strftime('%H:%M')
                    })
                    previous_messages.append({
                        'is_user': False,
                        'text': message.answer,
                        'timestamp': message.created_at.strftime('%H:%M')
                    })
            except:
                # Handle case where user doesn't have a student profile
                pass

        return render(request, self.template_name, {
            'previous_messages': previous_messages
        })

    def post(self, request):
        # Get the question from the form
        question = request.POST.get('question', '')

        if not question:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Question is required'}, status=400)
            return redirect('eduwize_app:ai-chatbot')

        # Generate an answer using our specialized AI model
        answer = self.generate_answer(question)

        # Save the chat message
        chat = None
        if request.user.is_authenticated:
            try:
                chat = AIChatbot.objects.create(
                    student=request.user.student,
                    question=question,
                    answer=answer
                )
            except Exception as e:
                print(f"Error saving chat with student: {e}")
                # If user doesn't have a student profile, just create the chat without student
                chat = AIChatbot.objects.create(
                    question=question,
                    answer=answer
                )
        else:
            chat = AIChatbot.objects.create(
                question=question,
                answer=answer
            )

        # If this is an AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            response_data = {
                'question': question,
                'answer': answer,
                'timestamp': datetime.datetime.now().strftime('%H:%M')
            }

            # Add chat ID if available
            if chat:
                response_data['chat_id'] = chat.id

            return JsonResponse(response_data)

        # Otherwise redirect back to the chatbot page
        return redirect('eduwize_app:ai-chatbot')

    def generate_answer(self, question):
        """
        Generate an answer based on the question using our specialized AI model.
        """
        # Import our AI model
        from .ai_models import BaseAIAssistant

        # Create an instance of our AI assistant
        ai_assistant = BaseAIAssistant()

        # Access knowledge base to provide context
        context = {}
        for subject, levels in self.knowledge_base.items():
            if subject.lower() in question.lower():
                context["subject"] = subject
                context["level"] = next((level for level in levels.keys() if level.lower() in question.lower()), None)
                break

        # Generate response using our specialized model
        try:
            response = ai_assistant.generate_response(
                prompt=question,
                context={
                    "task_type": "concept_teaching",
                    "subject": context.get("subject", "general"),
                    "depth": "intermediate"
                }
            )
            return response
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"I'm having trouble processing your request at the moment. Please try again later."


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
    template_name = 'eduwize_app/dark_home.html'  # Use the new dark theme template
    context_object_name = 'featured_courses'  # Changed to match the template
    paginate_by = 10
    ordering = ['-created_at']
    # queryset = Course.objects.all() # Fetch all courses - handled by get_queryset
    allow_empty = True
    extra_context = {'title': 'Home Page'}
    success_url = reverse_lazy('eduwize_app:home')

    def get_queryset(self):
        """
        Override the default queryset to order by creation date.
        """
        return Course.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add real statistics for the dashboard
        context['course_count'] = Course.objects.count()
        context['student_count'] = Student.objects.filter(status='active').count()
        context['ai_interactions'] = AIChatbot.objects.count()

        # Get top courses by enrollment
        top_courses = Course.objects.annotate(
            enrollment_count=Count('enrollment')
        ).order_by('-enrollment_count')[:5]
        context['top_courses'] = top_courses

        # Add recent activities if user is authenticated
        if self.request.user.is_authenticated:
            try:
                activities = ActivityLog.objects.filter(
                    student=self.request.user.student
                ).order_by('-created_at')[:5]
                context['activities'] = activities
            except:
                pass

            # Add upcoming quizzes
            try:
                quizzes = Quiz.objects.filter(
                    course__in=self.request.user.student.courses_enrolled.all()
                ).order_by('created_at')[:3]
                context['quizzes'] = quizzes
            except:
                pass

        return context


# Study Planner View
@method_decorator(login_required, name='dispatch')
class StudyPlannerView(TemplateView):
    template_name = 'eduwize_app/study_planner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the student
        try:
            student = self.request.user.student
            context['student'] = student

            # Get enrolled courses
            context['courses'] = student.courses_enrolled.all()

            # Get upcoming quizzes
            context['quizzes'] = Quiz.objects.filter(
                course__in=student.courses_enrolled.all()
            ).order_by('created_at')[:5]

        except:
            # Handle case where user doesn't have a student profile
            pass

        return context

def student_files_upload(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        for file in files:
            StudentFile.objects.create(student=request.user.student, file=file)
            return HttpResponse('Files uploaded successfully')
    else:
        form = StudentFileForm()
    return render(request, 'upload.html', {'form': form})


@never_cache
def health_check(request):
    """
    Health check endpoint for monitoring systems.
    Checks database connection and returns status.
    """
    status = 200
    db_conn = True

    # Check database connection
    try:
        db_conn = connections['default'].is_usable()
        if not db_conn:
            status = 500
    except OperationalError:
        db_conn = False
        status = 500

    # Check cache if needed
    # cache_status = cache.get('health_check_key', 'missing')
    # cache.set('health_check_key', 'available', 10)

    data = {
        'status': 'healthy' if status == 200 else 'unhealthy',
        'database': 'connected' if db_conn else 'disconnected',
        'timestamp': datetime.datetime.now().isoformat(),
    }

    return JsonResponse(data, status=status)


def offline_view(request):
    """
    View for the offline page when the app is used as a PWA without internet connection.
    """
    return render(request, 'eduwize_app/offline.html')


# Exam Paper Views
class ExamPaperListView(ListView):
    model = ExamPaper
    template_name = 'eduwize_app/exam_paper_list.html'
    context_object_name = 'exam_papers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by course if specified
        course_id = self.request.GET.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        # Filter by year if specified
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(year=year)

        # Filter by exam type if specified
        exam_type = self.request.GET.get('exam_type')
        if exam_type:
            queryset = queryset.filter(exam_type=exam_type)

        # Filter by level if specified
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)

        # Exclude solutions by default unless specifically requested
        show_solutions = self.request.GET.get('show_solutions')
        if not show_solutions or show_solutions.lower() != 'true':
            queryset = queryset.filter(is_solution=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add filter options to context
        context['courses'] = Course.objects.all()
        context['years'] = ExamPaper.objects.values_list('year', flat=True).distinct().order_by('-year')
        context['exam_types'] = ExamPaper.objects.values_list('exam_type', flat=True).distinct()
        context['levels'] = StudyLevelChoices.choices

        # Add current filter values to context
        context['current_filters'] = {
            'course': self.request.GET.get('course', ''),
            'year': self.request.GET.get('year', ''),
            'exam_type': self.request.GET.get('exam_type', ''),
            'level': self.request.GET.get('level', ''),
            'show_solutions': self.request.GET.get('show_solutions', 'false'),
        }

        # Add admin status to context
        context['is_admin'] = is_admin(self.request.user)

        return context

class ExamPaperDetailView(DetailView):
    model = ExamPaper
    template_name = 'eduwize_app/exam_paper_detail.html'
    context_object_name = 'exam_paper'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the exam paper
        exam_paper = self.get_object()

        # Increment view count
        exam_paper.increment_views()

        # Add solutions if this is a question paper
        if not exam_paper.is_solution:
            context['solutions'] = exam_paper.solutions.all()

        # Add related papers if this is a solution
        if exam_paper.is_solution and exam_paper.related_paper:
            context['question_paper'] = exam_paper.related_paper

        # Add other papers from the same course
        context['related_papers'] = ExamPaper.objects.filter(
            course=exam_paper.course
        ).exclude(
            id=exam_paper.id
        ).order_by('-year')[:5]

        # Add admin status to context
        context['is_admin'] = is_admin(self.request.user)

        return context

@method_decorator(admin_required, name='dispatch')
class ExamPaperCreateView(CreateView):
    model = ExamPaper
    form_class = ExamPaperForm
    template_name = 'eduwize_app/exam_paper_form.html'
    success_url = reverse_lazy('eduwize_app:exam-papers-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Exam paper '{form.instance.title}' was created successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the exam paper. Please check the form and try again.")
        return super().form_invalid(form)

@method_decorator(admin_required, name='dispatch')
class ExamPaperUpdateView(UpdateView):
    model = ExamPaper
    form_class = ExamPaperForm
    template_name = 'eduwize_app/exam_paper_form.html'
    success_url = reverse_lazy('eduwize_app:exam-papers-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Exam paper '{form.instance.title}' was updated successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the exam paper. Please check the form and try again.")
        return super().form_invalid(form)

@method_decorator(admin_required, name='dispatch')
class ExamPaperDeleteView(DeleteView):
    model = ExamPaper
    template_name = 'eduwize_app/exam_paper_confirm_delete.html'
    success_url = reverse_lazy('eduwize_app:exam-papers-list')

    def delete(self, request, *args, **kwargs):
        exam_paper = self.get_object()
        exam_paper_title = exam_paper.title
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Exam paper '{exam_paper_title}' was deleted successfully.")
        return response
