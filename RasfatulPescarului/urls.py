from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse

# Import sitemaps
try:
    from main.sitemaps import sitemaps
except ImportError:
    sitemaps = {}

# Servește ads.txt
def ads_txt(request):
    content = "google.com, pub-4988585637197167, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type="text/plain")

# Servește robots.txt
def robots_txt(request):
    content = """User-agent: *
Allow: /

# Sitemaps
Sitemap: https://rasfatul-pescarului.ro/sitemap.xml

# Disallow admin and private areas
Disallow: /admin/
Disallow: /accounts/
Disallow: /api/
Disallow: /static/admin/
Disallow: /media/private/
Disallow: /search?
Disallow: /*?page=
Disallow: /*?sort=
Disallow: /*?filter=

# Allow important content
Allow: /static/
Allow: /media/
Allow: /locations/
Allow: /solunar-calendar/
Allow: /about/
Allow: /contact/
Allow: /privacy/
Allow: /ads.txt

# Crawl delay for respectful crawling
Crawl-delay: 1

# Special rules for different bots
User-agent: Googlebot
Crawl-delay: 0

User-agent: Bingbot
Crawl-delay: 1

User-agent: facebookexternalhit
Allow: /"""
    return HttpResponse(content, content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Include main app URLs
    
    # SEO și monetizare
    path('ads.txt', ads_txt, name='ads_txt'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Serve media files in development and production
# În producție, WhiteNoise va servi fișierele media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
