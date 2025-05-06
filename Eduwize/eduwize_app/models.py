from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Choices
class StudyLevelChoices(models.TextChoices):

    LEVEL_2 = 'NQF2', 'NQF Level 2'
    LEVEL_3 = 'NQF3', 'NQF Level 3'
    LEVEL_4 = 'NQF4', 'NQF Level 4'

class ResourceTypeChoices(models.TextChoices):
    VIDEO = 'video', 'Video'
    DOCUMENT = 'document', 'Document'
    EXAM_PAPER = 'exam_paper', 'Exam Paper'

class QuestionTypeChoices(models.TextChoices):
    MULTIPLE_CHOICE = 'multiple_choice', 'Multiple Choice'
    TRUE_FALSE = 'true_false', 'True/False'
    FILL_IN_BLANKS = 'fill_in_blanks', 'Fill in Blanks'
    SHORT_ANSWER = 'short_answer', 'Short Answer'
    ESSAY = 'essay', 'Essay'

# Models

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(
        max_length=5,
        choices=StudyLevelChoices.choices,
        default=StudyLevelChoices.LEVEL_2
    )
    student_id = models.CharField(max_length=9, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    courses_enrolled = models.ManyToManyField('Course', through='Enrollment')

    def __str__(self):
        return self.user.username

class StudentFile(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='profile_pictures/')
uploaded_at = models.DateTimeField(auto_now_add=True)

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    level = models.CharField(
        max_length=5,
        choices=StudyLevelChoices.choices
    )
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    duration = models.CharField(max_length=10)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    tags = models.ManyToManyField('Tags', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name}"

class StudyMaterial(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='study_materials/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    resource_type = models.CharField(
        max_length=10,
        choices=ResourceTypeChoices.choices,
        default=ResourceTypeChoices.VIDEO
    )
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=10)
    max_score = models.PositiveIntegerField(default=0)
    pass_percentage = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    options = models.JSONField()
    correct_answers = models.JSONField()
    question_type = models.CharField(
        max_length=20,
        choices=QuestionTypeChoices.choices,
        default=QuestionTypeChoices.MULTIPLE_CHOICE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text

class PerformanceAnalysis(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    completion_percentage = models.FloatField()
    time_taken = models.DurationField(null=True, blank=True)
    attempts = models.PositiveIntegerField(default=1)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.quiz.title}"

class Notification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.feedback

class AIChatbot(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='chatbot_messages')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_helpful = models.BooleanField(default=False)
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.question

class AIRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendation = models.TextField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recommendation

class Tags(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ActivityLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.TextField()
    activity_type = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.activity

class ExamPaper(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='exam_papers/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exam_papers')
    year = models.PositiveIntegerField(help_text="The year of the exam paper (e.g., 2023)")
    exam_type = models.CharField(max_length=50, help_text="Type of exam (e.g., Midterm, Final, Mock)")
    level = models.CharField(
        max_length=5,
        choices=StudyLevelChoices.choices,
        help_text="The study level this exam paper is for"
    )
    is_solution = models.BooleanField(default=False, help_text="Is this a solution paper?")
    related_paper = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='solutions', help_text="If this is a solution, link to the original paper")
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', 'exam_type']
        verbose_name = "Exam Paper"
        verbose_name_plural = "Exam Papers"

    def __str__(self):
        return f"{self.title} ({self.year})"

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
