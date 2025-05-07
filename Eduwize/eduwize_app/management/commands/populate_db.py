from django.core.management.base import BaseCommand
from eduwize_app.models import Course, Quiz, Question, StudyMaterial, Tags
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the database with initial courses, quizzes, and study resources'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Create some tags
        tags = ['Python', 'Django', 'JavaScript', 'HTML', 'CSS', 'Data Science', 'Machine Learning']
        tag_objects = []
        for tag in tags:
            tag_object, created = Tags.objects.get_or_create(name=tag, slug=slugify(tag))
            tag_objects.append(tag_object)

        # Create some courses
        course1 = Course.objects.create(
            name='Introduction to Python',
            description='A beginner-friendly introduction to the Python programming language.',
            level='NQF4',
            duration='8 weeks'
        )
        course1.tags.set(tag_objects[:2]) # Python, Django

        course2 = Course.objects.create(
            name='Web Development with Django',
            description='Learn how to build web applications using the Django framework.',
            level='NQF4',
            duration='12 weeks'
        )
        course2.tags.set(tag_objects[1:3]) # Django, JavaScript

        course3 = Course.objects.create(
            name='Data Science Fundamentals',
            description='An introduction to the fundamental concepts of data science.',
            level='NQF4',
            duration='10 weeks'
        )
        course3.tags.set(tag_objects[5:]) # Data Science, Machine Learning

        # Create some quizzes for course1
        quiz1 = Quiz.objects.create(
            course=course1,
            title='Python Basics Quiz',
            description='A quiz to test your knowledge of Python basics.',
            duration='30 minutes',
            max_score=20,
            pass_percentage=70
        )

        # Create some questions for quiz1
        Question.objects.create(
            quiz=quiz1,
            question_text='What is the correct syntax to output "Hello World" in Python?',
            options='{"a": "print("Hello World")", "b": "echo "Hello World"", "c": "System.out.println("Hello World")", "d": "printf("Hello World")"}',
            correct_answers='["a"]',
            question_type='multiple_choice'
        )
        Question.objects.create(
            quiz=quiz1,
            question_text='Which of the following is NOT a valid data type in Python?',
            options='{"a": "int", "b": "float", "c": "string", "d": "boolean"}',
            correct_answers='["c"]',
            question_type='multiple_choice'
        )

        # Create some study materials for course1
        StudyMaterial.objects.create(
            course=course1,
            title='Python Tutorial',
            description='A comprehensive tutorial on the Python programming language.',
            file='study_materials/python_tutorial.pdf',
            resource_type='document'
        )
        StudyMaterial.objects.create(
            course=course1,
            title='Python Basics Video',
            description='A video explaining the basics of Python programming.',
            file='study_materials/python_basics.mp4',
            resource_type='video'
        )

        self.stdout.write(self.style.SUCCESS('Database population complete!'))