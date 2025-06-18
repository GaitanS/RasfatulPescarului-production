#!/usr/bin/env python
"""
Live SEO Test for Răsfățul Pescarului
Tests the live website for SEO issues
"""

import requests
from bs4 import BeautifulSoup
import json
import time

def test_live_seo():
    """Test live website SEO"""
    base_url = 'https://rasfatul-pescarului.ro'
    
    print("🚀 Testing Live SEO for Răsfățul Pescarului\n")
    
    # Test basic pages
    pages = [
        ('/', 'Homepage'),
        ('/robots.txt', 'Robots.txt'),
        ('/sitemap.xml', 'Sitemap'),
        ('/ads.txt', 'Ads.txt'),
        ('/about/', 'About'),
        ('/contact/', 'Contact'),
        ('/locations/', 'Locations'),
        ('/solunar-calendar/', 'Solunar Calendar'),
    ]
    
    print("🔍 Testing page accessibility...")
    
    for path, name in pages:
        try:
            url = f"{base_url}{path}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {name} ({path}) - OK")
                
                # Test HTML pages for SEO elements
                if path.endswith('/') or path == '/':
                    test_page_seo(response.text, url, name)
                    
            else:
                print(f"❌ {name} ({path}) - Status: {response.status_code}")
                
        except requests.RequestException as e:
            print(f"❌ {name} ({path}) - Error: {str(e)}")
        
        time.sleep(0.5)  # Be respectful to the server

def test_page_seo(html_content, url, page_name):
    """Test SEO elements of a page"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check title
    title = soup.find('title')
    if title:
        title_text = title.get_text().strip()
        if 30 <= len(title_text) <= 60:
            print(f"  ✅ Good title length: {len(title_text)} chars")
        else:
            print(f"  ⚠️ Title length issue: {len(title_text)} chars")
    else:
        print(f"  ❌ Missing title tag")
    
    # Check meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        desc_content = meta_desc.get('content', '').strip()
        if 120 <= len(desc_content) <= 160:
            print(f"  ✅ Good meta description length: {len(desc_content)} chars")
        else:
            print(f"  ⚠️ Meta description length issue: {len(desc_content)} chars")
    else:
        print(f"  ❌ Missing meta description")
    
    # Check canonical URL
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical:
        print(f"  ✅ Canonical URL present")
    else:
        print(f"  ❌ Missing canonical URL")
    
    # Check Open Graph tags
    og_tags = ['og:title', 'og:description', 'og:image', 'og:url']
    missing_og = []
    
    for tag in og_tags:
        if not soup.find('meta', attrs={'property': tag}):
            missing_og.append(tag)
    
    if not missing_og:
        print(f"  ✅ All Open Graph tags present")
    else:
        print(f"  ⚠️ Missing OG tags: {', '.join(missing_og)}")
    
    # Check structured data
    structured_data = soup.find_all('script', attrs={'type': 'application/ld+json'})
    if structured_data:
        print(f"  ✅ Structured data present ({len(structured_data)} scripts)")
        
        # Validate JSON
        valid_json = 0
        for script in structured_data:
            try:
                json.loads(script.get_text())
                valid_json += 1
            except json.JSONDecodeError:
                pass
        
        if valid_json == len(structured_data):
            print(f"  ✅ All structured data is valid JSON")
        else:
            print(f"  ⚠️ Some structured data has invalid JSON")
    else:
        print(f"  ❌ No structured data found")
    
    # Check headings
    h1_tags = soup.find_all('h1')
    if len(h1_tags) == 1:
        print(f"  ✅ Proper H1 structure (1 tag)")
    elif len(h1_tags) == 0:
        print(f"  ❌ No H1 tag found")
    else:
        print(f"  ⚠️ Multiple H1 tags ({len(h1_tags)})")
    
    # Check images alt text
    images = soup.find_all('img')
    images_without_alt = [img for img in images if not img.get('alt')]
    
    if images:
        if not images_without_alt:
            print(f"  ✅ All images have alt text ({len(images)} images)")
        else:
            print(f"  ⚠️ {len(images_without_alt)}/{len(images)} images missing alt text")
    
    print()  # Empty line for readability

def test_technical_seo():
    """Test technical SEO aspects"""
    print("🔧 Testing Technical SEO...")
    
    base_url = 'https://rasfatul-pescarului.ro'
    
    # Test robots.txt
    try:
        response = requests.get(f"{base_url}/robots.txt", timeout=10)
        if response.status_code == 200:
            content = response.text
            if 'Sitemap:' in content:
                print("✅ robots.txt accessible with sitemap declaration")
            else:
                print("⚠️ robots.txt accessible but no sitemap declaration")
        else:
            print(f"❌ robots.txt not accessible (status: {response.status_code})")
    except requests.RequestException as e:
        print(f"❌ robots.txt error: {str(e)}")
    
    # Test sitemap.xml
    try:
        response = requests.get(f"{base_url}/sitemap.xml", timeout=10)
        if response.status_code == 200:
            print("✅ sitemap.xml accessible")
            
            # Check if it's valid XML
            try:
                soup = BeautifulSoup(response.content, 'xml')
                urls = soup.find_all('url')
                print(f"  ✅ Sitemap contains {len(urls)} URLs")
            except Exception:
                print("  ⚠️ Sitemap XML parsing issues")
        else:
            print(f"❌ sitemap.xml not accessible (status: {response.status_code})")
    except requests.RequestException as e:
        print(f"❌ sitemap.xml error: {str(e)}")
    
    # Test ads.txt
    try:
        response = requests.get(f"{base_url}/ads.txt", timeout=10)
        if response.status_code == 200:
            content = response.text
            if 'google.com' in content:
                print("✅ ads.txt accessible with Google AdSense")
            else:
                print("⚠️ ads.txt accessible but no Google AdSense found")
        else:
            print(f"❌ ads.txt not accessible (status: {response.status_code})")
    except requests.RequestException as e:
        print(f"❌ ads.txt error: {str(e)}")

def test_performance():
    """Test basic performance metrics"""
    print("\n⚡ Testing Performance...")
    
    base_url = 'https://rasfatul-pescarului.ro'
    
    try:
        start_time = time.time()
        response = requests.get(base_url, timeout=30)
        load_time = time.time() - start_time
        
        if response.status_code == 200:
            print(f"✅ Homepage loads in {load_time:.2f} seconds")
            
            if load_time < 3:
                print("  ✅ Good loading speed")
            elif load_time < 5:
                print("  ⚠️ Acceptable loading speed")
            else:
                print("  ❌ Slow loading speed")
            
            # Check response size
            content_length = len(response.content)
            print(f"  📊 Page size: {content_length / 1024:.1f} KB")
            
        else:
            print(f"❌ Homepage not accessible (status: {response.status_code})")
            
    except requests.RequestException as e:
        print(f"❌ Performance test error: {str(e)}")

if __name__ == '__main__':
    test_live_seo()
    test_technical_seo()
    test_performance()
    
    print("\n🎉 Live SEO test completed!")
    print("\n💡 Recommendations:")
    print("  • Monitor Core Web Vitals in Google Search Console")
    print("  • Check mobile usability regularly")
    print("  • Update content regularly for freshness")
    print("  • Monitor search rankings for target keywords")
