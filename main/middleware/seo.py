"""
SEO Middleware for Răsfățul Pescarului
Automatically adds meta tags and structured data
"""

from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from main.utils.breadcrumbs import get_breadcrumbs_for_view


class SEOMiddleware(MiddlewareMixin):
    """
    Middleware to automatically add SEO-related context to all views
    """
    
    def process_template_response(self, request, response):
        """
        Add SEO context to template responses
        """
        if hasattr(response, 'context_data') and response.context_data is not None:
            # Get current view info
            resolver_match = resolve(request.path)
            view_name = f"{resolver_match.namespace}:{resolver_match.url_name}" if resolver_match.namespace else resolver_match.url_name
            
            # Add breadcrumbs based on current view
            if 'breadcrumbs' not in response.context_data:
                breadcrumbs = self.get_breadcrumbs_for_request(request, view_name, response.context_data)
                response.context_data['breadcrumbs'] = breadcrumbs
            
            # Add canonical URL if not set
            if 'canonical_url' not in response.context_data:
                response.context_data['canonical_url'] = request.build_absolute_uri(request.path)
            
            # Add current URL for social sharing
            response.context_data['current_url'] = request.build_absolute_uri(request.path)
            
            # Add site info
            response.context_data['site_name'] = 'Răsfățul Pescarului'
            response.context_data['site_url'] = 'https://rasfatul-pescarului.ro'
        
        return response
    
    def get_breadcrumbs_for_request(self, request, view_name, context):
        """
        Get breadcrumbs for the current request
        """
        try:
            # Get object from context if available
            kwargs = {}
            
            if 'lake' in context:
                kwargs['lake'] = context['lake']
            elif 'county' in context:
                kwargs['county'] = context['county']
            elif 'product' in context:
                kwargs['product'] = context['product']
            elif 'category' in context:
                kwargs['category'] = context['category']
            
            return get_breadcrumbs_for_view(view_name, **kwargs)
        except Exception:
            # Return empty breadcrumbs if something goes wrong
            return []


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers for better SEO and security
    """
    
    def process_response(self, request, response):
        """
        Add security headers to response
        """
        # X-Content-Type-Options
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options
        response['X-Frame-Options'] = 'DENY'
        
        # X-XSS-Protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy (basic)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
            "https://cdn.jsdelivr.net https://cdnjs.cloudflare.com "
            "https://code.jquery.com https://pagead2.googlesyndication.com "
            "https://www.googletagmanager.com https://www.google-analytics.com "
            "https://unpkg.com https://ep1.adtrafficquality.google "
            "https://ep2.adtrafficquality.google; "
            "style-src 'self' 'unsafe-inline' "
            "https://cdn.jsdelivr.net https://cdnjs.cloudflare.com "
            "https://fonts.googleapis.com https://unpkg.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https: http:; "
            "connect-src 'self' https://www.google-analytics.com "
            "https://ep1.adtrafficquality.google https://ep2.adtrafficquality.google; "
            "frame-src https://www.google.com https://pagead2.googlesyndication.com;"
        )
        response['Content-Security-Policy'] = csp
        
        return response


class CacheControlMiddleware(MiddlewareMixin):
    """
    Add appropriate cache headers for different content types
    """
    
    def process_response(self, request, response):
        """
        Add cache control headers based on content type and path
        """
        path = request.path
        
        # Static files - long cache
        if path.startswith('/static/') or path.startswith('/media/'):
            response['Cache-Control'] = 'public, max-age=31536000'  # 1 year
        
        # API endpoints - short cache
        elif path.startswith('/api/'):
            response['Cache-Control'] = 'public, max-age=300'  # 5 minutes
        
        # Sitemap and robots - medium cache
        elif path in ['/sitemap.xml', '/robots.txt', '/ads.txt']:
            response['Cache-Control'] = 'public, max-age=86400'  # 1 day
        
        # Regular pages - short cache
        else:
            response['Cache-Control'] = 'public, max-age=3600'  # 1 hour
        
        return response
