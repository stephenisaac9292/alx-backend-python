# Django-Middleware-0x03/chats/middleware.py

from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from collections import defaultdict, deque
import logging
import os

# Set up logging
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requests.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# ========== MIDDLEWARE 1 ==========
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)

# ========== MIDDLEWARE 2 ==========
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_time = datetime.strptime("18:00", "%H:%M").time()
        self.end_time = datetime.strptime("21:00", "%H:%M").time()

    def __call__(self, request):
        now = datetime.now().time()
        if request.path.startswith("/chat/"):
            if not (self.start_time <= now <= self.end_time):
                return HttpResponseForbidden("Chat access allowed only between 6PM and 9PM.")
        return self.get_response(request)

# ========== MIDDLEWARE 3 ==========
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = defaultdict(deque)
        self.limit = 5
        self.time_window = timedelta(minutes=1)

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chat/'):
            ip = self.get_client_ip(request)
            now = datetime.now()
            msg_times = self.message_log[ip]

            # Clear old timestamps
            while msg_times and now - msg_times[0] > self.time_window:
                msg_times.popleft()

            if len(msg_times) >= self.limit:
                return HttpResponseForbidden("Message rate limit exceeded. Try again later.")

            msg_times.append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')
