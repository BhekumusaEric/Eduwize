from django.db import migrations
from django.utils import timezone

def add_sample_hackathons(apps, schema_editor):
    Hackathon = apps.get_model('fun_zone', 'Hackathon')
    Hackathon.objects.create(
        title='AI Hackathon',
        description='Build AI-powered solutions',
        start_date=timezone.now(),
        end_date=timezone.now() + timezone.timedelta(days=3),
        location='Online',
        prize='$1000'
    )
    Hackathon.objects.create(
        title='Web Development Hackathon',
        description='Create amazing web apps',
        start_date=timezone.now(),
        end_date=timezone.now() + timezone.timedelta(days=2),
        location='New York',
        prize='$500'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('fun_zone', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_sample_hackathons),
    ]