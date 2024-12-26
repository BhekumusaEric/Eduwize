from django.contrib import admin

# Register your models here.
from .models import Student, Course, Enrollment, StudyMaterial, Quiz, Question, PerformanceAnalysis, Notification, Feedback, AIChatbot, AIRecommendation, Tags, ActivityLog ,  StudentFile , StudyLevelChoices , ResourceTypeChoices 

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(StudyMaterial)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(PerformanceAnalysis)
admin.site.register(Notification)
admin.site.register(Feedback)
admin.site.register(AIChatbot)
admin.site.register(AIRecommendation)
admin.site.register(Tags)
admin.site.register(ActivityLog)
admin.site.register(StudentFile)
