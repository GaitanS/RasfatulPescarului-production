#!/usr/bin/env python
"""
SEO Health Check Script for Răsfățul Pescarului
Checks various SEO aspects of the website
"""

import os
import sys
import django
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from django.urls import reverse
from django.test import Client
from main.models import Lake, County


class SEOChecker:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.client = Client()
        self.issues = []
        self.successes = []
    
    def log_issue(self, issue):
        """Log an SEO issue"""
        self.issues.append(issue)
        print(f"❌ {issue}")
    
    def log_success(self, success):
        """Log a successful check"""
        self.successes.append(success)
        print(f"✅ {success}")
    
    def check_page_seo(self, url, expected_title=None):
        """Check SEO elements of a specific page"""
        try:
            response = self.client.get(url)
            if response.status_code != 200:
                self.log_issue(f"Page {url} returns status {response.status_code}")
                return
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check title
            title = soup.find('title')
            if title:
                title_text = title.get_text().strip()
                if len(title_text) < 30:
                    self.log_issue(f"Title too short on {url}: '{title_text}'")
                elif len(title_text) > 60:
                    self.log_issue(f"Title too long on {url}: '{title_text}'")
                else:
                    self.log_success(f"Good title length on {url}")
                
                if expected_title and expected_title not in title_text:
                    self.log_issue(f"Title doesn't contain expected text '{expected_title}' on {url}")
            else:
                self.log_issue(f"Missing title tag on {url}")
            
            # Check meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                desc_content = meta_desc.get('content', '').strip()
                if len(desc_content) < 120:
                    self.log_issue(f"Meta description too short on {url}: '{desc_content}'")
                elif len(desc_content) > 160:
                    self.log_issue(f"Meta description too long on {url}: '{desc_content}'")
                else:
                    self.log_success(f"Good meta description length on {url}")
            else:
                self.log_issue(f"Missing meta description on {url}")
            
            # Check canonical URL
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            if canonical:
                self.log_success(f"Canonical URL present on {url}")
            else:
                self.log_issue(f"Missing canonical URL on {url}")
            
            # Check Open Graph tags
            og_title = soup.find('meta', attrs={'property': 'og:title'})
            og_desc = soup.find('meta', attrs={'property': 'og:description'})
            og_image = soup.find('meta', attrs={'property': 'og:image'})
            
            if og_title and og_desc and og_image:
                self.log_success(f"Complete Open Graph tags on {url}")
            else:
                missing = []
                if not og_title: missing.append('og:title')
                if not og_desc: missing.append('og:description')
                if not og_image: missing.append('og:image')
                self.log_issue(f"Missing Open Graph tags on {url}: {', '.join(missing)}")
            
            # Check structured data
            structured_data = soup.find_all('script', attrs={'type': 'application/ld+json'})
            if structured_data:
                self.log_success(f"Structured data present on {url} ({len(structured_data)} scripts)")
                
                # Validate JSON
                for script in structured_data:
                    try:
                        json.loads(script.get_text())
                    except json.JSONDecodeError:
                        self.log_issue(f"Invalid JSON-LD on {url}")
            else:
                self.log_issue(f"No structured data on {url}")
            
            # Check headings structure
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            h1_count = len(soup.find_all('h1'))
            
            if h1_count == 0:
                self.log_issue(f"No H1 tag on {url}")
            elif h1_count > 1:
                self.log_issue(f"Multiple H1 tags on {url} ({h1_count})")
            else:
                self.log_success(f"Proper H1 structure on {url}")
            
            # Check images alt text
            images = soup.find_all('img')
            images_without_alt = [img for img in images if not img.get('alt')]
            if images_without_alt:
                self.log_issue(f"Images without alt text on {url}: {len(images_without_alt)}")
            elif images:
                self.log_success(f"All images have alt text on {url}")
        
        except Exception as e:
            self.log_issue(f"Error checking {url}: {str(e)}")
    
    def check_technical_seo(self):
        """Check technical SEO aspects"""
        print("\n🔧 Checking Technical SEO...")
        
        # Check robots.txt
        try:
            response = self.client.get('/robots.txt')
            if response.status_code == 200:
                self.log_success("robots.txt is accessible")
                content = response.content.decode('utf-8')
                if 'Sitemap:' in content:
                    self.log_success("Sitemap declared in robots.txt")
                else:
                    self.log_issue("Sitemap not declared in robots.txt")
            else:
                self.log_issue("robots.txt not accessible")
        except Exception as e:
            self.log_issue(f"Error checking robots.txt: {str(e)}")
        
        # Check sitemap.xml
        try:
            response = self.client.get('/sitemap.xml')
            if response.status_code == 200:
                self.log_success("sitemap.xml is accessible")
            else:
                self.log_issue("sitemap.xml not accessible")
        except Exception as e:
            self.log_issue(f"Error checking sitemap.xml: {str(e)}")
        
        # Check ads.txt
        try:
            response = self.client.get('/ads.txt')
            if response.status_code == 200:
                self.log_success("ads.txt is accessible")
                content = response.content.decode('utf-8')
                if 'google.com' in content:
                    self.log_success("Google AdSense declared in ads.txt")
                else:
                    self.log_issue("Google AdSense not found in ads.txt")
            else:
                self.log_issue("ads.txt not accessible")
        except Exception as e:
            self.log_issue(f"Error checking ads.txt: {str(e)}")
    
    def check_main_pages(self):
        """Check main pages SEO"""
        print("\n📄 Checking Main Pages...")
        
        pages = [
            ('/', 'Răsfățul Pescarului'),
            ('/about/', 'Despre'),
            ('/contact/', 'Contact'),
            ('/privacy/', 'Confidențialitate'),
            ('/locations/', 'Locuri'),
            ('/solunar-calendar/', 'Calendar'),
        ]
        
        for url, expected_title in pages:
            self.check_page_seo(url, expected_title)
    
    def check_dynamic_pages(self):
        """Check dynamic pages SEO"""
        print("\n🏞️ Checking Dynamic Pages...")
        
        # Check a few lakes
        lakes = Lake.objects.filter(is_active=True)[:3]
        for lake in lakes:
            url = f'/locations/lake/{lake.slug}/'
            self.check_page_seo(url, lake.name)
        
        # Check a few counties
        counties = County.objects.all()[:3]
        for county in counties:
            url = f'/locations/county/{county.slug}/'
            self.check_page_seo(url, county.name)
    
    def run_full_check(self):
        """Run complete SEO check"""
        print("🚀 Starting SEO Health Check for Răsfățul Pescarului\n")
        
        self.check_technical_seo()
        self.check_main_pages()
        self.check_dynamic_pages()
        
        print(f"\n📊 SEO Check Results:")
        print(f"✅ Successes: {len(self.successes)}")
        print(f"❌ Issues: {len(self.issues)}")
        
        if self.issues:
            print(f"\n🔧 Issues to fix:")
            for issue in self.issues:
                print(f"  • {issue}")
        
        if len(self.issues) == 0:
            print("\n🎉 Perfect! No SEO issues found!")
        elif len(self.issues) < 5:
            print("\n👍 Good! Only minor SEO issues found.")
        else:
            print("\n⚠️ Several SEO issues need attention.")
        
        return len(self.issues) == 0


if __name__ == '__main__':
    checker = SEOChecker()
    success = checker.run_full_check()
    sys.exit(0 if success else 1)
