import os
import django
from pathlib import Path

import sys
sys.path.append("C:/Users/makha/OneDrive/Desktop/Eduwize")
sys.path.append("C:/Users/makha/OneDrive/Desktop/Eduwize/Eduwize")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eduwize.Eduwize.settings')
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ['DJANGO_SETTINGS_MODULE'] = 'Eduwize.settings'
django.setup()

try:
    from fun_zone.models import Hackathon
except Exception as e:
    print(f"Error importing Hackathon: {e}")
    raise

from django.utils import timezone

def populate():
    hackathons = [
        {'title': 'AI Hackathon', 'description': 'Build AI-powered solutions', 'start_date': timezone.now(), 'end_date': timezone.now() + timezone.timedelta(days=3), 'location': 'Online', 'prize': '$1000'},
        {'title': 'Web Development Hackathon', 'description': 'Create amazing web apps', 'start_date': timezone.now(), 'end_date': timezone.now() + timezone.timedelta(days=2), 'location': 'New York', 'prize': '$500'},
    ]

    for hackathon_data in hackathons:
        hackathon = Hackathon(**hackathon_data)
        hackathon.save()

if __name__ == '__main__':
    print('Populating hackathons...')
    populate()
    print('Hackathons populated!')