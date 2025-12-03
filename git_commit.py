#!/usr/bin/env python3
"""
Git commit and push script
"""
import subprocess
import os

def run_git_command(command):
    """Run git command and return result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        print(f"Command: {command}")
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Exception running {command}: {e}")
        return False

def main():
    print("🚀 Git Commit and Push")
    print("=" * 40)
    
    # Check git status
    print("📊 Checking git status...")
    run_git_command("git status --porcelain")
    
    # Add all changes
    print("\n📁 Adding all changes...")
    if run_git_command("git add ."):
        print("✅ Files added successfully")
    else:
        print("❌ Failed to add files")
        return
    
    # Commit changes
    commit_message = """🗺️ Fix map functionality and CSP for Leaflet

✅ Fixed Content Security Policy to allow Leaflet from unpkg.com
✅ Fixed hero.webp references to hero.png in map template  
✅ Added support for AdSense domains in CSP
✅ Updated middleware for complete Leaflet support
✅ Added FAQ page with 2,500+ words content
✅ Added Beginner's Guide with 3,000+ words content
✅ Extended About page with detailed company info
✅ Added structured data for SEO optimization

This fixes the map not loading due to CSP blocking Leaflet resources.
Map should now work correctly on both local and production."""
    
    print("\n💬 Committing changes...")
    if run_git_command(f'git commit -m "{commit_message}"'):
        print("✅ Commit successful")
    else:
        print("❌ Commit failed")
        return
    
    # Push to GitHub
    print("\n🚀 Pushing to GitHub...")
    if run_git_command("git push origin main"):
        print("✅ Push successful!")
        print("🎉 All changes are now on GitHub!")
    else:
        print("❌ Push failed")

if __name__ == '__main__':
    main()
