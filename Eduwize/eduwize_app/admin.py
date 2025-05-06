from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Student, Course, Enrollment, StudyMaterial, Quiz, Question, PerformanceAnalysis, Notification, Feedback, AIChatbot, AIRecommendation, Tags, ActivityLog, StudentFile, ExamPaper, StudyLevelChoices, ResourceTypeChoices

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'level_display', 'duration', 'created_at', 'thumbnail_preview')
    list_filter = ('level', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'thumbnail_preview')
    filter_horizontal = ('prerequisites', 'tags')

    fieldsets = (
        ('Course Information', {
            'fields': ('name', 'description', 'level', 'duration')
        }),
        ('Media', {
            'fields': ('thumbnail', 'thumbnail_preview'),
            'classes': ('collapse',)
        }),
        ('Relationships', {
            'fields': ('prerequisites', 'tags'),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def level_display(self, obj):
        return obj.get_level_display()
    level_display.short_description = 'Level'

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="100" height="auto" />', obj.thumbnail.url)
        return "No thumbnail"
    thumbnail_preview.short_description = 'Thumbnail Preview'

class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'resource_type', 'views', 'created_at')
    list_filter = ('resource_type', 'course', 'created_at')
    search_fields = ('title', 'description', 'course__name')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'completed_at')
    list_filter = ('enrolled_at', 'completed_at')
    search_fields = ('student__user__username', 'course__name')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration', 'max_score', 'pass_percentage')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'description', 'course__name')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'question_type', 'created_at')
    list_filter = ('question_type', 'quiz', 'created_at')
    search_fields = ('question_text', 'quiz__title')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Question Information', {
            'fields': ('quiz', 'question_text', 'question_type')
        }),
        ('Answer Options', {
            'fields': ('options', 'correct_answers'),
            'description': 'For options and correct answers, use valid JSON format. For multiple choice, options should be a list of strings, and correct_answers should be a list of indices or values.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'level', 'status', 'created_at')
    list_filter = ('level', 'status', 'created_at')
    search_fields = ('user__username', 'user__email', 'student_id', 'bio')
    readonly_fields = ('created_at', 'updated_at')

class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ExamPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'year', 'exam_type', 'level_display', 'is_solution', 'views', 'created_at')
    list_filter = ('year', 'exam_type', 'level', 'is_solution', 'course', 'created_at')
    search_fields = ('title', 'description', 'course__name', 'exam_type')
    readonly_fields = ('views', 'created_at', 'updated_at')

    fieldsets = (
        ('Paper Information', {
            'fields': ('title', 'description', 'file', 'course')
        }),
        ('Exam Details', {
            'fields': ('year', 'exam_type', 'level', 'is_solution', 'related_paper')
        }),
        ('Statistics', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def level_display(self, obj):
        return obj.get_level_display()
    level_display.short_description = 'Level'

admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(StudyMaterial, StudyMaterialAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(PerformanceAnalysis)
admin.site.register(Notification)
admin.site.register(Feedback)
admin.site.register(AIChatbot)
admin.site.register(AIRecommendation)
admin.site.register(Tags, TagsAdmin)
admin.site.register(ActivityLog)
admin.site.register(StudentFile)
admin.site.register(ExamPaper, ExamPaperAdmin)
