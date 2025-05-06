"""
WSGI config for PythonAnywhere deployment.
"""

import os
import sys

# Add your project directory to the sys.path
path = '/home/eduwize/Eduwize'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'Eduwize.settings'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_SECRET_KEY'] = 'your-secret-key-here'  # Replace with a secure key in production

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
