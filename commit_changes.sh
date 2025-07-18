#!/bin/bash

# Commit și push modificările pentru fix-ul hărții

echo "🚀 Committing map fixes..."

# Add all changes
git add .

# Commit with descriptive message
git commit -m "🗺️ Fix map functionality and CSP for Leaflet

✅ Fixed Content Security Policy to allow Leaflet from unpkg.com
✅ Fixed hero.webp references to hero.png in map template  
✅ Added support for AdSense domains in CSP
✅ Updated middleware for complete Leaflet support

This fixes the map not loading due to CSP blocking Leaflet resources.
Map should now work correctly on both local and production."

# Push to GitHub
git push origin main

echo "✅ Changes pushed to GitHub!"
