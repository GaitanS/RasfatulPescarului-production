"""
Test script to verify Search Console fixes are working
Run this to check if canonical tags, redirects, and other fixes are properly applied
"""

import os
import sys
import django
from urllib.parse import urlparse, urljoin
import requests
from collections import defaultdict

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from django.test import RequestFactory, Client
from django.urls import reverse, get_resolver
from main.models import Lake, Article, County, FishSpecies


class SearchConsoleFixTester:
    """Test all Search Console fixes"""

    def __init__(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.issues = defaultdict(list)
        self.successes = defaultdict(list)

    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)

    def test_canonical_tags(self):
        """Test that canonical tags are present and correct"""
        self.print_header("TESTING CANONICAL TAGS")

        test_urls = [
            '/',
            '/locations/',
            '/about/',
            '/contact/',
            '/blog/',
        ]

        for url in test_urls:
            try:
                response = self.client.get(url)
                content = response.content.decode('utf-8')

                if 'rel="canonical"' in content:
                    # Extract canonical URL
                    start = content.find('rel="canonical" href="') + 22
                    end = content.find('"', start)
                    canonical = content[start:end]

                    print(f"✓ {url}")
                    print(f"  Canonical: {canonical}")

                    # Check if canonical matches expected
                    expected = f"https://rasfatul-pescarului.ro{url}"
                    if canonical == expected:
                        self.successes['canonical'].append(url)
                    else:
                        print(f"  ⚠ Expected: {expected}")
                        self.issues['canonical'].append((url, f"Mismatch: {canonical} != {expected}"))
                else:
                    print(f"✗ {url} - No canonical tag found!")
                    self.issues['canonical'].append((url, "Missing canonical tag"))

            except Exception as e:
                print(f"✗ {url} - ERROR: {str(e)}")
                self.issues['canonical'].append((url, str(e)))

        print()

    def test_append_slash(self):
        """Test that URLs without trailing slash redirect to version with slash"""
        self.print_header("TESTING APPEND_SLASH REDIRECTS")

        test_urls = [
            ('/about', '/about/'),
            ('/contact', '/contact/'),
            ('/locations', '/locations/'),
        ]

        for url_without, url_with in test_urls:
            try:
                response = self.client.get(url_without, follow=False)

                if response.status_code in [301, 302]:
                    redirect_url = response.url
                    if redirect_url == url_with:
                        print(f"✓ {url_without} → {url_with} (301)")
                        self.successes['append_slash'].append(url_without)
                    else:
                        print(f"✗ {url_without} → {redirect_url} (expected {url_with})")
                        self.issues['append_slash'].append((url_without, f"Wrong redirect: {redirect_url}"))
                else:
                    print(f"⚠ {url_without} - No redirect (status {response.status_code})")
                    # This might be OK if CommonMiddleware is doing it
                    # Test with follow=True
                    response_follow = self.client.get(url_without, follow=True)
                    if response_follow.request['PATH_INFO'] == url_with:
                        print(f"  ✓ But redirect works internally")
                        self.successes['append_slash'].append(url_without)

            except Exception as e:
                print(f"✗ {url_without} - ERROR: {str(e)}")
                self.issues['append_slash'].append((url_without, str(e)))

        print()

    def test_duplicate_content(self):
        """Check for potential duplicate content issues"""
        self.print_header("CHECKING DUPLICATE CONTENT")

        # Check lakes with similar descriptions
        print("\n1. Checking lakes for duplicate descriptions:")
        lakes = Lake.objects.filter(is_active=True).values('name', 'description', 'slug')

        descriptions_seen = {}
        duplicate_count = 0

        for lake in lakes[:20]:  # Check first 20
            desc = lake['description'][:100].strip().lower()  # First 100 chars

            if desc in descriptions_seen and desc:
                duplicate_count += 1
                print(f"  ⚠ Possible duplicate:")
                print(f"    - {lake['name']} ({lake['slug']})")
                print(f"    - {descriptions_seen[desc]['name']} ({descriptions_seen[desc]['slug']})")
                self.issues['duplicate_content'].append(
                    (lake['slug'], f"Similar to {descriptions_seen[desc]['slug']}")
                )
            else:
                descriptions_seen[desc] = lake

        if duplicate_count == 0:
            print("  ✓ No duplicate lake descriptions found (in first 20)")
            self.successes['duplicate_content'].append("lakes")
        else:
            print(f"\n  Found {duplicate_count} potential duplicates")

        # Check for pages with similar titles
        print("\n2. Checking for pages with query parameters:")
        test_urls_with_params = [
            '/locations/?page=2',
            '/locations/?county=cluj',
            '/blog/?category=tehnici',
        ]

        for url in test_urls_with_params:
            try:
                response = self.client.get(url)
                if response.status_code == 200:
                    content = response.content.decode('utf-8')

                    if 'rel="canonical"' in content:
                        start = content.find('rel="canonical" href="') + 22
                        end = content.find('"', start)
                        canonical = content[start:end]

                        # Canonical should NOT include query params for most cases
                        if '?' not in canonical:
                            print(f"  ✓ {url} - Canonical without params: {canonical}")
                            self.successes['duplicate_content'].append(url)
                        else:
                            print(f"  ⚠ {url} - Canonical HAS params: {canonical}")
                            self.issues['duplicate_content'].append(
                                (url, f"Canonical includes params: {canonical}")
                            )
            except Exception as e:
                print(f"  ✗ {url} - ERROR: {str(e)}")

        print()

    def test_500_errors(self):
        """Test critical URLs for 500 errors"""
        self.print_header("TESTING FOR 500 ERRORS")

        # Test all critical URLs
        critical_urls = [
            '/',
            '/about/',
            '/contact/',
            '/locations/',
            '/blog/',
            '/dictionar-pescuit/',
            '/specii-de-pesti/',
        ]

        print("Testing critical URLs:")
        for url in critical_urls:
            try:
                response = self.client.get(url)

                if response.status_code == 200:
                    print(f"  ✓ {url} - OK (200)")
                    self.successes['500_errors'].append(url)
                elif response.status_code == 404:
                    print(f"  ⚠ {url} - Not Found (404)")
                    self.issues['500_errors'].append((url, "404 Not Found"))
                elif 500 <= response.status_code < 600:
                    print(f"  ✗ {url} - SERVER ERROR ({response.status_code})")
                    self.issues['500_errors'].append((url, f"Server error {response.status_code}"))
                else:
                    print(f"  ⚠ {url} - Status {response.status_code}")

            except Exception as e:
                print(f"  ✗ {url} - EXCEPTION: {str(e)}")
                self.issues['500_errors'].append((url, f"Exception: {str(e)}"))

        # Test some dynamic URLs (lakes, articles if they exist)
        print("\nTesting dynamic URLs:")

        # Test first lake
        first_lake = Lake.objects.filter(is_active=True).first()
        if first_lake:
            url = f'/baltă/{first_lake.slug}/'
            try:
                response = self.client.get(url)
                if response.status_code == 200:
                    print(f"  ✓ Lake detail: {url} - OK")
                    self.successes['500_errors'].append(url)
                else:
                    print(f"  ✗ Lake detail: {url} - Status {response.status_code}")
                    self.issues['500_errors'].append((url, f"Status {response.status_code}"))
            except Exception as e:
                print(f"  ✗ Lake detail: {url} - ERROR: {str(e)}")
                self.issues['500_errors'].append((url, str(e)))

        # Test first article (if exists)
        first_article = Article.objects.filter(is_published=True).first()
        if first_article:
            url = f'/blog/{first_article.slug}/'
            try:
                response = self.client.get(url)
                if response.status_code == 200:
                    print(f"  ✓ Article detail: {url} - OK")
                    self.successes['500_errors'].append(url)
                else:
                    print(f"  ✗ Article detail: {url} - Status {response.status_code}")
                    self.issues['500_errors'].append((url, f"Status {response.status_code}"))
            except Exception as e:
                print(f"  ✗ Article detail: {url} - ERROR: {str(e)}")
                self.issues['500_errors'].append((url, str(e)))
        else:
            print("  ⚠ No articles found - run populate_content.py first")

        print()

    def test_404_handling(self):
        """Test that 404 pages work correctly"""
        self.print_header("TESTING 404 HANDLING")

        test_404_urls = [
            '/this-page-does-not-exist/',
            '/baltă/non-existent-lake/',
            '/blog/non-existent-article/',
        ]

        for url in test_404_urls:
            try:
                response = self.client.get(url)

                if response.status_code == 404:
                    print(f"✓ {url} - Correctly returns 404")

                    # Check if custom 404 template is used
                    content = response.content.decode('utf-8')
                    if 'Pagina nu a fost găsită' in content or '404' in content:
                        print(f"  ✓ Custom 404 page is rendered")
                        self.successes['404_handling'].append(url)
                    else:
                        print(f"  ⚠ Default 404 page (consider custom template)")

                else:
                    print(f"✗ {url} - Returns {response.status_code} instead of 404")
                    self.issues['404_handling'].append((url, f"Status {response.status_code}"))

            except Exception as e:
                print(f"✗ {url} - ERROR: {str(e)}")
                self.issues['404_handling'].append((url, str(e)))

        print()

    def test_redirects(self):
        """Test that redirects work correctly and aren't chained"""
        self.print_header("TESTING REDIRECTS")

        print("Testing for redirect chains:")
        print("(Max 1 redirect allowed, more = chain issue)")

        # Test some URLs that might have redirects
        test_urls = [
            '/about',  # Should redirect to /about/
            '/contact',  # Should redirect to /contact/
        ]

        for url in test_urls:
            try:
                # Don't follow redirects, count them manually
                response = self.client.get(url, follow=False)
                redirect_count = 0
                current_url = url

                while response.status_code in [301, 302, 307, 308] and redirect_count < 5:
                    redirect_count += 1
                    current_url = response.url
                    response = self.client.get(current_url, follow=False)

                if redirect_count == 0:
                    print(f"  ✓ {url} - No redirect needed (200)")
                    self.successes['redirects'].append(url)
                elif redirect_count == 1:
                    print(f"  ✓ {url} - Single redirect to {current_url}")
                    self.successes['redirects'].append(url)
                else:
                    print(f"  ✗ {url} - REDIRECT CHAIN ({redirect_count} redirects)")
                    self.issues['redirects'].append((url, f"Chain of {redirect_count} redirects"))

            except Exception as e:
                print(f"  ✗ {url} - ERROR: {str(e)}")
                self.issues['redirects'].append((url, str(e)))

        print()

    def print_summary(self):
        """Print summary of all tests"""
        self.print_header("TEST SUMMARY")

        total_tests = sum(len(v) for v in self.successes.values())
        total_issues = sum(len(v) for v in self.issues.values())

        print(f"\n✓ Successful tests: {total_tests}")
        print(f"✗ Issues found: {total_issues}")

        if total_issues > 0:
            print("\n" + "=" * 60)
            print("  ISSUES THAT NEED FIXING")
            print("=" * 60)

            for category, issue_list in self.issues.items():
                if issue_list:
                    print(f"\n{category.upper().replace('_', ' ')}:")
                    for url, issue in issue_list[:10]:  # Show first 10
                        print(f"  ✗ {url}")
                        print(f"    Issue: {issue}")

            if total_issues > 10:
                print(f"\n... and {total_issues - 10} more issues")

        else:
            print("\n🎉 ALL TESTS PASSED! Site is ready for Search Console re-indexing.")

        print("\n" + "=" * 60)

        return total_issues == 0

    def run_all_tests(self):
        """Run all tests"""
        print("\n")
        print("🔍 SEARCH CONSOLE FIX VERIFICATION")
        print("=" * 60)
        print("Testing all fixes for Google Search Console issues")
        print()

        try:
            self.test_canonical_tags()
            self.test_append_slash()
            self.test_duplicate_content()
            self.test_500_errors()
            self.test_404_handling()
            self.test_redirects()

            success = self.print_summary()

            return success

        except Exception as e:
            print(f"\n❌ FATAL ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main function"""
    tester = SearchConsoleFixTester()
    success = tester.run_all_tests()

    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED")
        print("\nNext steps:")
        print("1. Deploy these changes to production")
        print("2. Wait 3-7 days for Google to re-crawl")
        print("3. Check Search Console for improvements")
        print("4. Request manual indexing for important pages")
    else:
        print("⚠ ISSUES FOUND - Please fix them before deployment")
        print("\nReview the issues above and:")
        print("1. Fix each issue in the code")
        print("2. Run this test again")
        print("3. Deploy only after all tests pass")

    print("=" * 60)
    print()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
