#!/usr/bin/env python
"""
Simple SEO Test for Răsfățul Pescarului
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_basic_pages():
    """Test basic pages are accessible"""
    client = Client()
    
    pages = [
        ('/', 'Homepage'),
        ('/robots.txt', 'Robots.txt'),
        ('/sitemap.xml', 'Sitemap'),
        ('/ads.txt', 'Ads.txt'),
    ]
    
    print("🔍 Testing basic pages...")
    
    for url, name in pages:
        try:
            response = client.get(url, HTTP_HOST='testserver')
            if response.status_code == 200:
                print(f"✅ {name} ({url}) - OK")
            else:
                print(f"❌ {name} ({url}) - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {name} ({url}) - Error: {str(e)}")

def test_meta_tags():
    """Test meta tags in templates"""
    print("\n🏷️ Testing meta tags...")
    
    from django.template import Template, Context
    from django.template.loader import get_template
    
    try:
        # Test base template
        template = get_template('base.html')
        context = Context({
            'request': type('obj', (object,), {
                'get_full_path': lambda: '/',
                'build_absolute_uri': lambda x: f'https://rasfatul-pescarului.ro{x}'
            })()
        })
        
        rendered = template.render(context)
        
        # Check for essential meta tags
        checks = [
            ('meta name="description"', 'Meta description'),
            ('meta name="keywords"', 'Meta keywords'),
            ('meta property="og:title"', 'Open Graph title'),
            ('meta property="og:description"', 'Open Graph description'),
            ('link rel="canonical"', 'Canonical URL'),
            ('application/ld+json', 'Structured data'),
        ]
        
        for check, name in checks:
            if check in rendered:
                print(f"✅ {name} - Present")
            else:
                print(f"❌ {name} - Missing")
                
    except Exception as e:
        print(f"❌ Template test error: {str(e)}")

def test_sitemap():
    """Test sitemap generation"""
    print("\n🗺️ Testing sitemap...")
    
    try:
        from main.sitemaps import sitemaps
        print(f"✅ Sitemap classes loaded: {list(sitemaps.keys())}")
        
        # Test each sitemap
        for name, sitemap_class in sitemaps.items():
            try:
                sitemap = sitemap_class()
                items = sitemap.items()
                print(f"✅ {name} sitemap: {len(items)} items")
            except Exception as e:
                print(f"❌ {name} sitemap error: {str(e)}")
                
    except Exception as e:
        print(f"❌ Sitemap test error: {str(e)}")

def test_structured_data():
    """Test structured data generation"""
    print("\n📊 Testing structured data...")
    
    try:
        from main.templatetags.seo_tags import structured_data_website, structured_data_organization
        
        # Test website structured data
        website_data = structured_data_website()
        if 'application/ld+json' in website_data:
            print("✅ Website structured data - Generated")
        else:
            print("❌ Website structured data - Failed")
        
        # Test organization structured data
        org_data = structured_data_organization()
        if 'application/ld+json' in org_data:
            print("✅ Organization structured data - Generated")
        else:
            print("❌ Organization structured data - Failed")
            
    except Exception as e:
        print(f"❌ Structured data test error: {str(e)}")

if __name__ == '__main__':
    print("🚀 Starting Simple SEO Tests for Răsfățul Pescarului\n")
    
    test_basic_pages()
    test_meta_tags()
    test_sitemap()
    test_structured_data()
    
    print("\n✅ SEO tests completed!")
