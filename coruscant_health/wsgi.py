import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coruscant_health.settings')

# Get the WSGI application
application = get_wsgi_application()
app = application
