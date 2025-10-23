from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

# Import models cu try/except pentru a evita erorile
try:
    from .models import Lake, County, Article, FishingTerm, FishSpecies
except ImportError:
    Lake = None
    County = None
    Article = None
    FishingTerm = None
    FishSpecies = None

class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            'main:home',
            'main:about',
            'main:contact',
            'main:privacy',
            'main:faq',
            'main:ghid_incepatori',
            'main:solunar_calendar',
            'main:locations_list',
            'main:blog_home',
            'main:fishing_dictionary',
            'main:fish_species_list'
        ]

    def location(self, item):
        try:
            return reverse(item)
        except:
            if item == 'main:home':
                return '/'
            return f'/{item.split(":")[-1]}/'

    def lastmod(self, item):
        # Return current time for all static pages
        return timezone.now()

    def priority(self, item):
        priorities = {
            'main:home': 1.0,
            'main:locations_list': 0.9,
            'main:blog_home': 0.9,
            'main:fishing_dictionary': 0.8,
            'main:fish_species_list': 0.8,
            'main:solunar_calendar': 0.8,
            'main:ghid_incepatori': 0.8,
            'main:faq': 0.7,
            'main:about': 0.6,
            'main:contact': 0.6,
            'main:privacy': 0.4
        }
        return priorities.get(item, 0.5)

class LakeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        if Lake:
            return Lake.objects.filter(is_active=True).order_by('-updated_at')[:1000]
        return []

    def lastmod(self, obj):
        return getattr(obj, 'updated_at', timezone.now())

    def location(self, obj):
        return f'/locations/lake/{obj.slug}/'

    def priority(self, obj):
        # Higher priority for lakes with more views or recent updates
        if hasattr(obj, 'views_count') and obj.views_count > 100:
            return 0.9
        return 0.8

class CountySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    protocol = 'https'

    def items(self):
        if County:
            return County.objects.all().order_by('name')
        return []

    def location(self, obj):
        return f'/locations/county/{obj.slug}/'

    def lastmod(self, obj):
        return getattr(obj, 'updated_at', timezone.now())

    def priority(self, obj):
        # Higher priority for counties with more lakes
        if hasattr(obj, 'lakes') and obj.lakes.count() > 10:
            return 0.8
        return 0.6

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        if Article:
            return Article.objects.filter(is_published=True).order_by('-published_date')
        return []

    def lastmod(self, obj):
        return getattr(obj, 'updated_at', timezone.now())

    def location(self, obj):
        return f'/blog/{obj.slug}/'

    def priority(self, obj):
        # Higher priority for featured articles
        if hasattr(obj, 'is_featured') and obj.is_featured:
            return 0.9
        return 0.8

class FishingTermSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        if FishingTerm:
            return FishingTerm.objects.filter(is_active=True).order_by('term')
        return []

    def lastmod(self, obj):
        return getattr(obj, 'updated_at', timezone.now())

    def location(self, obj):
        return f'/dictionar-pescuit/{obj.slug}/'

class FishSpeciesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        if FishSpecies:
            return FishSpecies.objects.filter(is_active=True).order_by('name')
        return []

    def lastmod(self, obj):
        return getattr(obj, 'updated_at', timezone.now())

    def location(self, obj):
        return f'/specii-de-pesti/{obj.slug}/'

class CountyGuideSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        if County:
            # Filter counties that have guide content populated
            return County.objects.exclude(guide_content='').exclude(guide_content__isnull=True).order_by('name')
        return []

    def lastmod(self, obj):
        return getattr(obj, 'updated_at', timezone.now())

    def location(self, obj):
        return f'/judete/{obj.slug}/ghid/'

# Definește sitemaps
sitemaps = {
    'static': StaticViewSitemap,
}

# Adaugă sitemaps pentru modele doar dacă există
if Lake:
    sitemaps['lakes'] = LakeSitemap
if County:
    sitemaps['counties'] = CountySitemap
    sitemaps['county-guides'] = CountyGuideSitemap
if Article:
    sitemaps['articles'] = ArticleSitemap
if FishingTerm:
    sitemaps['fishing-terms'] = FishingTermSitemap
if FishSpecies:
    sitemaps['fish-species'] = FishSpeciesSitemap
