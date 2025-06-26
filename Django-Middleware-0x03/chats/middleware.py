# 0x03-MessagingApp-Django/chats/middleware.py

from datetime import datetime, time
from django.http import HttpResponseForbidden
import logging
import os

# Ensure log file is set
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requests.log')
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_time = time(18, 0)  # 6 PM
        self.end_time = time(21, 0)    # 9 PM

    def __call__(self, request):
        now = datetime.now().time()
        if request.path.startswith('/chat/'):
            if not (self.start_time <= now <= self.end_time):
                return HttpResponseForbidden("Chat access allowed only between 6PM and 9PM.")
        return self.get_response(request)
