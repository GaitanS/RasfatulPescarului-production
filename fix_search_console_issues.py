#!/usr/bin/env python
"""
Fix Search Console Issues for Răsfățul Pescarului
Addresses specific issues identified in Google Search Console
"""

import requests
from bs4 import BeautifulSoup
import time

def check_live_seo_issues():
    """Check specific SEO issues from Search Console"""
    base_url = 'https://rasfatul-pescarului.ro'
    
    print("🔍 Checking Live SEO Issues from Search Console\n")
    
    # Pages to check based on Search Console issues
    pages_to_check = [
        ('/', 'Homepage'),
        ('/about/', 'About Page'),
        ('/contact/', 'Contact Page'),
        ('/locations/', 'Locations Page'),
        ('/solunar-calendar/', 'Solunar Calendar'),
        ('/privacy/', 'Privacy Policy'),
    ]
    
    issues_found = []
    
    for path, name in pages_to_check:
        print(f"🔍 Checking {name} ({path})...")
        
        try:
            url = f"{base_url}{path}"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                issues_found.append(f"❌ {name}: HTTP {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            page_issues = []
            
            # Check title tag
            title = soup.find('title')
            if not title:
                page_issues.append("Missing title tag")
            elif len(title.get_text().strip()) < 30:
                page_issues.append(f"Title too short: {len(title.get_text().strip())} chars")
            elif len(title.get_text().strip()) > 60:
                page_issues.append(f"Title too long: {len(title.get_text().strip())} chars")
            
            # Check meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if not meta_desc:
                page_issues.append("Missing meta description")
            elif len(meta_desc.get('content', '').strip()) < 120:
                page_issues.append(f"Meta description too short: {len(meta_desc.get('content', '').strip())} chars")
            elif len(meta_desc.get('content', '').strip()) > 160:
                page_issues.append(f"Meta description too long: {len(meta_desc.get('content', '').strip())} chars")
            
            # Check canonical URL
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            if not canonical:
                page_issues.append("Missing canonical URL")
            
            # Check Open Graph tags
            og_title = soup.find('meta', attrs={'property': 'og:title'})
            og_desc = soup.find('meta', attrs={'property': 'og:description'})
            og_image = soup.find('meta', attrs={'property': 'og:image'})
            og_url = soup.find('meta', attrs={'property': 'og:url'})
            
            missing_og = []
            if not og_title: missing_og.append('og:title')
            if not og_desc: missing_og.append('og:description')
            if not og_image: missing_og.append('og:image')
            if not og_url: missing_og.append('og:url')
            
            if missing_og:
                page_issues.append(f"Missing OG tags: {', '.join(missing_og)}")
            
            # Check structured data
            structured_data = soup.find_all('script', attrs={'type': 'application/ld+json'})
            if not structured_data:
                page_issues.append("No structured data found")
            
            # Check H1 tags
            h1_tags = soup.find_all('h1')
            if len(h1_tags) == 0:
                page_issues.append("No H1 tag found")
            elif len(h1_tags) > 1:
                page_issues.append(f"Multiple H1 tags: {len(h1_tags)}")
            
            # Report results
            if page_issues:
                print(f"  ❌ Issues found:")
                for issue in page_issues:
                    print(f"    • {issue}")
                issues_found.extend([f"{name}: {issue}" for issue in page_issues])
            else:
                print(f"  ✅ No issues found")
            
        except Exception as e:
            error_msg = f"{name}: Error - {str(e)}"
            print(f"  ❌ {error_msg}")
            issues_found.append(error_msg)
        
        time.sleep(0.5)  # Be respectful to the server
        print()
    
    return issues_found

def check_technical_issues():
    """Check technical SEO issues"""
    print("🔧 Checking Technical SEO Issues...\n")
    
    base_url = 'https://rasfatul-pescarului.ro'
    technical_issues = []
    
    # Check robots.txt
    try:
        response = requests.get(f"{base_url}/robots.txt", timeout=10)
        if response.status_code == 200:
            print("✅ robots.txt accessible")
            content = response.text
            if 'Sitemap:' not in content:
                technical_issues.append("robots.txt missing sitemap declaration")
        else:
            technical_issues.append(f"robots.txt not accessible (HTTP {response.status_code})")
    except Exception as e:
        technical_issues.append(f"robots.txt error: {str(e)}")
    
    # Check sitemap.xml
    try:
        response = requests.get(f"{base_url}/sitemap.xml", timeout=10)
        if response.status_code == 200:
            print("✅ sitemap.xml accessible")
            try:
                soup = BeautifulSoup(response.content, 'xml')
                urls = soup.find_all('url')
                print(f"  📊 Contains {len(urls)} URLs")
                if len(urls) == 0:
                    technical_issues.append("sitemap.xml contains no URLs")
            except Exception:
                technical_issues.append("sitemap.xml has parsing issues")
        else:
            technical_issues.append(f"sitemap.xml not accessible (HTTP {response.status_code})")
    except Exception as e:
        technical_issues.append(f"sitemap.xml error: {str(e)}")
    
    # Check ads.txt
    try:
        response = requests.get(f"{base_url}/ads.txt", timeout=10)
        if response.status_code == 200:
            print("✅ ads.txt accessible")
            content = response.text
            if 'google.com' not in content:
                technical_issues.append("ads.txt missing Google AdSense entry")
        else:
            technical_issues.append(f"ads.txt not accessible (HTTP {response.status_code})")
    except Exception as e:
        technical_issues.append(f"ads.txt error: {str(e)}")
    
    return technical_issues

def generate_fix_report(page_issues, technical_issues):
    """Generate a comprehensive fix report"""
    print("\n" + "="*60)
    print("📋 SEARCH CONSOLE ISSUES FIX REPORT")
    print("="*60)
    
    total_issues = len(page_issues) + len(technical_issues)
    
    if total_issues == 0:
        print("🎉 No issues found! All SEO elements are properly implemented.")
        return
    
    print(f"\n📊 Total Issues Found: {total_issues}")
    
    if page_issues:
        print(f"\n🔍 Page-Level Issues ({len(page_issues)}):")
        for i, issue in enumerate(page_issues, 1):
            print(f"  {i}. {issue}")
    
    if technical_issues:
        print(f"\n🔧 Technical Issues ({len(technical_issues)}):")
        for i, issue in enumerate(technical_issues, 1):
            print(f"  {i}. {issue}")
    
    print(f"\n💡 Recommendations:")
    print("  1. Wait 5-10 minutes for deployment to complete")
    print("  2. Clear browser cache and test again")
    print("  3. Submit updated sitemap to Google Search Console")
    print("  4. Request re-indexing for updated pages")
    print("  5. Monitor Search Console for improvements over next 24-48 hours")
    
    print(f"\n🔄 Next Steps:")
    print("  • If issues persist, check server deployment status")
    print("  • Verify template inheritance is working correctly")
    print("  • Test with different browsers/devices")
    print("  • Contact hosting provider if technical issues persist")

def main():
    """Main function to run all checks"""
    print("🚀 Search Console Issues Fix Check for Răsfățul Pescarului")
    print("="*60)
    
    # Check page-level issues
    page_issues = check_live_seo_issues()
    
    # Check technical issues
    technical_issues = check_technical_issues()
    
    # Generate comprehensive report
    generate_fix_report(page_issues, technical_issues)
    
    # Return success/failure
    return len(page_issues) + len(technical_issues) == 0

if __name__ == '__main__':
    success = main()
    
    if success:
        print("\n✅ All checks passed! SEO improvements are working correctly.")
    else:
        print("\n⚠️ Issues found. Please review the report above and take corrective action.")
        print("\n🕐 Note: If you just deployed changes, wait 5-10 minutes and run this script again.")
