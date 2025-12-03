#!/bin/bash

# Quick Deployment Script for Hostinger
# Run this on your Hostinger server via SSH

echo "🚀 Starting deployment to Hostinger..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration - Update these paths for your setup
PROJECT_DIR="/home/u123456789/domains/rasfatul-pescarului.ro/public_html"
VENV_DIR="/home/u123456789/virtualenv/rasfatul-pescarului.ro"

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Changing to project directory..."
    cd $PROJECT_DIR
fi

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    print_error "Project directory not found: $PROJECT_DIR"
    exit 1
fi

# Step 1: Pull latest changes from GitHub
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

if [ $? -eq 0 ]; then
    print_success "Git pull completed"
else
    print_error "Git pull failed"
    exit 1
fi

# Step 2: Activate virtual environment
echo "🐍 Activating virtual environment..."
if [ -f "$VENV_DIR/bin/activate" ]; then
    source $VENV_DIR/bin/activate
    print_success "Virtual environment activated"
else
    print_warning "Virtual environment not found, continuing without it"
fi

# Step 3: Install/update dependencies (if requirements changed)
if git diff HEAD~1 HEAD --name-only | grep -q "requirements.txt"; then
    echo "📦 Installing updated dependencies..."
    pip install -r requirements.txt
    print_success "Dependencies updated"
fi

# Step 4: Run migrations (if any)
echo "🗄️  Checking for database migrations..."
python manage.py migrate --check
if [ $? -ne 0 ]; then
    echo "Running database migrations..."
    python manage.py migrate
    print_success "Migrations completed"
else
    print_success "No migrations needed"
fi

# Step 5: Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

if [ $? -eq 0 ]; then
    print_success "Static files collected"
else
    print_error "Static files collection failed"
fi

# Step 6: Clear cache (if using cache)
echo "🧹 Clearing cache..."
python manage.py shell -c "from django.core.cache import cache; cache.clear()" 2>/dev/null
print_success "Cache cleared"

# Step 7: Restart application
echo "🔄 Restarting application..."
if [ -f "tmp/restart.txt" ]; then
    touch tmp/restart.txt
    print_success "Application restarted (Passenger)"
else
    mkdir -p tmp
    touch tmp/restart.txt
    print_success "Restart file created"
fi

# Step 8: Run basic checks
echo "🔍 Running system checks..."
python manage.py check --deploy

if [ $? -eq 0 ]; then
    print_success "All system checks passed"
else
    print_warning "Some system checks failed, but deployment continued"
fi

# Step 9: Test if website is accessible
echo "🌐 Testing website accessibility..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://rasfatul-pescarului.ro)

if [ "$HTTP_STATUS" = "200" ]; then
    print_success "Website is accessible (HTTP $HTTP_STATUS)"
else
    print_warning "Website returned HTTP $HTTP_STATUS"
fi

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "📋 Summary:"
echo "  • Code updated from GitHub"
echo "  • Static files collected"
echo "  • Application restarted"
echo "  • System checks completed"
echo ""
echo "🔗 Next steps:"
echo "  • Visit https://rasfatul-pescarului.ro to verify"
echo "  • Check that WebP images are loading"
echo "  • Test SEO improvements"
echo "  • Monitor performance in Google Search Console"
echo ""
echo "🆘 If issues occur:"
echo "  • Check logs: tail -f /tmp/django.log"
echo "  • Verify file permissions: ls -la static/"
echo "  • Test individual pages manually"
