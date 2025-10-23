import json
import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.utils import timezone
from astral import moon, LocationInfo
from astral.sun import sun
from datetime import timedelta
from math import sin, sqrt, atan2, radians, cos
from .models import SiteSettings, County, Video, Lake
from .utils.email import send_contact_confirmation_email, send_contact_admin_email

def calculate_fishing_rating(moon_phase, date):
    base_rating = 5 - abs(moon_phase - 0.5) * 6
    month = date.month
    if 3 <= month <= 8:
        base_rating += 0.5
    elif month in [9, 10]:
        base_rating += 0.25
    return round(max(1, min(5, base_rating)), 2)

def calculate_solunar_data(date):
    location = LocationInfo('Romania', 'Romania', 'Europe/Bucharest', 45.9432, 24.9668)
    moon_phase = moon.phase(date) / 28.0
    s = sun(location.observer, date)
    solar_noon = s['noon']
    solar_midnight = datetime.datetime.combine(date, datetime.time(0, 0)) + timedelta(hours=12)
    
    try:
        moonrise = moon.moonrise(location.observer, date)
        moonset = moon.moonset(location.observer, date)
        
        moonrise_dt = None
        if moonrise:
            moonrise_dt = datetime.datetime.combine(date, moonrise.time())
        
        moonset_dt = None
        if moonset:
            moonset_dt = datetime.datetime.combine(date, moonset.time())

        if moonrise_dt:
            major_start = (moonrise_dt - timedelta(hours=1)).time()
            major_end = (moonrise_dt + timedelta(hours=1)).time()
        else:
            major_start = (solar_noon - timedelta(hours=1)).time()
            major_end = (solar_noon + timedelta(hours=1)).time()
        
        if moonset_dt:
            minor_start = (moonset_dt - timedelta(hours=1)).time()
            minor_end = (moonset_dt + timedelta(hours=1)).time()
        else:
            minor_start = (solar_midnight - timedelta(hours=1)).time()
            minor_end = (solar_midnight + timedelta(hours=1)).time()
    except Exception:
        major_start = (solar_noon - timedelta(hours=1)).time()
        major_end = (solar_noon + timedelta(hours=1)).time()
        minor_start = (solar_midnight - timedelta(hours=1)).time()
        minor_end = (solar_midnight + timedelta(hours=1)).time()
    
    rating = calculate_fishing_rating(moon_phase, date)
    
    return {
        'date': date,
        'moon_phase': moon_phase,
        'major_start': major_start,
        'major_end': major_end,
        'minor_start': minor_start,
        'minor_end': minor_end,
        'rating': rating
    }

def home(request):
    today = timezone.now().date()
    solunar_predictions = []

    for i in range(3):
        date = today + timedelta(days=i)
        prediction = calculate_solunar_data(date)
        solunar_predictions.append(prediction)

    # Get random lakes for the homepage
    random_lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities').order_by('?')[:3]

    # Get featured videos for the homepage
    featured_videos = Video.objects.filter(is_active=True, is_featured=True)[:3]

    context = {
        'solunar_predictions': solunar_predictions,
        'random_lakes': random_lakes,
        'featured_videos': featured_videos,
    }
    return render(request, 'index/index.html', context)

def fishing_locations(request):
    """View pentru lista de locații de pescuit"""
    lakes = Lake.objects.filter(is_active=True)
    counties = County.objects.prefetch_related('lakes').all()
    return render(request, 'locations/list.html', {
        'lakes': lakes,
        'counties': counties
    })

from django.db.models import Q

@require_http_methods(['GET'])
def filter_lakes(request):
    """API endpoint pentru filtrarea lacurilor"""
    lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities')

    # Apply county filter
    county_id = request.GET.get('county')
    selected_county = None
    if county_id:
        lakes = lakes.filter(county_id=county_id)
        try:
            selected_county = County.objects.get(id=county_id)
        except County.DoesNotExist:
            pass

    # Apply fish types filter
    fish_types = request.GET.getlist('fish_types[]')
    if fish_types:
        lakes = lakes.filter(fish_species__name__in=fish_types).distinct()

    # Apply price filter (using 12h price for filtering)
    max_price = request.GET.get('max_price')
    if max_price:
        lakes = lakes.filter(price_12h__lte=max_price)

    # Apply facilities filter
    facilities = request.GET.getlist('facilities[]')
    if facilities:
        lakes = lakes.filter(facilities__name__in=facilities).distinct()

    # Apply rating filter
    min_rating = request.GET.get('min_rating')
    if min_rating:
        try:
            min_rating_value = float(min_rating)
            # Filter lakes that have at least the minimum rating
            # We need to calculate average rating for each lake and filter
            from django.db.models import Avg, Q
            lakes = lakes.annotate(
                avg_rating=Avg('reviews__rating', filter=Q(reviews__is_approved=True, reviews__is_spam=False))
            ).filter(avg_rating__gte=min_rating_value)
        except (ValueError, TypeError):
            pass  # Invalid rating value, ignore filter

    # Format lake data for response
    lakes_data = []
    counties_in_results = set()

    for lake in lakes:
        counties_in_results.add(lake.county.name)
        lakes_data.append({
            'id': lake.id,
            'slug': lake.slug,
            'name': lake.name,
            'address': lake.address,
            'county': lake.county.name,
            'latitude': float(lake.latitude),
            'longitude': float(lake.longitude),
            'fish_species': [{'name': fish.name} for fish in lake.fish_species.all()],
            'facilities': [{'name': facility.name, 'icon_class': facility.icon_class} for facility in lake.facilities.all()],
            'price_12h': float(lake.price_12h),
            'price_24h': float(lake.price_24h),
            'image_url': lake.get_display_image().url if lake.get_display_image() else None,
            'average_rating': lake.average_rating,
            'total_reviews': lake.total_reviews
        })

    # Prepare response data
    response_data = {
        'lakes': lakes_data,
        'selected_county': selected_county.name if selected_county else None,
        'counties_in_results': list(counties_in_results)
    }

    return JsonResponse(response_data)

@require_http_methods(['GET'])
def debug_lakes(request):
    """Debug endpoint to check lakes data"""
    lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities')

    lakes_data = [{
        'id': lake.id,
        'slug': lake.slug,
        'name': lake.name,
        'address': lake.address,
        'county': lake.county.name,
        'latitude': float(lake.latitude),
        'longitude': float(lake.longitude),
        'fish_species': [{'name': fish.name} for fish in lake.fish_species.all()],
        'facilities': [{'name': facility.name, 'icon_class': facility.icon_class} for facility in lake.facilities.all()],
        'price_12h': float(lake.price_12h),
        'price_24h': float(lake.price_24h),
        'image_url': lake.get_display_image().url if lake.get_display_image() else '/static/images/lake-placeholder.jpg',
        'average_rating': lake.average_rating,
        'total_reviews': lake.total_reviews
    } for lake in lakes]

    return JsonResponse({
        'count': len(lakes_data),
        'lakes': lakes_data
    }, indent=2)

from .models import Lake, County

def locations_map(request):
    """View pentru harta locațiilor"""
    lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities')
    counties = County.objects.all().order_by('name')

    # Serialize lakes data for JavaScript
    lakes_data = [{
        'id': lake.id,
        'slug': lake.slug,
        'name': lake.name,
        'address': lake.address,
        'county': lake.county.name,
        'latitude': float(lake.latitude),
        'longitude': float(lake.longitude),
        'fish_species': [{'name': fish.name} for fish in lake.fish_species.all()],
        'facilities': [{'name': facility.name, 'icon_class': facility.icon_class} for facility in lake.facilities.all()],
        'price_12h': float(lake.price_12h),
        'price_24h': float(lake.price_24h),
        'image_url': lake.get_display_image().url if lake.get_display_image() else '/static/images/lake-placeholder.jpg',
        'average_rating': lake.average_rating,
        'total_reviews': lake.total_reviews
    } for lake in lakes]

    return render(request, 'locations/map.html', {
        'lakes_json': json.dumps(lakes_data),
        'lakes': lakes,
        'counties': counties
    })

def county_lakes(request, county_slug):
    """View pentru lacurile dintr-un județ"""
    county = get_object_or_404(County, slug=county_slug)
    lakes = Lake.objects.filter(county=county, is_active=True)
    return render(request, 'locations/county_lakes.html', {
        'county': county,
        'lakes': lakes
    })

@require_http_methods(['GET'])
def nearby_lakes(request):
    """API endpoint pentru lacurile din apropiere"""
    try:
        user_lat = float(request.GET.get('lat'))
        user_lng = float(request.GET.get('lng'))

        lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities')

        # Calculate distances and sort by proximity
        lakes_with_distance = []
        for lake in lakes:
            # Calculate distance using Haversine formula
            R = 6371  # Earth's radius in km
            dlat = radians(float(lake.latitude) - user_lat)
            dlon = radians(float(lake.longitude) - user_lng)
            a = sin(dlat/2)**2 + cos(radians(user_lat)) * cos(radians(float(lake.latitude))) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c

            lakes_with_distance.append({
                'id': lake.id,
                'slug': lake.slug,
                'name': lake.name,
                'address': lake.address,
                'county': lake.county.name,
                'latitude': float(lake.latitude),
                'longitude': float(lake.longitude),
                'fish_species': [{'name': fish.name} for fish in lake.fish_species.all()],
                'facilities': [{'name': facility.name, 'icon_class': facility.icon_class} for facility in lake.facilities.all()],
                'price_12h': float(lake.price_12h),
                'price_24h': float(lake.price_24h),
                'image_url': lake.get_display_image().url if lake.get_display_image() else None,
                'distance': round(distance, 1),
                'average_rating': lake.average_rating,
                'total_reviews': lake.total_reviews
            })

        # Sort by distance and limit to 6 nearest lakes
        lakes_with_distance.sort(key=lambda x: x['distance'])
        nearest_lakes = lakes_with_distance[:6]

        return JsonResponse({'lakes': nearest_lakes})
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)

def lake_detail(request, slug):
    """View pentru detaliile unui lac"""
    lake = get_object_or_404(
        Lake.objects.select_related('county').prefetch_related('photos'),
        slug=slug,
        is_active=True
    )

    # Get nearby lakes (within same county for now)
    nearby_lakes = Lake.objects.filter(
        county=lake.county,
        is_active=True
    ).exclude(id=lake.id)[:3]

    context = {
        'lake': lake,
        'nearby_lakes': nearby_lakes,
        'can_edit_lake': lake.can_edit(request.user) if request.user.is_authenticated else False
    }
    return render(request, 'locations/lake_detail.html', context)

def add_review(request, lake_id):
    """Add a review for a lake"""
    if request.method == 'POST':
        from .models import LakeReview

        lake = get_object_or_404(Lake, id=lake_id, is_active=True)

        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        try:
            review = LakeReview.objects.create(
                lake=lake,
                reviewer_name=request.POST.get('reviewer_name'),
                reviewer_email=request.POST.get('reviewer_email'),
                rating=int(request.POST.get('rating')),
                title=request.POST.get('title'),
                comment=request.POST.get('comment'),
                visit_date=request.POST.get('visit_date'),
                ip_address=ip
            )
            messages.success(request, 'Recenzia dvs. a fost trimisă cu succes! Va fi publicată după aprobare.')
        except Exception as e:
            messages.error(request, 'A apărut o eroare la trimiterea recenziei. Vă rugăm să încercați din nou.')

        return redirect('main:lake_detail', slug=lake.slug)

    return redirect('main:fishing_locations')

def tutorials(request):
    """View pentru lista de tutoriale video"""
    videos = Video.objects.filter(is_active=True).order_by('-created_at')

    # Get featured videos for sidebar
    featured_videos = Video.objects.filter(is_active=True, is_featured=True).order_by('-created_at')[:4]

    # Pagination
    paginator = Paginator(videos, 12)
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    context = {
        'videos': videos,
        'featured_videos': featured_videos,
        'categories': [],  # Add categories here if you have a Category model
    }

    return render(request, 'tutorials/list.html', context)

def video_detail(request, video_id):
    """View pentru detaliile unui tutorial video"""
    video = get_object_or_404(Video, id=video_id, is_active=True)
    
    # Get related videos
    related_videos = Video.objects.filter(
        is_active=True
    ).exclude(id=video.id).order_by('?')[:4]
    
    return render(request, 'tutorials/detail.html', {
        'video': video,
        'related_videos': related_videos
    })

def about(request):
    """View pentru pagina Despre noi"""
    return render(request, 'pages/about.html')

def contact(request):
    """View pentru pagina de contact"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Store form data in case of error
        form_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }

        # Basic validation
        if not all([name, email, subject, message]):
            messages.error(
                request,
                'Te rugăm să completezi toate câmpurile obligatorii.'
            )
            # Get contact settings for error case
            from .models import ContactSettings
            contact_settings = ContactSettings.get_settings()
            context = {
                'form_data': form_data,
                'contact_settings': contact_settings
            }
            return render(request, 'pages/contact.html', context)

        try:
            # Get client IP address
            def get_client_ip(request):
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                return ip

            # Save contact message to database
            from .models import ContactMessage
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
                ip_address=get_client_ip(request)
            )

            # Send contact emails
            send_contact_confirmation_email(email, name)
            send_contact_admin_email(name, email, subject, message)

            messages.success(
                request,
                'Mesajul tău a fost trimis cu succes! Te vom contacta în curând.'
            )
            return redirect('main:contact')
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Error processing contact form: {str(e)}')
            logger.exception('Full traceback:')

            messages.error(
                request,
                'A apărut o eroare la trimiterea mesajului. Te rugăm să încerci din nou.'
            )
            # Get contact settings for error case
            contact_settings = ContactSettings.get_settings()
            context = {
                'form_data': form_data,
                'contact_settings': contact_settings
            }
            return render(request, 'pages/contact.html', context)

    # Get contact settings
    from .models import ContactSettings
    contact_settings = ContactSettings.get_settings()

    context = {
        'contact_settings': contact_settings
    }
    return render(request, 'pages/contact.html', context)

@require_http_methods(['GET'])
def solunar_data(request):
    """API endpoint pentru date solunar"""
    today = timezone.now().date()
    predictions = []
    
    for i in range(3):
        date = today + timedelta(days=i)
        prediction = calculate_solunar_data(date)
        # Convert datetime objects to string format for JSON serialization
        predictions.append({
            'date': date.strftime('%Y-%m-%d'),
            'moon_phase': prediction['moon_phase'],
            'major_start': prediction['major_start'].strftime('%H:%M'),
            'major_end': prediction['major_end'].strftime('%H:%M'),
            'minor_start': prediction['minor_start'].strftime('%H:%M'),
            'minor_end': prediction['minor_end'].strftime('%H:%M'),
            'rating': prediction['rating']
        })
    
    return JsonResponse({'predictions': predictions})

def solunar_calendar(request):
    """View pentru calendarul solunar lunar"""
    from dateutil.relativedelta import relativedelta
    import calendar
    
    # Get year and month from query params or use current date
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    # Get all days in the selected month
    first_day = datetime.date(year, month, 1)
    last_day = first_day + relativedelta(months=1, days=-1)
    
    # Calculate solunar data for each day
    calendar_data = []
    current_date = first_day
    while current_date <= last_day:
        prediction = calculate_solunar_data(current_date)
        calendar_data.append(prediction)
        current_date += timedelta(days=1)
    
    # Romanian month names
    months = [
        'Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie',
        'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie'
    ]
    
    context = {
        'calendar_data': calendar_data,
        'current_year': year,
        'current_month': month,
        'years_range': range(timezone.now().year - 2, timezone.now().year + 3),
        'months': [(i+1, name) for i, name in enumerate(months)]
    }
    return render(request, 'solunar/calendar.html', context)

def terms(request):
    """View pentru pagina de termeni și condiții"""
    return render(request, 'pages/terms.html')

def privacy(request):
    """View function for the privacy policy page."""
    return render(request, 'pages/privacy.html')

def faq(request):
    """View function for the FAQ page."""
    return render(request, 'pages/faq.html')

def ghid_incepatori(request):
    """View function for the beginners guide page."""
    return render(request, 'pages/ghid-incepatori.html')

def test_iframe(request):
    """Test iframe page"""
    return render(request, 'test_iframe.html')


# ========================================
# BLOG VIEWS
# ========================================

def blog_home(request):
    """Homepage for blog articles"""
    from main.models import Article, ArticleCategory
    from django.core.paginator import Paginator
    from django.db import models

    # Get filter parameters
    category_slug = request.GET.get('category')

    # Base queryset - only published articles
    articles = Article.objects.filter(is_published=True).select_related('category', 'author')

    # Filter by category if specified
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(ArticleCategory, slug=category_slug, is_active=True)
        articles = articles.filter(category=selected_category)

    # Pagination
    paginator = Paginator(articles, 12)  # 12 articles per page
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)

    # Get all active categories for sidebar
    categories = ArticleCategory.objects.filter(is_active=True).annotate(
        article_count=models.Count('articles', filter=models.Q(articles__is_published=True))
    )

    # Get featured articles for sidebar
    featured_articles = Article.objects.filter(
        is_published=True,
        is_featured=True
    ).order_by('-published_date')[:5]

    context = {
        'articles': articles_page,
        'categories': categories,
        'selected_category': selected_category,
        'featured_articles': featured_articles,
        'total_articles': articles.count(),
    }

    return render(request, 'blog/article_list.html', context)


def article_detail(request, slug):
    """Detail view for a single article"""
    from main.models import Article

    article = get_object_or_404(Article, slug=slug, is_published=True)

    # Increment views count
    article.increment_views()

    # Get related articles (same category, exclude current)
    related_articles = Article.objects.filter(
        is_published=True,
        category=article.category
    ).exclude(id=article.id).order_by('-published_date')[:3]

    # Get previous article (older)
    previous_article = Article.objects.filter(
        is_published=True,
        published_date__lt=article.published_date
    ).order_by('-published_date').first()

    # Get next article (newer)
    next_article = Article.objects.filter(
        is_published=True,
        published_date__gt=article.published_date
    ).order_by('published_date').first()

    context = {
        'article': article,
        'related_articles': related_articles,
        'previous_article': previous_article,
        'next_article': next_article,
    }

    return render(request, 'blog/article_detail.html', context)


# ========================================
# FISHING DICTIONARY VIEWS
# ========================================

def fishing_dictionary(request):
    """View for fishing terms dictionary"""
    from main.models import FishingTerm
    from django.db import models

    # Get filter parameters
    category = request.GET.get('category')
    search = request.GET.get('search')
    letter = request.GET.get('letter')

    # Base queryset
    terms = FishingTerm.objects.filter(is_active=True)

    # Apply filters
    if category:
        terms = terms.filter(category=category)

    if search:
        terms = terms.filter(
            models.Q(term__icontains=search) |
            models.Q(definition__icontains=search)
        )

    if letter:
        terms = terms.filter(term__istartswith=letter)

    # Order alphabetically
    terms = terms.order_by('term')

    # Get all categories for filter
    categories = FishingTerm.CATEGORY_CHOICES

    # Get alphabet for letter navigation
    import string
    alphabet = list(string.ascii_uppercase)

    # Get first letters that have terms
    available_letters = FishingTerm.objects.filter(is_active=True).values_list(
        'term', flat=True
    )
    available_letters = sorted(set(term[0].upper() for term in available_letters if term))

    context = {
        'terms': terms,
        'categories': categories,
        'selected_category': category,
        'search_query': search,
        'selected_letter': letter,
        'alphabet': alphabet,
        'available_letters': available_letters,
        'total_terms': terms.count(),
    }

    return render(request, 'dictionary/fishing_terms.html', context)


def fishing_term_detail(request, slug):
    """Detail view for a fishing term"""
    from main.models import FishingTerm

    term = get_object_or_404(FishingTerm, slug=slug, is_active=True)

    # Get related terms
    related_terms = term.related_terms.filter(is_active=True)[:6]

    # Get terms in same category
    similar_terms = FishingTerm.objects.filter(
        is_active=True,
        category=term.category
    ).exclude(id=term.id).order_by('?')[:5]

    context = {
        'term': term,
        'related_terms': related_terms,
        'similar_terms': similar_terms,
    }

    return render(request, 'dictionary/term_detail.html', context)


# ========================================
# COUNTY GUIDE VIEWS
# ========================================

def county_guide(request, slug):
    """Detail view for county fishing guide"""
    from main.models import County, FishSpecies
    from django.db.models import Q

    # Get county that has guide content populated
    county = get_object_or_404(
        County.objects.exclude(Q(guide_content='') | Q(guide_content__isnull=True)),
        slug=slug
    )

    # Get lakes in this county
    lakes = county.lakes.filter(is_active=True).select_related('county').prefetch_related(
        'fish_species', 'facilities'
    )[:10]  # Show top 10 lakes

    # Get fish species available in this county
    fish_species = FishSpecies.objects.filter(
        lake__county=county,
        lake__is_active=True,
        is_active=True
    ).distinct()

    context = {
        'county': county,
        'lakes': lakes,
        'fish_species': fish_species,
        'total_lakes': county.get_lakes_count(),
    }

    return render(request, 'guides/county_guide.html', context)


# ========================================
# FISH SPECIES VIEWS
# ========================================

def fish_species_list(request):
    """List of all fish species"""
    from main.models import FishSpecies

    # Get filter parameters
    category = request.GET.get('category')

    # Base queryset
    species = FishSpecies.objects.filter(is_active=True)

    # Filter by category if specified
    if category:
        species = species.filter(category=category)

    # Order by category and name
    species = species.order_by('category', 'name')

    # Get categories for filter
    categories = FishSpecies.CATEGORY_CHOICES

    context = {
        'species_list': species,
        'categories': categories,
        'selected_category': category,
        'total_species': species.count(),
    }

    return render(request, 'species/fish_species_list.html', context)


def fish_species_detail(request, slug):
    """Detail view for a fish species"""
    from main.models import FishSpecies, Lake

    species = get_object_or_404(FishSpecies, slug=slug, is_active=True)

    # Get lakes where this species can be found
    lakes = Lake.objects.filter(
        fish_species=species,
        is_active=True
    ).select_related('county').prefetch_related('facilities')[:12]

    # Get related species (same category)
    related_species = FishSpecies.objects.filter(
        is_active=True,
        category=species.category
    ).exclude(id=species.id)[:6]

    context = {
        'species': species,
        'lakes': lakes,
        'related_species': related_species,
        'total_lakes': lakes.count(),
    }

    return render(request, 'species/fish_species_detail.html', context)
