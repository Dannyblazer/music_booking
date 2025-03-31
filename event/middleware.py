import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info(f"Request: {request.method} {request.path} by {request.user}")
        return None

    def process_response(self, request, response):
        logger.info(f"Response: {response.status_code} for {request.method} {request.path}")
        return response