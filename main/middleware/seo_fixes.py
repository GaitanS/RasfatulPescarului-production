"""
SEO Middleware - Fixes for Google Search Console issues
Handles canonical URLs, redirects, and prevents duplicate content
"""

from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger('main')


class SEOMiddleware(MiddlewareMixin):
    """
    Middleware to handle common SEO issues:
    - Force trailing slashes (handled by CommonMiddleware but we log it)
    - Prevent URL parameter pollution
    - Log potential duplicate content issues
    """

    def process_request(self, request):
        """Process incoming request for SEO issues"""

        # Log requests with multiple query parameters (potential duplicate content)
        if len(request.GET) > 3:
            logger.warning(
                f"Multiple query parameters detected: {request.path}?{request.GET.urlencode()} "
                f"- May cause duplicate content issues"
            )

        # Force HTTPS in production (if not already)
        if not request.is_secure() and request.get_host() != '127.0.0.1:8000':
            # Let the web server handle this, just log
            logger.info(f"HTTP request detected: {request.build_absolute_uri()}")

        return None

    def process_response(self, request, response):
        """Process response to add SEO headers"""

        # Add X-Robots-Tag header for special cases
        if response.status_code == 404:
            response['X-Robots-Tag'] = 'noindex'

        # Log 500 errors for debugging Search Console issues
        if 500 <= response.status_code < 600:
            logger.error(
                f"Server error {response.status_code} for URL: {request.path} "
                f"- User agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
            )

        return response


class CanonicalURLMiddleware(MiddlewareMixin):
    """
    Middleware to enforce canonical URLs and prevent duplicate content
    """

    def process_request(self, request):
        """
        Redirect to canonical URL if needed
        """
        # Get the path without query string
        path = request.path
        query_string = request.META.get('QUERY_STRING', '')

        # List of allowed query parameters that don't create duplicate content
        allowed_params = ['page', 'category', 'county', 'search']

        # Check if we have query parameters
        if query_string:
            # Parse query string
            params = {}
            for param in query_string.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value

            # Check for problematic parameters
            problematic_params = [k for k in params.keys() if k not in allowed_params]

            if problematic_params:
                logger.warning(
                    f"Non-canonical URL detected: {path}?{query_string} "
                    f"- Problematic params: {problematic_params}"
                )

        return None


class RedirectMiddleware(MiddlewareMixin):
    """
    Handle common redirect issues to prevent chains
    """

    # Common old URLs that need redirects
    REDIRECTS = {
        '/locations/': '/locations/',  # Ensure trailing slash
        '/about-us/': '/about/',  # Old URL structure
        # Add more as needed
    }

    def process_request(self, request):
        """Check for old URLs and redirect"""

        path = request.path

        # Check if this path needs a redirect
        if path in self.REDIRECTS:
            new_path = self.REDIRECTS[path]
            if path != new_path:
                logger.info(f"Redirecting {path} -> {new_path}")
                return HttpResponsePermanentRedirect(new_path)

        return None
