#!/usr/bin/env python3
"""
Test script pentru verificarea CSP fix-ului
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_csp_headers():
    """Test CSP headers pentru Leaflet"""
    print("🔍 Testing CSP Headers for Leaflet Support")
    print("=" * 50)
    
    client = Client()
    
    # Test map page
    try:
        response = client.get('/locations/map/')
        
        print(f"📄 Map page status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Map page loads successfully")
            
            # Check CSP header
            csp_header = response.get('Content-Security-Policy', '')
            
            print(f"\n🔒 Content-Security-Policy:")
            print(f"   {csp_header}")
            
            # Check if unpkg.com is allowed
            if 'unpkg.com' in csp_header:
                print("✅ unpkg.com is allowed in CSP")
                
                # Check specific directives
                if 'script-src' in csp_header and 'unpkg.com' in csp_header:
                    print("✅ unpkg.com allowed for scripts")
                else:
                    print("❌ unpkg.com NOT allowed for scripts")
                
                if 'style-src' in csp_header and 'unpkg.com' in csp_header:
                    print("✅ unpkg.com allowed for styles")
                else:
                    print("❌ unpkg.com NOT allowed for styles")
                    
            else:
                print("❌ unpkg.com is NOT allowed in CSP")
            
            # Check if pagead2.googlesyndication.com is allowed for frames
            if 'pagead2.googlesyndication.com' in csp_header:
                print("✅ Google AdSense frames allowed")
            else:
                print("❌ Google AdSense frames NOT allowed")
                
        else:
            print(f"❌ Map page failed to load: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing map page: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Expected CSP should include:")
    print("   - script-src: https://unpkg.com")
    print("   - style-src: https://unpkg.com") 
    print("   - frame-src: https://pagead2.googlesyndication.com")
    print("   - connect-src: https://ep1.adtrafficquality.google")

if __name__ == '__main__':
    test_csp_headers()
