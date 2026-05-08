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

# Run migrations and create superuser automatically on Vercel startup
if os.environ.get('VERCEL') or 'VERCEL_URL' in os.environ:
    try:
        print("Running migrations...")
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Migration error: {e}")

    # Create default superuser if it doesn't exist
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@coruscant.com', 'ComplexPass123!')
            print("Superuser 'admin' created.")
        else:
            # Make sure the existing admin user is a superuser
            admin_user = User.objects.get(username='admin')
            if not admin_user.is_superuser:
                admin_user.is_superuser = True
                admin_user.is_staff = True
                admin_user.save()
                print("Existing 'admin' user promoted to superuser.")
    except Exception as e:
        print(f"Superuser creation error: {e}")

app = application
