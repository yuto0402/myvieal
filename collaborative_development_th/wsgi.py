import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "collaborative_development_th.settings.dev")

application = get_wsgi_application()
