import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

# Add the current directory to sys.path
path = os.path.dirname(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coruscant_health.settings')

# Initialize Django
application = get_wsgi_application()

# Run migrations automatically on Vercel startup
if os.environ.get('VERCEL') or 'VERCEL_URL' in os.environ:
    try:
        print("Running migrations...")
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Migration error: {e}")

app = application
