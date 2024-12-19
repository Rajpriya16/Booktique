# middleware.py
from django.conf import settings

class AdminFrontendSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            # Admin site uses its own session configuration (database-backed)
            settings.SESSION_COOKIE_NAME = 'admin_sessionid'
            settings.SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Admin uses DB-based sessions
        else:
            # Frontend uses a different session configuration (e.g., cache-backed)
            settings.SESSION_COOKIE_NAME = 'frontend_sessionid'
            settings.SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'  # Example: cache-based sessions

        response = self.get_response(request)
        return response
