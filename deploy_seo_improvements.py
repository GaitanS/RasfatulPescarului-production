#!/usr/bin/env python
"""
Deploy SEO Improvements to Production
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip()}")
        return False

def check_git_status():
    """Check git status"""
    print("📊 Checking git status...")
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.stdout.strip():
            print("📝 Changes detected:")
            print(result.stdout)
            return True
        else:
            print("✅ No changes detected")
            return False
    except Exception as e:
        print(f"❌ Error checking git status: {e}")
        return False

def deploy_seo_improvements():
    """Deploy SEO improvements"""
    print("🚀 Deploying SEO Improvements to Răsfățul Pescarului\n")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: Not in Django project directory")
        return False
    
    # Check git status
    has_changes = check_git_status()
    
    if not has_changes:
        print("ℹ️ No changes to deploy")
        return True
    
    # Run Django checks
    if not run_command('python manage.py check', 'Running Django checks'):
        return False
    
    # Test migrations
    if not run_command('python manage.py makemigrations --dry-run', 'Checking for new migrations'):
        return False
    
    # Collect static files
    if not run_command('python manage.py collectstatic --noinput', 'Collecting static files'):
        return False
    
    # Compress static files
    if not run_command('python manage.py compress --force', 'Compressing static files'):
        return False
    
    # Add changes to git
    if not run_command('git add .', 'Adding changes to git'):
        return False
    
    # Commit changes
    commit_message = "SEO improvements: meta tags, structured data, breadcrumbs, sitemap enhancements"
    if not run_command(f'git commit -m "{commit_message}"', 'Committing changes'):
        return False
    
    # Push to remote
    print("\n🚨 Ready to push to production!")
    print("This will deploy the following SEO improvements:")
    print("  • Enhanced meta tags (title, description, keywords)")
    print("  • Open Graph and Twitter Card tags")
    print("  • Structured data (JSON-LD)")
    print("  • Breadcrumb navigation")
    print("  • Improved sitemap with priorities")
    print("  • Custom 404/500 error pages")
    print("  • SEO middleware for automatic optimization")
    print("  • Enhanced robots.txt")
    print("  • Security headers")
    
    response = input("\n❓ Do you want to push to production? (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        if not run_command('git push origin main', 'Pushing to production'):
            return False
        
        print("\n🎉 SEO improvements deployed successfully!")
        print("\n📋 Next steps:")
        print("  1. Wait for deployment to complete on Hostinger")
        print("  2. Test the live site with: python test_live_seo.py")
        print("  3. Submit updated sitemap to Google Search Console")
        print("  4. Monitor Search Console for improvements")
        print("  5. Check Core Web Vitals after deployment")
        
        return True
    else:
        print("❌ Deployment cancelled by user")
        return False

def create_deployment_checklist():
    """Create a deployment checklist"""
    checklist = """
# SEO Deployment Checklist

## Pre-deployment
- [ ] Run `python manage.py check`
- [ ] Test locally with `python test_seo_simple.py`
- [ ] Review all changes in git
- [ ] Backup production database

## Deployment
- [ ] Push changes to production
- [ ] Wait for deployment completion
- [ ] Test live site with `python test_live_seo.py`

## Post-deployment
- [ ] Submit updated sitemap to Google Search Console
- [ ] Test all major pages for SEO elements
- [ ] Check mobile usability
- [ ] Monitor Core Web Vitals
- [ ] Verify structured data with Google's Rich Results Test
- [ ] Check robots.txt and ads.txt accessibility

## Monitoring (first week)
- [ ] Monitor search rankings
- [ ] Check for crawl errors in Search Console
- [ ] Review page speed insights
- [ ] Monitor organic traffic changes
- [ ] Check for any broken links

## Long-term (monthly)
- [ ] Review Search Console performance
- [ ] Update meta descriptions based on CTR
- [ ] Add new structured data as needed
- [ ] Optimize underperforming pages
"""
    
    with open('seo_deployment_checklist.md', 'w', encoding='utf-8') as f:
        f.write(checklist)
    
    print("📋 Created deployment checklist: seo_deployment_checklist.md")

if __name__ == '__main__':
    success = deploy_seo_improvements()
    
    if success:
        create_deployment_checklist()
        print("\n✨ All SEO improvements are ready for production!")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
        sys.exit(1)
