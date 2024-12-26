from django import forms
from .models import Student, Course, Enrollment, StudyMaterial, Quiz, Question, PerformanceAnalysis, Notification, Feedback, AIChatbot, AIRecommendation, Tags, ActivityLog ,  StudentFile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# **1. Student Form**
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_picture', 'bio', 'date_of_birth']
        widgets = {
            'profile_picture': forms.ClearableFileInput(),
        }
# **2. Course Form**
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'level', 'thumbnail', 'duration']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Customizing the description field
            'thumbnail': forms.ClearableFileInput(),  # Removed 'multiple': False, as it's unnecessary
        }

# **3. Enrollment Form**
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']

# **4. Study Materials Form**
class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'file', 'course', 'resource_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'file': forms.ClearableFileInput(),
        }

# **5. Quiz Form**
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course', 'title', 'description', 'duration', 'max_score', 'pass_percentage']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

# **6. Question Form**
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'question_text', 'options', 'correct_answers', 'question_type']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

# **7. Performance Analysis Form**
class PerformanceForm(forms.ModelForm):
    class Meta:
        model = PerformanceAnalysis
        fields = ['student', 'quiz', 'score', 'completion_percentage', 'time_taken', 'attempts']

# **8. Notification Form**
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['student', 'message', 'is_read']
        widgets = {
            'date_posted': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# **9. Feedback Form**
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['student', 'feedback', 'rating']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

# **10. AI Chatbot Form**
class AIChatbotForm(forms.ModelForm):
    class Meta:
        model = AIChatbot
        fields = ['question', 'answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

# **11. AI Recommendations Form**
class AIRecommendationForm(forms.ModelForm):
    class Meta:
        model = AIRecommendation
        fields = ['recommendation']
        widgets = {
            'recommendation': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

# **12. Tags Form**
class TagsForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['name', 'slug']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

# **13. Activity Log Form**
class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = ['student', 'activity']
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class StudentFileForm(forms.ModelForm):
    class Meta:
        model = StudentFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(),
            }