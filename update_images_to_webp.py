#!/usr/bin/env python
"""
Update Images to WebP Format for Răsfățul Pescarului
This script helps verify and optimize the WebP image implementation
"""

import os
import glob
from pathlib import Path

def check_webp_images():
    """Check if WebP images exist in static/images directory"""
    print("🖼️ Checking WebP Images Implementation\n")
    
    static_images_dir = Path("static/images")
    
    # Expected WebP images
    expected_webp_images = [
        "hero.webp",
        "img_4.webp", 
        "lake-placeholder.webp"
    ]
    
    print("📋 Expected WebP Images:")
    for image in expected_webp_images:
        image_path = static_images_dir / image
        if image_path.exists():
            size = image_path.stat().st_size
            print(f"  ✅ {image} - {size:,} bytes")
        else:
            print(f"  ❌ {image} - NOT FOUND")
    
    print()

def check_template_updates():
    """Check if templates have been updated to use WebP images"""
    print("📄 Checking Template Updates\n")
    
    # Files that should reference WebP images
    template_files = [
        "templates/index/index.html",
        "templates/pages/about.html", 
        "templates/locations/list.html",
        "templates/locations/map.html",
        "templates/locations/county_lakes.html",
        "templates/lakes/my_lakes.html"
    ]
    
    webp_references = {
        "hero.webp": 0,
        "img_4.webp": 0,
        "lake-placeholder.webp": 0
    }
    
    old_references = {
        "hero.png": 0,
        "img_4.png": 0,
        "lake-placeholder.jpg": 0
    }
    
    for template_file in template_files:
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Count WebP references
                for webp_image in webp_references:
                    webp_references[webp_image] += content.count(webp_image)
                
                # Count old format references
                for old_image in old_references:
                    old_references[old_image] += content.count(old_image)
    
    print("✅ WebP References Found:")
    for image, count in webp_references.items():
        print(f"  {image}: {count} references")
    
    print("\n❌ Old Format References (should be 0):")
    for image, count in old_references.items():
        print(f"  {image}: {count} references")
    
    total_old = sum(old_references.values())
    if total_old == 0:
        print("\n🎉 All templates successfully updated to WebP!")
    else:
        print(f"\n⚠️ Found {total_old} old format references that need updating")
    
    print()

def check_css_optimization():
    """Check CSS files for image references"""
    print("🎨 Checking CSS Files\n")
    
    css_files = glob.glob("static/css/*.css") + glob.glob("templates/**/*.html", recursive=True)
    
    css_issues = []
    
    for css_file in css_files:
        if os.path.exists(css_file):
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Check for old image references in CSS
                    old_images = ["hero.png", "img_4.png", "lake-placeholder.jpg"]
                    for old_image in old_images:
                        if old_image in content:
                            css_issues.append(f"{css_file}: references {old_image}")
            except:
                continue
    
    if css_issues:
        print("⚠️ CSS Issues Found:")
        for issue in css_issues:
            print(f"  {issue}")
    else:
        print("✅ No CSS issues found")
    
    print()

def generate_performance_report():
    """Generate performance improvement report"""
    print("📊 Performance Improvement Report\n")
    
    # Estimate file size improvements (typical WebP savings)
    improvements = {
        "hero.webp": {"old_format": "PNG", "estimated_savings": "60-80%"},
        "img_4.webp": {"old_format": "PNG", "estimated_savings": "60-80%"},
        "lake-placeholder.webp": {"old_format": "JPG", "estimated_savings": "25-35%"}
    }
    
    print("🚀 Expected Performance Improvements:")
    for image, info in improvements.items():
        print(f"  {image}:")
        print(f"    • Format: {info['old_format']} → WebP")
        print(f"    • Size reduction: {info['estimated_savings']}")
        print(f"    • Faster loading: ✅")
        print(f"    • Better compression: ✅")
        print()
    
    print("📈 SEO Benefits:")
    print("  • Faster page load times")
    print("  • Better Core Web Vitals scores")
    print("  • Improved mobile performance")
    print("  • Reduced bandwidth usage")
    print("  • Better user experience")
    print()

def check_browser_support():
    """Check WebP browser support implementation"""
    print("🌐 Browser Support Check\n")
    
    # Check if there are fallback mechanisms
    template_files = glob.glob("templates/**/*.html", recursive=True)
    
    has_picture_tags = False
    has_webp_detection = False
    
    for template_file in template_files:
        if os.path.exists(template_file):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    if '<picture>' in content:
                        has_picture_tags = True
                    
                    if 'webp' in content.lower() and 'support' in content.lower():
                        has_webp_detection = True
            except:
                continue
    
    print("🔍 Browser Compatibility:")
    print(f"  Picture tags for fallback: {'✅' if has_picture_tags else '❌'}")
    print(f"  WebP detection script: {'✅' if has_webp_detection else '❌'}")
    print()
    
    print("📱 WebP Support:")
    print("  • Chrome: ✅ (since 2010)")
    print("  • Firefox: ✅ (since 2019)")
    print("  • Safari: ✅ (since 2020)")
    print("  • Edge: ✅ (since 2018)")
    print("  • Mobile browsers: ✅ (95%+ support)")
    print()

def main():
    """Main function to run all checks"""
    print("🚀 WebP Image Implementation Check for Răsfățul Pescarului")
    print("=" * 60)
    print()
    
    # Run all checks
    check_webp_images()
    check_template_updates()
    check_css_optimization()
    generate_performance_report()
    check_browser_support()
    
    print("🎯 Next Steps:")
    print("  1. Ensure all WebP images are uploaded to static/images/")
    print("  2. Run: python manage.py collectstatic")
    print("  3. Test website loading speed")
    print("  4. Monitor Core Web Vitals in Google Search Console")
    print("  5. Consider implementing lazy loading for better performance")
    print()
    
    print("✅ WebP Implementation Check Complete!")

if __name__ == '__main__':
    main()
