from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count
import re

class UserProfile(models.Model):
    """Extended user profile for additional information"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Utilizator"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Număr de telefon",
        help_text="Numărul dvs. de telefon pentru contact"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Orașul",
        help_text="Orașul în care locuiți"
    )
    county = models.ForeignKey(
        'County',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Județul",
        help_text="Județul în care locuiți"
    )
    bio = models.TextField(
        blank=True,
        max_length=500,
        verbose_name="Despre mine",
        help_text="Scurtă descriere despre dvs. și experiența la pescuit"
    )
    avatar = models.ImageField(
        upload_to='profiles/avatars/',
        null=True,
        blank=True,
        verbose_name="Fotografie de profil",
        help_text="Fotografia dvs. de profil (opțional)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data înregistrării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Profil utilizator"
        verbose_name_plural = "Profile utilizatori"

    def __str__(self):
        return f"Profil {self.user.username}"

    def get_full_name(self):
        """Get user's full name or username if not available"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username

class FishSpecies(models.Model):
    CATEGORY_CHOICES = [
        ('cyprinid', 'Ciprinide'),
        ('predator', 'Prădători'),
        ('other', 'Alte specii'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Numele speciei",
        help_text="Numele românesc al speciei de pește"
    )
    scientific_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Numele științific",
        help_text="Numele latin al speciei (opțional)"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name="URL slug",
        help_text="Se generează automat din nume"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name="Categoria",
        help_text="Categoria biologică a peștelui"
    )

    # Detailed information fields
    detailed_description = models.TextField(
        blank=True,
        verbose_name="Descriere detaliată",
        help_text="Descriere completă a speciei (aspect, caracteristici, comportament)"
    )
    habitat = models.TextField(
        blank=True,
        verbose_name="Habitat",
        help_text="Informații despre habitatul preferat al speciei"
    )
    fishing_techniques = models.TextField(
        blank=True,
        verbose_name="Tehnici de pescuit",
        help_text="Tehnici recomandate pentru pescuitul acestei specii"
    )
    best_baits = models.TextField(
        blank=True,
        verbose_name="Momeli recomandate",
        help_text="Cele mai eficiente momeli pentru această specie"
    )
    legal_info = models.TextField(
        blank=True,
        verbose_name="Informații legale",
        help_text="Dimensiuni minime legale, perioade de prohibiție, etc."
    )
    average_size = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Dimensiune medie",
        help_text="Dimensiunea medie a speciei (ex: 30-50 cm)"
    )
    max_size = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Dimensiune maximă",
        help_text="Dimensiunea maximă înregistrată (ex: 120 cm)"
    )
    image = models.ImageField(
        upload_to='fish_species/',
        null=True,
        blank=True,
        verbose_name="Imagine specie",
        help_text="Fotografie reprezentativă a speciei"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Activ"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Specie de pește"
        verbose_name_plural = "Specii de pești"
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get URL for fish species detail page"""
        from django.urls import reverse
        return reverse('main:fish_species_detail', kwargs={'slug': self.slug})

class Facility(models.Model):
    CATEGORY_CHOICES = [
        ('basic', 'De bază'),
        ('accommodation', 'Cazare'),
        ('food', 'Mâncare și băutură'),
        ('fishing', 'Pescuit'),
        ('services', 'Servicii'),
        ('recreation', 'Recreere'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Numele facilității"
    )
    icon_class = models.CharField(
        max_length=50,
        verbose_name="Clasa icon FontAwesome",
        help_text="Ex: fas fa-parking, fas fa-bed"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='basic',
        verbose_name="Categoria"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descriere",
        help_text="Descrierea detaliată a facilității"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activ"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Facilitate"
        verbose_name_plural = "Facilități"
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    def get_category_display_romanian(self):
        """Return Romanian category name for admin display"""
        category_map = {
            'basic': 'De bază',
            'accommodation': 'Cazare',
            'food': 'Mâncare și băutură',
            'fishing': 'Pescuit',
            'services': 'Servicii',
            'recreation': 'Recreere',
        }
        return category_map.get(self.category, self.category)

class County(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Nume județ",
        help_text="Numele complet al județului (ex: Argeș, Brașov, Cluj)"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="URL slug",
        help_text="Se generează automat din nume. Folosit pentru URL-uri (ex: arges, brasov)"
    )
    region = models.CharField(
        max_length=50,
        choices=[
            ('MOLDOVA', 'Moldova'),
            ('MUNTENIA', 'Muntenia'),
            ('OLTENIA', 'Oltenia'),
            ('BANAT', 'Banat'),
            ('CRISANA', 'Crișana'),
            ('MARAMURES', 'Maramureș'),
            ('TRANSILVANIA', 'Transilvania'),
            ('DOBROGEA', 'Dobrogea'),
            ('BUCURESTI', 'București')
        ],
        verbose_name="Regiune",
        help_text="Regiunea istorică din care face parte județului"
    )

    # County Guide Content
    guide_content = models.TextField(
        blank=True,
        verbose_name="Ghid pescuit județ",
        help_text="Ghid detaliat despre pescuitul în acest județ (acceptă HTML)"
    )
    guide_title = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Titlu ghid",
        help_text="Titlul ghidului de pescuit pentru județ (ex: Ghid Complet Pescuit în Cluj)"
    )
    guide_excerpt = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Rezumat ghid",
        help_text="Rezumat scurt al ghidului pentru județ"
    )
    has_guide = models.BooleanField(
        default=False,
        verbose_name="Are ghid",
        help_text="Bifează dacă există un ghid de pescuit pentru acest județ"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Județ"
        verbose_name_plural = "Județe"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_guide_url(self):
        """Get URL for county guide"""
        from django.urls import reverse
        if self.has_guide:
            return reverse('main:county_guide', kwargs={'slug': self.slug})
        return None

    def get_lakes_count(self):
        """Get count of active lakes in this county"""
        return self.lakes.filter(is_active=True).count()

class SiteSettings(models.Model):
    site_name = models.CharField(
        max_length=100,
        default='Răsfățul Pescarului',
        verbose_name="Numele site-ului",
        help_text="Numele principal al site-ului care apare în titlu și logo"
    )
    contact_email = models.EmailField(
        default='contact@rasfatulpescarului.ro',
        verbose_name="Email de contact",
        help_text="Adresa de email principală pentru contact (ex: contact@site.ro)"
    )
    phone = models.CharField(
        max_length=20,
        default='0700000000',
        verbose_name="Număr de telefon",
        help_text="Numărul de telefon pentru contact (ex: 0700 123 456)"
    )
    address = models.TextField(
        default='România',
        verbose_name="Adresa",
        help_text="Adresa completă a companiei"
    )
    facebook_url = models.URLField(
        blank=True,
        verbose_name="Link Facebook",
        help_text="URL-ul complet către pagina de Facebook (ex: https://facebook.com/pagina)"
    )
    instagram_url = models.URLField(
        blank=True,
        verbose_name="Link Instagram",
        help_text="URL-ul complet către pagina de Instagram"
    )
    youtube_url = models.URLField(
        blank=True,
        verbose_name="Link YouTube",
        help_text="URL-ul complet către canalul de YouTube"
    )
    about_text = models.TextField(
        default='Despre noi',
        verbose_name="Text despre noi",
        help_text="Descrierea scurtă a companiei care apare în footer"
    )

    class Meta:
        verbose_name = 'Setări Site'
        verbose_name_plural = 'Setări Site'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        return cls.objects.first()

class FooterSettings(models.Model):
    contact_info = models.CharField(
        max_length=200,
        default='Contact',
        verbose_name="Informații contact",
        help_text="Titlul secțiunii de contact din footer"
    )
    address = models.TextField(
        default='Strada Exemplu, Nr. 123, București',
        verbose_name="Adresa completă",
        help_text="Adresa fizică completă care apare în footer"
    )
    phone = models.CharField(
        max_length=20,
        default='+40 123 456 789',
        verbose_name="Telefon",
        help_text="Numărul de telefon cu prefixul țării (ex: +40 123 456 789)"
    )
    email = models.EmailField(
        default='contact@rasfatulpescarului.ro',
        verbose_name="Email",
        help_text="Adresa de email care apare în footer"
    )
    working_hours = models.CharField(
        max_length=100,
        default='Luni - Vineri: 09:00 - 18:00',
        verbose_name="Program de lucru",
        help_text="Programul de lucru (ex: Luni - Vineri: 09:00 - 18:00)"
    )

    class Meta:
        verbose_name = 'Setări Footer'
        verbose_name_plural = 'Setări Footer'

    def __str__(self):
        return 'Footer Settings'

    @classmethod
    def get_settings(cls):
        return cls.objects.first()

class Lake(models.Model):
    LAKE_TYPE_CHOICES = [
        ('private', 'Baltă privată'),
        ('public', 'Baltă publică'),
        ('competition', 'Baltă pentru competiții'),
        ('catch_release', 'Baltă cu regim "catch & release"'),
        ('mixed', 'Baltă cu regim mixt (reținere + catch & release)'),
        ('natural', 'Baltă naturală'),
    ]

    # Owner relationship
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_lakes',
        verbose_name="Proprietar",
        help_text="Utilizatorul care a creat și gestionează această baltă"
    )

    name = models.CharField(
        max_length=200,
        verbose_name="Numele bălții*",
        help_text="Numele complet al lacului sau bălții de pescuit"
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name="URL slug",
        help_text="URL-ul prietenos pentru lac (se generează automat din nume)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descriere",
        help_text="Descrierea detaliată a lacului, facilităților și condițiilor de pescuit"
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Localitate, județ*",
        help_text="Adresa completă a lacului (ex: Comuna X, Județul Y)"
    )
    county = models.ForeignKey(
        County,
        on_delete=models.CASCADE,
        related_name='lakes',
        verbose_name="Județul*",
        help_text="Județul în care se află lacul"
    )
    latitude = models.DecimalField(
        max_digits=18,
        decimal_places=15,
        verbose_name="Latitudine",
        help_text="Coordonata latitudine cu precizie mare (ex: 45.39189813235069). Folosește Google Maps pentru a găsi coordonatele"
    )
    longitude = models.DecimalField(
        max_digits=18,
        decimal_places=15,
        verbose_name="Longitudine",
        help_text="Coordonata longitudine cu precizie mare (ex: 24.62707585690222). Folosește Google Maps pentru a găsi coordonatele"
    )
    google_maps_embed = models.TextField(
        blank=True,
        null=True,
        verbose_name="Cod embed Google Maps",
        help_text="Cod iframe complet de la Google Maps (opțional). Dacă este completat, va fi folosit în locul coordonatelor. Exemplu: <iframe src='...' width='600' height='450'></iframe>"
    )
    lake_type = models.CharField(
        max_length=50,
        choices=LAKE_TYPE_CHOICES,
        default='private',
        verbose_name="Tipul bălții",
        help_text="Selectează tipul de baltă în funcție de administrare și regulament"
    )
    fish_species = models.ManyToManyField(
        FishSpecies,
        verbose_name="Specii de pești*",
        help_text="Selectează speciile de pești disponibile în acest lac"
    )
    facilities = models.ManyToManyField(
        Facility,
        verbose_name="Facilități*",
        help_text="Selectează facilitățile disponibile la acest lac"
    )
    price_12h = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preț pescuit 12h*",
        help_text="Prețul pentru 12 ore de pescuit în lei românești (ex: 30.00)"
    )
    price_24h = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preț pescuit 24h*",
        help_text="Prețul pentru 24 ore de pescuit în lei românești (ex: 50.00)"
    )

    # Backward compatibility property
    @property
    def price_per_day(self):
        """Backward compatibility - returns 24h price"""
        return self.price_24h
    rules = models.TextField(
        verbose_name="Regulament*",
        help_text="Regulile și restricțiile pentru pescuitul pe acest lac (ex: Permis obligatoriu, Se permite pescuitul din barcă, Program: 06:00-22:00)"
    )
    image = models.ImageField(
        upload_to='lakes/',
        null=True,
        blank=True,
        verbose_name="Imagine",
        help_text="Imaginea principală a lacului (format recomandat: JPG, PNG, max 2MB)"
    )

    # Contact information (required fields)
    contact_phone = models.CharField(
        max_length=20,
        verbose_name="Telefon*",
        help_text="Numărul de telefon pentru contact (ex: 0700 123 456)"
    )
    contact_email = models.EmailField(
        verbose_name="Email*",
        help_text="Adresa de email pentru contact"
    )

    # Optional fields
    number_of_stands = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Număr de standuri",
        help_text="Numărul total de standuri de pescuit disponibile"
    )
    surface_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Suprafață (ha)",
        help_text="Suprafața lacului în hectare (ex: 2.5)"
    )
    depth_min = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Adâncime minimă (m)",
        help_text="Adâncimea minimă a lacului în metri"
    )
    depth_max = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Adâncime maximă (m)",
        help_text="Adâncimea maximă a lacului în metri"
    )
    depth_average = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Adâncime medie (m)",
        help_text="Adâncimea medie a lacului în metri"
    )
    length_min = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Lungime minimă (m)",
        help_text="Lungimea minimă a lacului în metri"
    )
    length_max = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Lungime maximă (m)",
        help_text="Lungimea maximă a lacului în metri"
    )
    width_min = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Lățime minimă (m)",
        help_text="Lățimea minimă a lacului în metri"
    )
    width_max = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Lățime maximă (m)",
        help_text="Lățimea maximă a lacului în metri"
    )
    website = models.URLField(
        blank=True,
        verbose_name="Site web",
        help_text="Site-ul web oficial al bălții (opțional)"
    )
    facebook_url = models.URLField(
        blank=True,
        verbose_name="Facebook",
        help_text="Pagina de Facebook a bălții (opțional)"
    )
    instagram_url = models.URLField(
        blank=True,
        verbose_name="Instagram",
        help_text="Pagina de Instagram a bălții (opțional)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Activ",
        help_text="Bifează pentru a afișa lacul pe site. Debifează pentru a-l ascunde temporar"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Lac de pescuit"
        verbose_name_plural = "Lacuri de pescuit"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from name, handling Romanian characters
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Lake.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('main:balta_detail', kwargs={'slug': self.slug})

    def get_last_updated_display(self):
        """Get formatted last update date in Romanian"""
        months = {
            1: 'Ianuarie', 2: 'Februarie', 3: 'Martie', 4: 'Aprilie',
            5: 'Mai', 6: 'Iunie', 7: 'Iulie', 8: 'August',
            9: 'Septembrie', 10: 'Octombrie', 11: 'Noiembrie', 12: 'Decembrie'
        }
        return f"{self.updated_at.day} {months[self.updated_at.month]} {self.updated_at.year}"

    def can_edit(self, user):
        """Check if user can edit this lake"""
        return user.is_authenticated and (user == self.owner or user.is_staff)

    def get_safe_google_maps_embed(self):
        """Return sanitized Google Maps embed code or None if invalid"""
        if not self.google_maps_embed:
            return None

        # Basic sanitization - only allow iframe tags with Google Maps domains
        embed_code = self.google_maps_embed.strip()

        # Check if it contains iframe and Google Maps domain
        if ('<iframe' in embed_code.lower() and
            ('maps.google.com' in embed_code or 'google.com/maps' in embed_code)):

            # Remove any script tags or other potentially dangerous elements
            embed_code = re.sub(r'<script[^>]*>.*?</script>', '', embed_code, flags=re.IGNORECASE | re.DOTALL)
            embed_code = re.sub(r'<link[^>]*>', '', embed_code, flags=re.IGNORECASE)
            embed_code = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', '', embed_code, flags=re.IGNORECASE)

            return mark_safe(embed_code)

        return None

    @property
    def average_rating(self):
        """Calculate average rating from approved reviews"""
        reviews = self.reviews.filter(is_approved=True, is_spam=False)
        if reviews.exists():
            return round(reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'], 2)
        return 0

    @property
    def total_reviews(self):
        """Count approved reviews"""
        return self.reviews.filter(is_approved=True, is_spam=False).count()

    @property
    def rating_distribution(self):
        """Return rating distribution for approved reviews"""
        reviews = self.reviews.filter(is_approved=True, is_spam=False)
        distribution = {i: 0 for i in range(1, 6)}
        for review in reviews:
            distribution[review.rating] += 1
        return distribution

    def get_main_photo(self):
        """Get the main photo from gallery, fallback to legacy image field"""
        # First try to get main photo from gallery
        main_photo = self.photos.filter(is_main=True).first()
        if main_photo:
            return main_photo.image

        # Then try to get first photo from gallery
        first_photo = self.photos.first()
        if first_photo:
            return first_photo.image

        # Finally fallback to legacy image field
        return self.image

    def get_gallery_photos(self):
        """Get all gallery photos ordered by order field"""
        return self.photos.all().order_by('order', 'created_at')

    def has_gallery(self):
        """Check if lake has any gallery photos"""
        return self.photos.exists()

    def get_display_image(self):
        """Get the best available image for display (for backward compatibility)"""
        main_photo = self.get_main_photo()
        return main_photo if main_photo else None

class LakePhoto(models.Model):
    """Model for storing multiple photos for each lake"""

    lake = models.ForeignKey(
        Lake,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name="Lac"
    )
    image = models.ImageField(
        upload_to='lakes/gallery/',
        verbose_name="Imagine",
        help_text="Imaginea pentru galeria lacului (format recomandat: JPG, PNG, max 2MB)"
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Titlu imagine",
        help_text="Titlu descriptiv pentru imagine (generat automat)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descriere imagine",
        help_text="Descriere detaliată a imaginii (generat automat)"
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Imagine principală",
        help_text="Bifează pentru a seta această imagine ca principală în galerie"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordine",
        help_text="Ordinea de afișare în galerie (generat automat)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Fotografie lac"
        verbose_name_plural = "Fotografii lac"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.lake.name} - Foto {self.order + 1}"

    def clean(self):
        """Validate that a lake doesn't have more than 10 photos"""
        if self.lake_id:
            existing_photos = LakePhoto.objects.filter(lake=self.lake)
            if self.pk:
                existing_photos = existing_photos.exclude(pk=self.pk)

            if existing_photos.count() >= 10:
                raise ValidationError("Un lac poate avea maximum 10 fotografii în galerie.")

    def save(self, *args, **kwargs):
        # If this is set as main photo, unset other main photos for this lake
        if self.is_main:
            LakePhoto.objects.filter(lake=self.lake, is_main=True).update(is_main=False)

        # Auto-assign order if this is a new photo
        if not self.pk:
            last_photo = LakePhoto.objects.filter(lake=self.lake).order_by('-order').first()
            if last_photo:
                self.order = last_photo.order + 1
            else:
                self.order = 0

        super().save(*args, **kwargs)

class Video(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Titlul videoclipului",
        help_text="Titlul descriptiv al videoclipului (ex: Pescuit la crap pe lacul X)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descriere",
        help_text="Descrierea detaliată a videoclipului și conținutului acestuia"
    )
    url = models.URLField(
        verbose_name="Link video",
        help_text="URL-ul complet către videoclip (YouTube, Vimeo, etc.) - ex: https://youtube.com/watch?v=..."
    )
    thumbnail = models.ImageField(
        upload_to='videos/thumbnails/',
        blank=True,
        null=True,
        verbose_name="Imagine de previzualizare",
        help_text="Imaginea care apare înainte de redarea videoclipului (opțional, se poate genera automat)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activ",
        help_text="Bifează pentru a afișa videoclipul pe site"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Video recomandat",
        help_text="Bifează pentru a afișa videoclipul în secțiunea de recomandări"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Videoclip'
        verbose_name_plural = 'Videoclipuri'

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        """Convert video URL to embeddable format"""
        if not self.url:
            return ''

        # Handle YouTube URLs
        if 'youtube.com/watch' in self.url:
            # Extract video ID from URL like https://youtube.com/watch?v=VIDEO_ID
            import re
            match = re.search(r'[?&]v=([^&]+)', self.url)
            if match:
                video_id = match.group(1)
                return f'https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1'
        elif 'youtu.be/' in self.url:
            # Handle short YouTube URLs like https://youtu.be/VIDEO_ID
            video_id = self.url.split('youtu.be/')[-1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1'
        elif 'vimeo.com/' in self.url:
            # Handle Vimeo URLs
            video_id = self.url.split('vimeo.com/')[-1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'

        # Return original URL if no conversion needed
        return self.url

    def get_youtube_video_id(self):
        """Extract YouTube video ID from URL"""
        if not self.url:
            return None

        import re
        # Handle YouTube URLs
        if 'youtube.com/watch' in self.url:
            match = re.search(r'[?&]v=([^&]+)', self.url)
            if match:
                return match.group(1)
        elif 'youtu.be/' in self.url:
            return self.url.split('youtu.be/')[-1].split('?')[0]

        return None

    @property
    def youtube_thumbnail_url(self):
        """Get YouTube thumbnail URL"""
        video_id = self.get_youtube_video_id()
        if video_id:
            # Use maxresdefault for best quality, fallback to hqdefault if not available
            return f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
        return None

    def get_thumbnail_url(self):
        """Get thumbnail URL - either uploaded thumbnail or YouTube auto-generated"""
        if self.thumbnail:
            return self.thumbnail.url
        return self.youtube_thumbnail_url

class HeroSection(models.Model):
    main_button_text = models.CharField(
        max_length=100,
        default='Alătură-te grupului',
        verbose_name="Textul butonului principal",
        help_text="Textul care apare pe butonul principal din secțiunea hero (ex: Alătură-te grupului)"
    )
    main_button_url = models.URLField(
        default='https://www.facebook.com/rasfatulpescarului',
        verbose_name="Link buton principal",
        help_text="URL-ul către care duce butonul principal (ex: pagina de Facebook)"
    )
    facebook_url = models.URLField(
        default='https://www.facebook.com/rasfatulpescarului',
        verbose_name="Link Facebook",
        help_text="URL-ul complet către pagina de Facebook"
    )
    tiktok_url = models.URLField(
        default='https://www.tiktok.com/@rasfatulpescarului',
        verbose_name="Link TikTok",
        help_text="URL-ul complet către contul de TikTok"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = 'Secțiune Hero'
        verbose_name_plural = 'Secțiune Hero'

    def __str__(self):
        return 'Hero Section Settings'

    @classmethod
    def get_settings(cls):
        return cls.objects.first()

class OperatingHours(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Luni'),
        ('tuesday', 'Marți'),
        ('wednesday', 'Miercuri'),
        ('thursday', 'Joi'),
        ('friday', 'Vineri'),
        ('saturday', 'Sâmbătă'),
        ('sunday', 'Duminică'),
    ]

    lake = models.OneToOneField(
        Lake,
        on_delete=models.CASCADE,
        related_name='operating_hours',
        verbose_name="Lac"
    )

    # Monday
    monday_is_open = models.BooleanField(default=True, verbose_name="Deschis Luni")
    monday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    monday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    monday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    monday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Tuesday
    tuesday_is_open = models.BooleanField(default=True, verbose_name="Deschis Marți")
    tuesday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    tuesday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    tuesday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    tuesday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Wednesday
    wednesday_is_open = models.BooleanField(default=True, verbose_name="Deschis Miercuri")
    wednesday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    wednesday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    wednesday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    wednesday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Thursday
    thursday_is_open = models.BooleanField(default=True, verbose_name="Deschis Joi")
    thursday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    thursday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    thursday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    thursday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Friday
    friday_is_open = models.BooleanField(default=True, verbose_name="Deschis Vineri")
    friday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    friday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    friday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    friday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Saturday
    saturday_is_open = models.BooleanField(default=True, verbose_name="Deschis Sâmbătă")
    saturday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    saturday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    saturday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    saturday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    # Sunday
    sunday_is_open = models.BooleanField(default=True, verbose_name="Deschis Duminică")
    sunday_opening_time = models.TimeField(null=True, blank=True, verbose_name="Ora deschidere")
    sunday_closing_time = models.TimeField(null=True, blank=True, verbose_name="Ora închidere")
    sunday_is_24h = models.BooleanField(default=False, verbose_name="24 ore")
    sunday_special_notes = models.CharField(max_length=200, blank=True, verbose_name="Note speciale")

    general_notes = models.TextField(
        blank=True,
        verbose_name="Note generale",
        help_text="Informații generale despre program"
    )

    class Meta:
        verbose_name = "Program de funcționare"
        verbose_name_plural = "Programe de funcționare"

    def __str__(self):
        return f"Program {self.lake.name}"

class LakeReview(models.Model):
    RATING_CHOICES = [
        (1, '1 stea'),
        (2, '2 stele'),
        (3, '3 stele'),
        (4, '4 stele'),
        (5, '5 stele'),
    ]

    lake = models.ForeignKey(
        Lake,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Lac"
    )
    reviewer_name = models.CharField(
        max_length=100,
        verbose_name="Numele recenzentului",
        help_text="Numele dvs. complet"
    )
    reviewer_email = models.EmailField(
        verbose_name="Email",
        help_text="Pentru verificare (nu va fi afișat public)"
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Titlul recenziei",
        help_text="Titlu scurt pentru experiența dvs."
    )
    comment = models.TextField(
        max_length=1000,
        validators=[MinLengthValidator(20)],
        verbose_name="Comentariu",
        help_text="Descrieți experiența dvs. la acest lac (minim 20 caractere)"
    )
    visit_date = models.DateField(
        verbose_name="Data vizitei",
        help_text="Când ați vizitat lacul"
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name="Aprobat"
    )
    is_spam = models.BooleanField(
        default=False,
        verbose_name="Spam"
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="Adresa IP"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Recenzie lac"
        verbose_name_plural = "Recenzii lacuri"
        ordering = ['-created_at']
        unique_together = ['lake', 'reviewer_email']  # One review per email per lake

    def __str__(self):
        return f"{self.reviewer_name} - {self.lake.name} ({self.rating} stele)"


class ContactMessage(models.Model):
    """Model pentru stocarea mesajelor de contact"""
    name = models.CharField(
        max_length=100,
        verbose_name="Nume complet",
        help_text="Numele complet al persoanei care trimite mesajul"
    )
    email = models.EmailField(
        verbose_name="Email",
        help_text="Adresa de email pentru răspuns"
    )
    subject = models.CharField(
        max_length=200,
        verbose_name="Subiect",
        help_text="Subiectul mesajului"
    )
    message = models.TextField(
        verbose_name="Mesaj",
        help_text="Conținutul mesajului"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Adresa IP",
        help_text="Adresa IP de la care a fost trimis mesajul"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data trimiterii"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Citit",
        help_text="Marchează dacă mesajul a fost citit"
    )
    is_replied = models.BooleanField(
        default=False,
        verbose_name="Răspuns trimis",
        help_text="Marchează dacă s-a trimis un răspuns"
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name="Note administrative",
        help_text="Note interne pentru administratori"
    )

    class Meta:
        verbose_name = "Mesaj de contact"
        verbose_name_plural = "Mesaje de contact"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%d.%m.%Y %H:%M')})"

    def get_short_message(self):
        """Returnează o versiune scurtă a mesajului pentru afișare în admin"""
        if len(self.message) > 100:
            return self.message[:100] + "..."
        return self.message
    get_short_message.short_description = "Mesaj (scurt)"


class ContactSettings(models.Model):
    """Model pentru gestionarea setărilor de contact și programului de lucru"""

    # Contact Information
    company_name = models.CharField(
        max_length=100,
        default='Răsfățul Pescarului',
        verbose_name="Numele companiei",
        help_text="Numele companiei care apare pe pagina de contact"
    )
    address = models.TextField(
        default='Strada Exemplu, Nr. 123, București, România',
        verbose_name="Adresa completă",
        help_text="Adresa fizică completă a companiei"
    )
    phone = models.CharField(
        max_length=20,
        default='+40 700 000 000',
        verbose_name="Număr de telefon",
        help_text="Numărul principal de telefon pentru contact"
    )
    email = models.EmailField(
        default='contact@rasfatulpescarului.ro',
        verbose_name="Email de contact",
        help_text="Adresa principală de email pentru contact"
    )

    # Working Hours
    monday_friday_hours = models.CharField(
        max_length=50,
        default='09:00 – 18:00',
        verbose_name="Program Luni - Vineri",
        help_text="Programul de lucru pentru zilele de luni până vineri (ex: 09:00 – 18:00)"
    )
    saturday_hours = models.CharField(
        max_length=50,
        default='10:00 – 14:00',
        verbose_name="Program Sâmbătă",
        help_text="Programul de lucru pentru sâmbătă (ex: 10:00 – 14:00)"
    )
    sunday_hours = models.CharField(
        max_length=50,
        default='Închis',
        verbose_name="Program Duminică",
        help_text="Programul de lucru pentru duminică (ex: Închis sau 10:00 – 16:00)"
    )

    # Additional Information
    description = models.TextField(
        blank=True,
        verbose_name="Descriere",
        help_text="Descriere suplimentară care apare pe pagina de contact"
    )
    map_embed_code = models.TextField(
        blank=True,
        verbose_name="Cod embed hartă",
        help_text="Codul iframe pentru harta Google Maps (opțional)"
    )

    # Social Media
    facebook_url = models.URLField(
        blank=True,
        verbose_name="Link Facebook",
        help_text="URL-ul către pagina de Facebook"
    )
    instagram_url = models.URLField(
        blank=True,
        verbose_name="Link Instagram",
        help_text="URL-ul către pagina de Instagram"
    )
    youtube_url = models.URLField(
        blank=True,
        verbose_name="Link YouTube",
        help_text="URL-ul către canalul de YouTube"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    class Meta:
        verbose_name = "Setări Contact"
        verbose_name_plural = "Setări Contact"

    def __str__(self):
        return f"Setări Contact - {self.company_name}"

    @classmethod
    def get_settings(cls):
        """Returnează prima instanță de setări contact sau o creează dacă nu există"""
        settings = cls.objects.first()
        if not settings:
            settings = cls.objects.create()
        return settings


# ========================================
# BLOG & EDITORIAL CONTENT MODELS
# ========================================

class ArticleCategory(models.Model):
    """Categories for blog articles"""
    name = models.CharField(
        max_length=100,
        verbose_name="Numele categoriei",
        help_text="Numele categoriei de articole (ex: Tehnici de Pescuit, Echipamente)"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="URL slug",
        help_text="Se generează automat din nume"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descriere",
        help_text="Descrierea categoriei"
    )
    icon_class = models.CharField(
        max_length=50,
        default='fas fa-fish',
        verbose_name="Clasa icon FontAwesome",
        help_text="Ex: fas fa-fish, fas fa-water"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordine",
        help_text="Ordinea de afișare (număr mai mic = mai sus)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activ"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categorie articol"
        verbose_name_plural = "Categorii articole"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_articles_count(self):
        """Get count of published articles in this category"""
        return self.articles.filter(is_published=True).count()


class Article(models.Model):
    """Blog articles for editorial content"""
    title = models.CharField(
        max_length=250,
        verbose_name="Titlu articol",
        help_text="Titlul complet al articolului"
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name="URL slug",
        help_text="Se generează automat din titlu"
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles',
        verbose_name="Categorie",
        help_text="Categoria din care face parte articolul"
    )
    excerpt = models.TextField(
        max_length=500,
        verbose_name="Rezumat",
        help_text="Rezumat scurt al articolului (max 500 caractere)"
    )
    content = models.TextField(
        verbose_name="Conținut",
        help_text="Conținutul complet al articolului (acceptă HTML)"
    )
    featured_image = models.ImageField(
        upload_to='articles/',
        null=True,
        blank=True,
        verbose_name="Imagine principală",
        help_text="Imaginea principală a articolului"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles',
        verbose_name="Autor",
        help_text="Autorul articolului"
    )
    author_name = models.CharField(
        max_length=100,
        default='Echipa Răsfățul Pescarului',
        verbose_name="Nume autor afișat",
        help_text="Numele care apare ca autor pe articol"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Publicat",
        help_text="Bifează pentru a publica articolul"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Recomandat",
        help_text="Articol recomandat (apare în secțiuni speciale)"
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Vizualizări",
        help_text="Numărul de vizualizări al articolului"
    )
    reading_time = models.PositiveIntegerField(
        default=5,
        verbose_name="Timp de citire (minute)",
        help_text="Timpul estimat de citire în minute"
    )
    published_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data publicării",
        help_text="Data și ora când articolul a fost publicat"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creării")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data actualizării")

    # SEO fields
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Meta descriere SEO",
        help_text="Descriere pentru motoarele de căutare (max 160 caractere)"
    )
    meta_keywords = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Meta keywords SEO",
        help_text="Cuvinte cheie separate prin virgulă"
    )

    class Meta:
        verbose_name = "Articol"
        verbose_name_plural = "Articole"
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Auto-set published_date when first published
        if self.is_published and not self.published_date:
            from django.utils import timezone
            self.published_date = timezone.now()

        # Calculate reading time if not set (average 200 words per minute)
        if not self.reading_time or self.reading_time == 5:
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / 200))

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('main:article_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        """Increment article views count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class FishingTerm(models.Model):
    """Dictionary of fishing terms"""
    CATEGORY_CHOICES = [
        ('equipment', 'Echipamente'),
        ('techniques', 'Tehnici'),
        ('species', 'Specii'),
        ('regulations', 'Regulamente'),
        ('general', 'Termeni Generali'),
    ]

    term = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Termen",
        help_text="Termenul pescăresc (ex: Feeder, Boilies, Catch & Release)"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL slug"
    )
    definition = models.TextField(
        verbose_name="Definiție",
        help_text="Definiția completă a termenului"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general',
        verbose_name="Categorie"
    )
    related_terms = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=True,
        verbose_name="Termeni relevanți",
        help_text="Alți termeni legați de acesta"
    )
    example_usage = models.TextField(
        blank=True,
        verbose_name="Exemplu de utilizare",
        help_text="Exemplu de utilizare a termenului în context"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activ"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Termen pescăresc"
        verbose_name_plural = "Termeni pescărești"
        ordering = ['term']

    def __str__(self):
        return self.term

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.term)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('main:fishing_term_detail', kwargs={'slug': self.slug})
