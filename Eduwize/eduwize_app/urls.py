from django.urls import path
from django.views.generic import TemplateView , ListView , DetailView , CreateView , UpdateView , DeleteView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'eduwize_app'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    # Student URLs
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('students/add/', views.StudentCreateView.as_view(), name='student-add'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student-edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),

    # Course URLs
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('courses/add/', views.CourseCreateView.as_view(), name='course-add'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course-edit'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),

    # Enrollment URLs
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('enrollments/add/', views.EnrollmentCreateView.as_view(), name='enrollment-add'),
    path('enrollments/<int:pk>/edit/', views.EnrollmentUpdateView.as_view(), name='enrollment-edit'),
    path('enrollments/<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='enrollment-delete'),

    # Study Material URLs
    path('study-materials/', views.StudyMaterialListView.as_view(), name='study-materials-list'),
    path('study-materials/<int:pk>/', views.StudyMaterialDetailView.as_view(), name='study-materials-detail'),
    path('study-materials/add/', views.StudyMaterialCreateView.as_view(), name='study-materials-add'),
    path('study-materials/<int:pk>/edit/', views.StudyMaterialUpdateView.as_view(), name='study-materials-edit'),
    path('study-materials/<int:pk>/delete/', views.StudyMaterialDeleteView.as_view(), name='study-materials-delete'),

    # Quiz URLs
    path('quizzes/', views.QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/add/', views.QuizCreateView.as_view(), name='quiz-add'),
    path('quizzes/<int:pk>/edit/', views.QuizUpdateView.as_view(), name='quiz-edit'),
    path('quizzes/<int:pk>/delete/', views.QuizDeleteView.as_view(), name='quiz-delete'),

    # Question URLs
    path('questions/', views.QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('questions/add/', views.QuestionCreateView.as_view(), name='question-add'),
    path('questions/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question-edit'),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question-delete'),

    # Performance Analysis
    path('performances/', views.PerformanceListView.as_view(), name='performance-list'),
    path('performances/<int:pk>/', views.PerformanceDetailView.as_view(), name='performance-detail'),

    # Exam Paper URLs
    path('exam-papers/', views.ExamPaperListView.as_view(), name='exam-papers-list'),
    path('exam-papers/<int:pk>/', views.ExamPaperDetailView.as_view(), name='exam-papers-detail'),
    path('exam-papers/add/', views.ExamPaperCreateView.as_view(), name='exam-papers-add'),
    path('exam-papers/<int:pk>/edit/', views.ExamPaperUpdateView.as_view(), name='exam-papers-edit'),
    path('exam-papers/<int:pk>/delete/', views.ExamPaperDeleteView.as_view(), name='exam-papers-delete'),

    # General Pages
    path('', views.HomePageView.as_view(), name='home'),
    path('home.html', views.HomePageView.as_view(), name='home'),
    path('notifications/', views.NotificationsListView.as_view(), name='notifications-list'),
    path('feedback/', views.FeedbackFormView.as_view(), name='feedback'),
    path('ai-chatbot/', views.AIChatbotView.as_view(), name='ai-chatbot'),
    path('ai-recommendations/', views.AIRecommendationsView.as_view(), name='ai-recommendations'),
    path('study-planner/', views.StudyPlannerView.as_view(), name='study-planner'),
    path('tags/', views.TagsListView.as_view(), name='tags'),
    path('activity-log/', views.ActivityLogView.as_view(), name='activity-log'),
    path('profile/', views.profile, name='profile'),

    # Health check endpoint
    path('health/', views.health_check, name='health-check'),

    # PWA offline page
    path('offline/', views.offline_view, name='offline'),
]
