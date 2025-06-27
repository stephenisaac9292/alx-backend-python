from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden
import logging
import os
from collections import defaultdict, deque

# Logger setup
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requests.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# ========= 1. RequestLoggingMiddleware ==========
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)

# ========= 2. RestrictAccessByTimeMiddleware ==========
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_time = time(18, 0)  # 6 PM
        self.end_time = time(21, 0)    # 9 PM

    def __call__(self, request):
        now = datetime.now().time()
        if request.path.startswith("/chat/"):
            if not (self.start_time <= now <= self.end_time):
                return HttpResponseForbidden("Chat access allowed only between 6PM and 9PM.")
        return self.get_response(request)

# ========= 3. OffensiveLanguageMiddleware ==========
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = defaultdict(deque)
        self.limit = 5
        self.time_window = timedelta(minutes=1)

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/chat/"):
            ip = self.get_client_ip(request)
            now = datetime.now()
            times = self.message_log[ip]

            while times and now - times[0] > self.time_window:
                times.popleft()

            if len(times) >= self.limit:
                return HttpResponseForbidden("Message rate limit exceeded. Try again later.")

            times.append(now)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')

# ========= 4. RolepermissionMiddleware ==========
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/chat/"):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("User not authenticated.")
            if not (request.user.is_superuser or request.user.is_staff):
                return HttpResponseForbidden("Only admin or moderator can access this action.")
        return self.get_response(request)
