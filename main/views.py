import json
import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
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
from .models import Profile, SiteSettings, County, Video
from .utils.tokens import account_activation_token, password_reset_token
from .utils.email import (
    send_verification_email, send_password_reset_email,
    send_contact_confirmation_email, send_contact_admin_email
)

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
        
        if moonrise:
            moonrise_dt = datetime.datetime.combine(date, moonrise.time())
            major_start = (moonrise_dt - timedelta(hours=1)).time()
            major_end = (moonrise_dt + timedelta(hours=1)).time()
        else:
            major_start = (solar_noon - timedelta(hours=1)).time()
            major_end = (solar_noon + timedelta(hours=1)).time()
        
        if moonset:
            moonset_dt = datetime.datetime.combine(date, moonset.time())
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
    
    context = {
        'solunar_predictions': solunar_predictions
    }
    return render(request, 'index/index.html', context)



def product_detail(request, slug):
    """View pentru detaliile unui produs"""
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand')
        .prefetch_related(
            'attribute_values',
            'attribute_values__attribute',
            'reviews'
        ),
        slug=slug,
        is_active=True
    )
    
    # Get related products
    related_products = Product.objects.filter(
        Q(category=product.category) | Q(brand=product.brand),
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'shop/detail.html', context)

def cart(request):
    """View pentru coșul de cumpărături"""
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = Decimal('0.00')
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            total = product.price * Decimal(str(quantity))
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price,
                'total': total
            })
            cart_total += total
        except Product.DoesNotExist:
            pass
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'shipping_cost': Decimal('0.00'),  # Add your shipping logic
        'total_with_shipping': cart_total  # Add shipping cost if needed
    }
    return render(request, 'shop/cart.html', context)

@require_http_methods(['POST'])
@csrf_exempt
def add_to_cart(request):
    """Adaugă un produs în coș"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            product_id = str(data.get('product_id'))
            quantity = int(data.get('quantity', 1))
        else:
            product_id = str(request.POST.get('product_id'))
            quantity = int(request.POST.get('quantity', 1))
        
        # Validate product exists
        try:
            product = Product.objects.get(id=int(product_id), is_active=True)
        except (Product.DoesNotExist, ValueError):
            if request.content_type == 'application/json':
                return JsonResponse({'status': 'error', 'message': 'Produs invalid'}, status=400)
            else:
                messages.error(request, 'Produs invalid.')
                return redirect('main:cart')
        
        if not request.session.get('cart'):
            request.session['cart'] = {}
        
        cart = request.session['cart']
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
        
        request.session.modified = True
        
        if request.content_type == 'application/json':
            return JsonResponse({'status': 'success'})
        else:
            messages.success(request, 'Produs adăugat în coș cu succes!')
            return redirect('main:cart')
            
    except (json.JSONDecodeError, ValueError, TypeError):
        if request.content_type == 'application/json':
            return JsonResponse({'status': 'error', 'message': 'Date invalide'}, status=400)
        else:
            messages.error(request, 'Eroare la adăugarea produsului în coș.')
            return redirect('main:cart')

@require_http_methods(['POST'])
@csrf_exempt
def update_cart(request):
    """Actualizează cantitatea unui produs din coș"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            product_id = str(data.get('product_id'))
            quantity = int(data.get('quantity', 0))
        else:
            product_id = str(request.POST.get('product_id'))
            quantity = int(request.POST.get('quantity', 0))
        
        # Validate product exists
        try:
            product = Product.objects.get(id=int(product_id), is_active=True)
        except (Product.DoesNotExist, ValueError):
            if request.content_type == 'application/json':
                return JsonResponse({'status': 'error', 'message': 'Produs invalid'}, status=400)
            else:
                messages.error(request, 'Produs invalid.')
                return redirect('main:cart')
        
        if request.session.get('cart') and product_id in request.session['cart']:
            if quantity > 0:
                request.session['cart'][product_id] = quantity
            else:
                del request.session['cart'][product_id]
            request.session.modified = True
        
        if request.content_type == 'application/json':
            return JsonResponse({'status': 'success'})
        else:
            messages.success(request, 'Coș actualizat cu succes!')
            return redirect('main:cart')
            
    except (json.JSONDecodeError, ValueError, TypeError):
        if request.content_type == 'application/json':
            return JsonResponse({'status': 'error', 'message': 'Date invalide'}, status=400)
        else:
            messages.error(request, 'Eroare la actualizarea coșului.')
            return redirect('main:cart')

@require_http_methods(['POST'])
@csrf_exempt
def remove_from_cart(request):
    """Șterge un produs din coș"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            product_id = str(data.get('product_id'))
        else:
            product_id = str(request.POST.get('product_id'))
        
        # Validate product exists
        try:
            product = Product.objects.get(id=int(product_id), is_active=True)
        except (Product.DoesNotExist, ValueError):
            if request.content_type == 'application/json':
                return JsonResponse({'status': 'error', 'message': 'Produs invalid'}, status=400)
            else:
                messages.error(request, 'Produs invalid.')
                return redirect('main:cart')
        
        if request.session.get('cart') and product_id in request.session['cart']:
            del request.session['cart'][product_id]
            request.session.modified = True
        
        if request.content_type == 'application/json':
            return JsonResponse({'status': 'success'})
        else:
            messages.success(request, 'Produs șters din coș cu succes!')
            return redirect('main:cart')
            
    except (json.JSONDecodeError, ValueError, TypeError):
        if request.content_type == 'application/json':
            return JsonResponse({'status': 'error', 'message': 'Date invalide'}, status=400)
        else:
            messages.error(request, 'Eroare la ștergerea produsului din coș.')
            return redirect('main:cart')

def cart_count(request):
    """Returnează numărul de produse din coș"""
    cart = request.session.get('cart', {})
    count = sum(cart.values())
    return JsonResponse({'count': count})

def cart_total(request):
    """Calculează totalul coșului"""
    cart = request.session.get('cart', {})
    total = Decimal('0.00')
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            total += product.price * Decimal(str(quantity))
        except Product.DoesNotExist:
            pass
    
    return JsonResponse({'total': str(total)})

@login_required
def checkout(request):
    """View pentru procesul de checkout"""
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Coșul tău este gol.')
        return redirect('main:cart')
    
    # Calculate cart total
    total = Decimal('0.00')
    items = []
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            total += product.price * Decimal(str(quantity))
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * Decimal(str(quantity))
            })
        except Product.DoesNotExist:
            pass
    
    if request.method == 'POST':
        # Validate form data
        if all([
            request.POST.get('first_name'),
            request.POST.get('last_name'),
            request.POST.get('email'),
            request.POST.get('phone'),
            request.POST.get('address'),
            request.POST.get('city'),
            request.POST.get('county'),
            request.POST.get('postal_code'),
            request.POST.get('terms')
        ]):
            try:
                # Create Stripe checkout session
                stripe.api_key = settings.STRIPE_SECRET_KEY
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'ron',
                            'unit_amount': int(total * 100),  # Stripe uses cents
                            'product_data': {
                                'name': 'Comandă Răsfățul Pescarului',
                            },
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('main:checkout_success')),
                    cancel_url=request.build_absolute_uri(reverse('main:checkout')),
                    customer_email=request.POST.get('email'),
                    metadata={
                        'user_id': request.user.id,
                        'shipping_address': f"{request.POST.get('address')}, {request.POST.get('city')}, {request.POST.get('postal_code')}",
                        'phone': request.POST.get('phone')
                    }
                )
                return redirect(checkout_session.url)
            except Exception as e:
                messages.error(request, 'Eroare la procesarea plății. Te rugăm să încerci din nou.')
        else:
            messages.error(request, 'Te rugăm să completezi toate câmpurile obligatorii.')
    
    context = {
        'items': items,
        'total': total,
        'counties': County.objects.all().order_by('name')
    }
    return render(request, 'shop/checkout.html', context)

@login_required
def checkout_success(request):
    """View pentru pagina de succes după checkout"""
    # Clear the cart after successful checkout
    if 'cart' in request.session:
        del request.session['cart']
    return render(request, 'shop/checkout_success.html')

@csrf_exempt
def stripe_webhook(request):
    """Handler pentru webhook-urile Stripe"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        fulfill_order(session)
    
    return HttpResponse(status=200)

@login_required
def retry_payment(request, order_id):
    """View pentru reîncercarea plății unui order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.error(request, 'Această comandă nu poate fi replătită.')
        return redirect('main:order_detail', order_id=order.id)
    
    # Create new payment session
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'ron',
                    'unit_amount': int(order.total * 100),
                    'product_data': {
                        'name': f'Order #{order.id}',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('main:checkout_success')
            ),
            cancel_url=request.build_absolute_uri(
                reverse('main:order_detail', args=[order.id])
            ),
            metadata={
                'order_id': order.id
            }
        )
        return redirect(checkout_session.url)
    except Exception as e:
        messages.error(request, 'A apărut o eroare la procesarea plății.')
        return redirect('main:order_detail', order_id=order.id)

@login_required
def payment_status(request, order_id):
    """View pentru verificarea statusului plății"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return JsonResponse({
        'status': order.status,
        'paid': order.is_paid
    })

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
    lakes = Lake.objects.filter(is_active=True)
    
    # Apply county filter
    county_id = request.GET.get('county')
    if county_id:
        lakes = lakes.filter(county_id=county_id)
    
    # Apply fish types filter
    fish_types = request.GET.getlist('fish_types[]')
    if fish_types:
        q_objects = Q()
        for fish in fish_types:
            q_objects |= Q(fish_types__icontains=fish)
        lakes = lakes.filter(q_objects)
    
    # Apply price filter
    max_price = request.GET.get('max_price')
    if max_price:
        lakes = lakes.filter(price_per_day__lte=max_price)
    
    # Apply facilities filter
    facilities = request.GET.getlist('facilities[]')
    if facilities:
        q_objects = Q()
        for facility in facilities:
            q_objects |= Q(facilities__icontains=facility)
        lakes = lakes.filter(q_objects)
    
    # Format lake data for response
    lakes_data = [{
        'id': lake.id,
        'name': lake.name,
        'address': lake.address,
        'county': lake.county.name,
        'latitude': float(lake.latitude),
        'longitude': float(lake.longitude),
        'fish_types': lake.fish_types,
        'facilities': lake.facilities.split(),
        'price_per_day': float(lake.price_per_day),
        'image_url': lake.image.url if lake.image else None
    } for lake in lakes]
    
    return JsonResponse({'lakes': lakes_data})

from .models import Lake, County

def locations_map(request):
    """View pentru harta locațiilor"""
    lakes = Lake.objects.filter(is_active=True).select_related('county')
    counties = County.objects.all().order_by('name')
    
    # Serialize lakes data for JavaScript
    lakes_data = [{
        'id': lake.id,
        'name': lake.name,
        'address': lake.address,
        'county': lake.county.name,
        'latitude': float(lake.latitude),
        'longitude': float(lake.longitude),
        'fish_types': lake.fish_types,
        'facilities': lake.facilities.split(),
        'price_per_day': float(lake.price_per_day),
        'image_url': lake.image.url if lake.image else '/static/images/lake-placeholder.jpg'
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
        
        lakes = Lake.objects.filter(is_active=True).select_related('county')
        
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
                'name': lake.name,
                'address': lake.address,
                'county': lake.county.name,
                'latitude': float(lake.latitude),
                'longitude': float(lake.longitude),
                'fish_types': lake.fish_types,
                'facilities': lake.facilities.split(),
                'price_per_day': float(lake.price_per_day),
                'image_url': lake.image.url if lake.image else None,
                'distance': round(distance, 1)
            })
        
        # Sort by distance and limit to 6 nearest lakes
        lakes_with_distance.sort(key=lambda x: x['distance'])
        nearest_lakes = lakes_with_distance[:6]
        
        return JsonResponse({'lakes': nearest_lakes})
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)

def lake_detail(request, lake_id):
    """View pentru detaliile unui lac"""
    lake = get_object_or_404(Lake.objects.select_related('county'), id=lake_id, is_active=True)
    
    # Get nearby lakes (within same county for now)
    nearby_lakes = Lake.objects.filter(
        county=lake.county,
        is_active=True
    ).exclude(id=lake.id)[:3]
    
    context = {
        'lake': lake,
        'nearby_lakes': nearby_lakes
    }
    return render(request, 'locations/lake_detail.html', context)

def tutorials(request):
    """View pentru lista de tutoriale video"""
    videos = Video.objects.filter(is_active=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(videos, 12)
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    
    return render(request, 'tutorials/list.html', {'videos': videos})

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

def login_view(request):
    """View pentru autentificare"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # First check if user exists and is active
            user = User.objects.get(email=email)
            if not user.is_active:
                messages.error(request, 'Contul nu este activat. Verificați email-ul pentru link-ul de activare.')
                return render(request, 'account/login.html')
            
            # Then try to authenticate with both username and email
            user = authenticate(request, username=user.username, password=password)
            if user is None:
                user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'main:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Email sau parolă incorectă.')
        except User.DoesNotExist:
            messages.error(request, 'Email sau parolă incorectă.')
    
    return render(request, 'account/login.html')

def register(request):
    """View pentru înregistrare"""
    # Get all counties ordered by name
    counties = County.objects.all().order_by('name')
    context = {
        'counties': counties,
        'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY
    }
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        county_id = request.POST.get('county')
        terms = request.POST.get('terms')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        
        # Store form data for repopulating the form
        form_data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'county': county_id
        }
        context['form_data'] = form_data
        
        # Validare câmpuri obligatorii
        if not all([email, password, confirm_password, first_name, last_name]):
            messages.error(request, 'Toate câmpurile marcate cu * sunt obligatorii.')
            return render(request, 'account/register.html', context)
        
        # Validare termeni și condiții
        if not terms:
            messages.error(request, 'Trebuie să acceptați termenii și condițiile.')
            return render(request, 'account/register.html', context)
        
        # Validare reCAPTCHA
        if not recaptcha_response:
            messages.error(request, 'Vă rugăm să confirmați că nu sunteți robot.')
            return render(request, 'account/register.html', context)
        
        # Validare email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Există deja un cont cu acest email.')
            return render(request, 'account/register.html', context)
        
        # Validare parole
        if password != confirm_password:
            messages.error(request, 'Parolele nu coincid.')
            return render(request, 'account/register.html', context)
        
        if len(password) < 8:
            messages.error(request, 'Parola trebuie să aibă minim 8 caractere.')
            return render(request, 'account/register.html', context)
        
        # Validare nume și prenume
        if len(first_name) < 2 or len(last_name) < 2:
            messages.error(request, 'Numele și prenumele trebuie să aibă minim 2 caractere.')
            return render(request, 'account/register.html', context)
        
        # Validare telefon (opțional)
        if phone and not phone.isdigit():
            messages.error(request, 'Numărul de telefon trebuie să conțină doar cifre.')
            return render(request, 'account/register.html', context)
        
        # Validare județ (opțional)
        if county_id:
            try:
                county = County.objects.get(id=county_id)
            except County.DoesNotExist:
                messages.error(request, 'Județul selectat nu există.')
                return render(request, 'account/register.html', context)
        
        try:
            # Creare utilizator
            username = email.split('@')[0]  # Use part before @ as username
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.save()
            
            # Actualizare profil
            profile = user.profile
            profile.phone = phone
            if county_id:
                profile.county_id = county_id
            profile.save()
            
            # Trimitere email de verificare
            try:
                send_verification_email(request, user)
            except Exception as e:
                messages.warning(
                    request,
                    'Contul a fost creat, dar a apărut o eroare la trimiterea emailului de verificare. '
                    'Te rugăm să contactezi suportul.'
                )
                return redirect('main:login')
            
            messages.success(
                request,
                'Cont creat cu succes! Verifică email-ul pentru activare.'
            )
            return redirect('main:login')
            
        except Exception as e:
            # Ștergem utilizatorul dacă a fost creat
            if 'user' in locals():
                user.delete()
            
            if 'IntegrityError' in str(e):
                messages.error(request, 'Există deja un cont cu acest email.')
            else:
                messages.error(request, f'Eroare la crearea contului: {str(e)}')
            return render(request, 'account/register.html', context)
    
    return render(request, 'account/register.html', context)

def verify_email(request, uidb64, token):
    """View pentru verificarea email-ului"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email verificat cu succes! Te poți autentifica.')
    else:
        messages.error(request, 'Link de verificare invalid.')
    
    return redirect('main:login')

def password_reset(request):
    """View pentru resetarea parolei"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Send password reset email
            send_password_reset_email(request, user)
            messages.success(
                request,
                'Email trimis cu instrucțiuni de resetare a parolei.'
            )
            return redirect('main:login')
        except User.DoesNotExist:
            messages.error(request, 'Nu există cont cu acest email.')
    
    return render(request, 'account/password_reset.html')

def password_reset_confirm(request, uidb64, token):
    """View pentru confirmarea resetării parolei"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and password_reset_token.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 != password2:
                messages.error(request, 'Parolele nu coincid.')
            else:
                user.set_password(password1)
                user.save()
                messages.success(
                    request,
                    'Parola a fost resetată cu succes! Te poți autentifica.'
                )
                return redirect('main:login')
        
        return render(request, 'account/password_reset_confirm.html')
    else:
        messages.error(request, 'Link de resetare invalid.')
        return redirect('main:login')

@login_required
def logout_view(request):
    """View pentru delogare"""
    logout(request)
    return redirect('main:home')

@login_required
def profile(request):
    """View pentru profilul utilizatorului"""
    return render(request, 'account/profile.html')

@login_required
def edit_profile(request):
    """View pentru editarea profilului"""
    counties = County.objects.all().order_by('name')
    
    if request.method == 'POST':
        try:
            # Update user fields
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.email = request.POST.get('email')
            request.user.save()
            
            # Update profile fields
            profile = request.user.profile
            profile.phone = request.POST.get('phone')
            profile.city = request.POST.get('city')
            profile.address = request.POST.get('address')
            profile.postal_code = request.POST.get('postal_code')
            profile.county_id = request.POST.get('county')
            profile.newsletter = request.POST.get('newsletter') == 'on'
            profile.order_updates = request.POST.get('order_updates') == 'on'
            
            # Handle avatar upload
            if request.FILES.get('avatar'):
                profile.avatar = request.FILES['avatar']
            
            profile.save()
            
            messages.success(request, 'Profil actualizat cu succes!')
            return redirect('main:profile')
        except Exception as e:
            messages.error(request, f'Eroare la actualizarea profilului: {str(e)}')
    
    return render(request, 'account/edit_profile.html', {'counties': counties})

@login_required
def change_password(request):
    """View pentru schimbarea parolei"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not request.user.check_password(old_password):
            messages.error(request, 'Parola veche este incorectă.')
        elif password1 != password2:
            messages.error(request, 'Parolele noi nu coincid.')
        else:
            request.user.set_password(password1)
            request.user.save()
            messages.success(request, 'Parola a fost schimbată cu succes!')
            return redirect('main:login')
    
    return render(request, 'account/change_password.html')

@login_required
def orders(request):
    """View pentru lista comenzilor utilizatorului"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'account/orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """View pentru detaliile unei comenzi"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'account/order_detail.html', {'order': order})

@login_required
def order_cancel(request, order_id):
    """View pentru anularea unei comenzi"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.error(request, 'Această comandă nu poate fi anulată.')
        return redirect('main:order_detail', order_id=order.id)
    
    order.status = 'cancelled'
    order.save()
    
    # Send cancellation emails
    send_order_cancelled_email(request, order)
    send_order_cancelled_admin_email(order)
    
    messages.success(request, 'Comanda a fost anulată cu succes.')
    return render(request, 'account/order_cancel_confirmation.html', {
        'order': order
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
            return render(request, 'pages/contact.html', {'form_data': form_data})
        
        try:
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
            logger.error(f'Error sending contact form emails: {str(e)}')
            logger.exception('Full traceback:')
            
            messages.error(
                request,
                'A apărut o eroare la trimiterea mesajului. Te rugăm să încerci din nou.'
            )
            return render(request, 'pages/contact.html', {'form_data': form_data})
    
    return render(request, 'pages/contact.html')

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
