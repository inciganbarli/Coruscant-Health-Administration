import os
import sys

# Add the current directory to sys.path
path = os.path.dirname(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coruscant_health.settings')

try:
    application = get_wsgi_application()
    app = application
except Exception as e:
    print(f"Error loading WSGI application: {e}")
    raise e
