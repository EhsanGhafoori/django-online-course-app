from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from PIL import Image

from onlinecourse.models import Course, Lesson, Question, Choice, Enrollment


class Command(BaseCommand):
    help = 'Seed sample course, lessons, questions, and a test user for the final project'

    def handle(self, *args, **options):
        image = Image.new('RGB', (200, 120), color=(73, 109, 137))
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        image_file = ContentFile(buffer.getvalue(), name='course.png')

        course, _ = Course.objects.get_or_create(
            name='Cloud App Development',
            defaults={
                'description': 'Django online course final project sample course.',
                'total_enrollment': 1,
            },
        )
        if not course.image:
            course.image.save('course.png', image_file, save=True)

        Lesson.objects.get_or_create(
            course=course,
            order=1,
            defaults={
                'title': 'Introduction to Django',
                'content': 'Learn Django models, views, templates, and admin.',
            },
        )

        q1, _ = Question.objects.get_or_create(
            course=course,
            content='Is Django a Python framework',
            defaults={'grade': 100},
        )
        Choice.objects.get_or_create(
            question=q1, content='Yes', defaults={'is_correct': True})
        Choice.objects.get_or_create(
            question=q1, content='No', defaults={'is_correct': False})

        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Admin',
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            user.set_password('admin123')
            user.save()

        Enrollment.objects.get_or_create(user=user, course=course, defaults={'mode': 'honor'})
        self.stdout.write(self.style.SUCCESS('Seed data ready. Admin: admin / admin123'))
