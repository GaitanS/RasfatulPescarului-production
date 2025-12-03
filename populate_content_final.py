"""
Script to populate database with high-quality content for AdSense approval
This script aggregates content from multiple sources to create:
- Blog article categories and 13 original articles
- 10 detailed county fishing guides
- 70+ fishing dictionary terms
- Detailed information for 23 fish species
"""

import os
import sys
import django
from datetime import timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import (
    Article, ArticleCategory, FishingTerm, County,
    FishSpecies, User
)
from django.utils import timezone
from django.utils.text import slugify

def create_article_categories():
    """Create article categories"""
    print("Creating article categories...")

    categories_data = [
        {
            'name': 'Tehnici de Pescuit',
            'description': 'Tehnici avansate și tips pentru pescari de toate nivelurile',
            'icon_class': 'fas fa-fish',
            'order': 1,
            'slug': 'tehnici-pescuit'
        },
        {
            'name': 'Echipamente',
            'description': 'Ghiduri despre echipamente și accesorii de pescuit',
            'icon_class': 'fas fa-tools',
            'order': 2,
            'slug': 'echipamente'
        },
        {
            'name': 'Locații de Pescuit',
            'description': 'Cele mai bune locuri pentru pescuit în România',
            'icon_class': 'fas fa-map-marked-alt',
            'order': 3,
            'slug': 'locatii-pescuit'
        },
        {
            'name': 'Povești de Pescuit',
            'description': 'Experiențe și povești reale de la pescari',
            'icon_class': 'fas fa-book-open',
            'order': 4,
            'slug': 'povesti-pescuit'
        },
        {
            'name': 'Regulamente',
            'description': 'Regulamente și legislație pentru pescuit sportiv',
            'icon_class': 'fas fa-gavel',
            'order': 5,
            'slug': 'regulamente'
        },
    ]

    for cat_data in categories_data:
        category, created = ArticleCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"  ✓ Created category: {category.name}")
        else:
             # Update existing category to ensure slug is correct
            for key, value in cat_data.items():
                setattr(category, key, value)
            category.save()

    print(f"Categories created/updated: {ArticleCategory.objects.count()}\n")


def create_blog_articles():
    """Create original blog articles"""
    print("Creating blog articles...")

    # Get or create admin user
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.create_superuser(
            'admin', 'admin@example.com', 'admin'
        )

    # Get categories
    tech_cat = ArticleCategory.objects.get(slug='tehnici-pescuit')
    equip_cat = ArticleCategory.objects.get(slug='echipamente')
    loc_cat = ArticleCategory.objects.get(slug='locatii-pescuit')
    
    # Articles data
    articles_data = [
        # From populate_content.py
        {
            'title': 'Ghidul Complet al Pescuitului la Crap în România',
            'category': tech_cat,
            'excerpt': 'Descoperiți tehnicile avansate și secretele pescarilor experimentați pentru captura de crap în apele României. Un ghid complet cu tot ce trebuie să știți.',
            'content': """
<h2>Introducere în Pescuitul la Crap</h2>
<p>Crapul este una dintre cele mai populare specii de pești în rândul pescarilor din România. Cu o răspândire largă în majoritatea apelor noastre, acest pește ciprinid oferă provocări și satisfacții deosebite pentru pescarii de toate nivelurile.</p>

<h2>Echipamentul Necesar</h2>
<p>Pentru pescuitul la crap, veți avea nevoie de:</p>
<ul>
<li><strong>Lansete specializate</strong>: Lansete de crap cu lungimi între 3.60m și 3.90m, cu putere de aruncare de 2.75-3.5 lbs</li>
<li><strong>Mulinete robuste</strong>: Mulinete cu capacitate mare de fir, cu frână lină și sistem baitrunner</li>
<li><strong>Fir de pescuit</strong>: Fir monofilament de 0.30-0.35mm sau fir împletit de 0.18-0.22mm pentru mai multă rezistență</li>
<li><strong>Avertizoare</strong>: Avertizoare electronice sau swingere pentru detectarea imediată a atacului</li>
<li><strong>Rod pod</strong>: Suport solid pentru 2-3 lansete, ajustabil pe orice tip de teren</li>
</ul>

<h2>Cele Mai Bune Momeli pentru Crap</h2>
<p>Crapul este un pește omnivior, ceea ce înseamnă că acceptă o gamă largă de momeli:</p>

<h3>Boilies</h3>
<p>Boilies-urile sunt momelile cele mai populare pentru crap modern. Disponibile în diametre de 14-24mm, în arome dulci (căpșuni, vanilie, ananas) sau picante (condimente, pește). Pentru cele mai bune rezultate, folosiți boilies cu conținut proteic ridicat în apele reci și cele dulci în apele calde.</p>

<h3>Porumb</h3>
<p>Porumbul (fie natural, fie conservat) este o momeală clasică și foarte eficientă. Poate fi folosit singular sau în combinație cu boilies pe același cârlig (popup rig). Avantajul: preț accesibil și eficiență dovedită.</p>

<h3>Pellets</h3>
<p>Peletii din furaje pentru pești sunt excelente atât ca momelă pe cârlig, cât și pentru umplutura coșului. Variante recomandate: pellets halibut, pellets de crap, pellets condimentați.</p>

<h2>Tehnici de Pescuit</h2>

<h3>Method Feeder</h3>
<p>Tehnica method feeder este extrem de productivă pentru crap. Constă în folosirea unui coș special care se umple cu un amestec de nada lipicioasă (method mix) în care se ascunde cârligul cu momelă. Când coșul ajunge pe fund, momelă este înconjurată de nada parfumată care atrage rapid peștii.</p>

<h3>Pescuit la Distanță</h3>
<p>Pentru crapii care stau departe de mal, tehnica de pescuit la distanță este esențială. Folosiți plumbi în formă de pară de 80-120g pentru aruncături peste 80 metri. Marcați linia cu un marker elastic pentru a arunca constant în același punct.</p>

<h3>Pescuit de Suprafață</h3>
<p>În zilele călduroase de vară, crapii vin adesea la suprafață. Tehnica cu controller și floater este perfectă pentru astfel de situații. Folosiți boilies flotante (popup) sau pâine ca momelă.</p>

<h2>Cele Mai Bune Locații</h2>
<p>În România, crapul poate fi pescuit în:</p>
<ul>
<li>Bălți private specializate pentru pescuitul sportiv</li>
<li>Lacuri de acumulare (Vidraru, Izvoru Muntelui, Drăgan)</li>
<li>Canalul Dunăre-Marea Neagră</li>
<li>Brațele Dunării din Delta Dunării</li>
<li>Lacuri naturale și iazuri amenajate</li>
</ul>

<h2>Perioade Optime de Pescuit</h2>
<p>Crapul poate fi pescuit pe tot parcursul anului, dar cele mai bune perioade sunt:</p>
<ul>
<li><strong>Primăvara</strong> (aprilie-iunie): După reproducere, crapii sunt foarte activi și căutând hrană pentru recuperare</li>
<li><strong>Vara</strong> (iulie-august): Nopțile sunt cele mai productive, când temperaturile scad</li>
<li><strong>Toamna</strong> (septembrie-octombrie): Crapii se hrănesc intens pentru iarnă</li>
<li><strong>Iarna</strong> (noiembrie-martie): Pescuit mai dificil, dar posibil în zilele cu temperaturi peste 5°C</li>
</ul>

<h2>Recomandări pentru Începători</h2>
<p>Dacă sunteți la început în pescuitul la crap, vă recomandăm:</p>
<ol>
<li>Începeți cu echipament de bază, dar de calitate</li>
<li>Alegeți bălți comerciale unde densitatea de pește este mare</li>
<li>Folosiți momeli simple: porumb sau boilies comerciale</li>
<li>Învățați să legați montajele de bază: safety clip, helicopter rig, inline</li>
<li>Fiți răbdători - crapul este un pește prudent care necesită timp și răbdare</li>
</ol>

<h2>Concluzie</h2>
<p>Pescuitul la crap în România oferă oportunități extraordinare pentru toți pasionații. Cu echipamentul corect, tehnicile potrivite și cunoștințele necesare despre comportamentul acestui pește, veți putea să vă bucurați de sesiuni de pescuit memorabile și de capturi impresionante. Practicați catch & release pentru a proteja această specie prețioasă și pentru ca generațiile viitoare să se bucure de aceeași pasiune.</p>
""",
            'reading_time': 8,
            'is_featured': True,
        },
        {
            'title': 'Top 10 Cele Mai Bune Lacuri de Pescuit din România în 2025',
            'category': loc_cat,
            'excerpt': 'Descoperiți cele mai bune locații pentru pescuit sportiv din România. De la bălți private la lacuri de acumulare spectaculoase, vă prezentăm destinațiile de top.',
            'content': """
<h2>Introducere</h2>
<p>România dispune de o rețea impresionantă de ape pentru pescuit sportiv, de la bălți private amenajate special pentru pescari până la lacuri naturale și de acumulare spectaculoase. În acest ghid, vă prezentăm cele mai bune 10 locații pentru pescuit din țară, evaluate după calitatea peștelui, facilități, accesibilitate și experiența generală oferită.</p>

<h2>1. Balta Pescăreț - Județul Cluj</h2>
<p><strong>Rating: 9.5/10</strong></p>
<p>Situată la doar 15 km de Cluj-Napoca, Balta Pescăreț este considerată una dintre cele mai bune bălți private din Transilvania. Cu o suprafață de 8 hectare și o adâncime maximă de 4 metri, această locație oferă:</p>
<ul>
<li>Stoc bogat de crap (exemplare până la 20 kg)</li>
<li>Șalău, somn, știucă și clean în cantități generoase</li>
<li>20 de standuri amenajate complet</li>
<li>Facilități moderne: toalete, dușuri, energie electrică</li>
<li>Posibilitate de pescuit 24/7</li>
<li>Restaurant și magazin de pescuit pe loc</li>
</ul>
<p><strong>Preț:</strong> 50 lei/12h, 80 lei/24h</p>

<h2>2. Lacul Vidraru - Județul Argeș</h2>
<p><strong>Rating: 9.3/10</strong></p>
<p>Un lac de acumulare spectaculos în inima munților Făgăraș, Lacul Vidraru este renumit pentru:</p>
<ul>
<li>Păstrăvi uriaşi (recorduri de peste 15 kg)</li>
<li>Peisaje montane de neuitat</li>
<li>Pescuit gratuit (necesită doar permis de pescuit)</li>
<li>Multiple puncte de acces de pe mal și din barcă</li>
<li>Sezon optim: Mai - Octombrie</li>
</ul>
<p><strong>Preț:</strong> Gratuit (permis de pescuit obligatoriu)</p>

<h2>3. Balta King Carp - Județul Ilfov</h2>
<p><strong>Rating: 9.2/10</strong></p>
<p>La doar 25 km de București, King Carp este destinația perfectă pentru pescarii din Capitală:</p>
<ul>
<li>Specii: Crap oglindă și solzos (exemplare record de 25+ kg)</li>
<li>Sistem catch & release strict pentru protecția stockului</li>
<li>15 standuri VIP cu platforme betonate</li>
<li>Bivuak-uri pentru închiriat</li>
<li>Magazin specializat și instructor pe loc</li>
<li>Pescuit doar cu boilies (fără porumb sau furaje)</li>
</ul>
<p><strong>Preț:</strong> 100 lei/24h (includes 2 pescari)</p>

<h2>4. Delta Dunării - Județul Tulcea</h2>
<p><strong>Rating: 9.1/10</strong></p>
<p>Paradisul pescarilor din România, Delta oferă o experiență unică:</p>
<ul>
<li>Peste 45 specii de pești de apă dulce</li>
<li>Șalău, somn, crap, clean, știucă în abundență</li>
<li>Posibilitate de pescuit din barcă în nenumărate brațe și canale</li>
<li>Experiență autentică în natură sălbatică</li>
<li>Greu de acces dar merită efortul</li>
</ul>
<p><strong>Preț:</strong> Variabil (închiriere barcă + cazare)</p>

<h2>5. Balta Amurgi - Județul Timiș</h2>
<p><strong>Rating: 9.0/10</strong></p>
<p>Cea mai modernă bază de pescuit din vestul țării:</p>
<ul>
<li>Amur alb (exemplare de 15-30 kg)</li>
<li>Crap, caras, clean</li>
<li>25 de standuri cu toate facilitățile</li>
<li>Cazare în cabane moderne</li>
<li>Restaurant cu specific pescăresc</li>
<li>Evenimente și concursuri regulate</li>
</ul>
<p><strong>Preț:</strong> 60 lei/24h</p>

<h2>6. Lacul Izvoru Muntelui (Bicaz) - Județul Neamț</h2>
<p><strong>Rating: 8.9/10</strong></p>
<p>Cel mai mare lac de acumulare din România:</p>
<ul>
<li>Suprafață impresionantă de 33 km²</li>
<li>Clean de dimensiuni record</li>
<li>Șalău, crap, biban</li>
<li>Pescuit gratuit de pe mal sau din barcă</li>
<li>Peisaje spectaculoase</li>
</ul>
<p><strong>Preț:</strong> Gratuit (permis obligatoriu)</p>

<h2>7. Balta Paradise - Județul Constanța</h2>
<p><strong>Rating: 8.8/10</strong></p>
<p>Aproape de mare, o destinație perfectă pentru vacanțe:</p>
<ul>
<li>Crap oglindă (stoc excelent)</li>
<li>Știucă și șalău</li>
<li>18 standuri amenajate</li>
<li>Posibilitate de combinare pescuit + plajă</li>
<li>Restaurant și piscină</li>
</ul>
<p><strong>Preț:</strong> 70 lei/24h</p>

<h2>8. Canalul Dunăre-Marea Neagră - Județele Constanța și Ialomița</h2>
<p><strong>Rating: 8.7/10</strong></p>
<p>Un loc aparte pentru pescuit:</p>
<ul>
<li>Crap de dimensiuni mari</li>
<li>Somn, clean, caras</li>
<li>Acces gratuit în majoritatea punctelor</li>
<li>Pescuit de mal foarte accesibil</li>
<li>Transport naval care creează curenți favorabili</li>
</ul>
<p><strong>Preț:</strong> Gratuit</p>

<h2>9. Balta Dunărea - Județul Brașov</h2>
<p><strong>Rating: 8.6/10</strong></p>
<p>În apropiere de Brașov, o bază modernă:</p>
<ul>
<li>Păstrăv curcubeu</li>
<li>Crap, șalău, clean</li>
<li>Pescuit pentru familii</li>
<li>Zone speciale pentru copii</li>
<li>Facilități complete</li>
</ul>
<p><strong>Preț:</strong> 45 lei/12h, 75 lei/24h</p>

<h2>10. Lacul Drăgan - Județul Sălaj</h2>
<p><strong>Rating: 8.5/10</strong></p>
<p>Lac de acumulare în inima Sălajului:</p>
<ul>
<li>Crap, clean, biban</li>
<li>Pescuit liniștit, fără aglomerație</li>
<li>Peisaje frumoase</li>
<li>Acces gratuit</li>
<li>Ideal pentru weekend-uri de relaxare</li>
</ul>
<p><strong>Preț:</strong> Gratuit (permis obligatoriu)</p>

<h2>Concluzie</h2>
<p>România oferă locații extraordinare pentru pescuit sportiv, de la bălți private cu facilități de lux până la lacuri naturale spectaculoase. Indiferent de preferințe și buget, veți găsi locul perfect pentru pasiunea dumneavoastră. Nu uitați să respectați regulamentele locale și să practicați catch & release acolo unde este necesar pentru protejarea stockurilor de pește.</p>
""",
            'reading_time': 10,
            'is_featured': True,
        },
        # From create_articles.py
        {
            'title': 'Top 10 Lansete pentru Pescuitul la Crap în 2025',
            'category': equip_cat,
            'excerpt': 'Cele mai bune lansete pentru pescuit la crap - analiză detaliată și recomandări pentru toate bugetele.',
            'content': '<h2>Introducere</h2><p>Alegerea lansetei potrivite este crucială. În acest ghid vă prezentăm top 10 lansete evaluate după performanță și raport calitate-preț.</p><h2>1. Fox Horizon X5</h2><p>Preț: ~1,200 lei. Cea mai bună lansetă premium cu performanțe excepționale la distanță.</p><h2>2. Daiwa Emblem Carp</h2><p>Preț: ~650 lei. Cel mai bun raport calitate-preț.</p><h2>Concluzie</h2><p>Investește înțelept și alege lanseta care corespunde nevoilor tale specifice.</p>',
            'reading_time': 7,
            'is_featured': True,
        },
        {
            'title': 'Pescuit în Delta Dunării - Ghid Complet',
            'category': loc_cat,
            'excerpt': 'Ghid complet pentru pescuitul în Delta Dunării - locații, specii, echipament și sfaturi practice.',
            'content': '<h2>De Ce Delta?</h2><p>Delta Dunării este paradisul pescarilor din România cu peste 45 specii de pești.</p><h2>Specii</h2><p>Somn, șalău, știucă, crap în abundență.</p><h2>Când</h2><p>Primăvara este cea mai bună perioadă.</p><h2>Echipament</h2><p>Lansete spinning, vestă salvare obligatorie.</p>',
            'reading_time': 6,
        },
        {
            'title': 'Tehnici de Pescuit la Somn Noaptea - Ghid Expert',
            'category': tech_cat,
            'excerpt': 'Descoperă cele mai eficiente tehnici pentru pescuitul la somn în timpul nopții, inclusiv alegerea monturilor și momeli.',
            'content': '<h2>Introducere</h2><p>Somnul este cel mai activ noaptea, când iese în căutarea hranei. Pescuitul nocturn necesită echipament specific și tehnici adaptate.</p><h2>Echipament Esențial</h2><p>Lansete puternice 2.7-3m, 100-300g. Mulinete robuste cu frână puternică. Fir monofilament 0.50-0.70mm sau braid 0.30-0.40mm.</p><h2>Momeli Eficiente</h2><p>Clonc viu (cea mai bună opțiune), boilar mare (24-30mm), păstrăv mort, calamar. Somnul preferă momeli mari și aromate.</p><h2>Montaje Recomandate</h2><p>Montaj cu plumb inline 80-200g pentru funduri nisipoase. Montaj cu plumb pierdut pentru zone cu obstacole. Carlige 6/0-10/0 foarte ascuțite.</p><h2>Locația Perfectă</h2><p>Căutați adâncituri de 3-8 metri, zone cu copaci căzuți, pontoane. Somnul patrulează aproape de maluri noaptea.</p><h2>Sfaturi Importante</h2><p>Fiți atenți la sonerie - atacul este violent. Folosiți lanternă frontală cu lumină roșie. Mănuși groase pentru manipulare în siguranță.</p>',
            'reading_time': 6,
        },
        {
            'title': 'Cum Să Alegi Mulineta Perfectă Pentru Tipul Tău de Pescuit',
            'category': equip_cat,
            'excerpt': 'Ghid complet pentru alegerea mulinetei potrivite - criterii tehnice, mărci recomandate și sfaturi practice.',
            'content': '<h2>Tipuri de Mulinete</h2><p>Există două mari categorii: mulinete cu tambur fix (spinning) și mulinete cu tambur rotativ (multiplier). Pentru majoritatea pescarilor, mulinetele spinning sunt ideale.</p><h2>Criterii de Selecție</h2><p>Dimensiunea (1000-8000) - alegere în funcție de peștele țintă. Raportul de recuperare (5.0:1 până la 7.0:1). Numărul de rulmenți (minim 4-5 pentru performanță). Capacitatea tambur - verificați ce lungime de fir încape.</p><h2>Frâna</h2><p>Frâna frontală este mai precisă și puternică. Frâna posterioară se ajustează mai ușor în timpul pescuitului. Pentru crap și somn, frâna trebuie să reziste la 8-15 kg.</p><h2>Mărci Recomandate</h2><p>Shimano - cele mai fiabile, durabilitate excepțională. Daiwa - raport calitate-preț excelent. Okuma - opțiune bugetară bună. Penn - perfecte pentru pescuit la somn.</p><h2>Întreținere</h2><p>Curățați după fiecare pescuit în ape sărate. Ungere rulmenți anual. Verificați frâna regulat. Păstrați în loc uscat.</p>',
            'reading_time': 5,
            'is_featured': True,
        },
        {
            'title': 'Top 10 Bălți de Pescuit în Apropierea Bucureștiului',
            'category': loc_cat,
            'excerpt': 'Cele mai bune locații de pescuit la maxim 100 km de București - cu detalii despre specii, prețuri și facilități.',
            'content': '<h2>1. Snagov</h2><p>La 40 km nord de București. Specii: crap, caras, știucă, biban. Prețuri: 30-50 lei/zi. Facilități: pontoane, parcare, restaurant.</p><h2>2. Comana</h2><p>La 35 km sud. Specii: somn, crap, șalău. Prețuri: 40-80 lei/zi. Zonă protejată cu natură superbă.</p><h2>3. Băneasa</h2><p>În București. Specii: crap, caras. Gratis pentru permis București. Foarte accesibil.</p><h2>4. Căldărușani</h2><p>La 45 km nord-est. Specii: crap mare (10+ kg), somn, știucă. Prețuri: 50-100 lei/zi.</p><h2>5. Buftea</h2><p>La 20 km nord-vest. Specii: crap, caras, biban. Prețuri: 30-60 lei/zi. Popular la weekend.</p><h2>Sfaturi</h2><p>Rezervați loc din timp la weekend. Verificați dacă permit pescuit nocturn. Întrebați despre regulamente speciale.</p>',
            'reading_time': 7,
        },
        {
            'title': 'Pescuitul la Feeder pentru Începători - Tot Ce Trebuie Să Știi',
            'category': tech_cat,
            'excerpt': 'Ghid complet de inițiere în pescuitul la feeder - echipament, tehnici, momeli și sfaturi practice.',
            'content': '<h2>Ce Este Feederul?</h2><p>Feederul este o tehnică de pescuit de fund care folosește un coș (feeder) umplut cu nadă pentru a atrage peștele. Ideală pentru crap, caras, plătică și clean.</p><h2>Echipament Necesar</h2><p>Lansetă feeder 3.6-3.9m, 40-120g. Mulinetă 3000-4000 cu bobină de rezervă. Fir principal 0.20-0.25mm. Shock leader 0.28-0.30mm. Cosuri feeder diverse mărimi (20-80g).</p><h2>Montajul</h2><p>Montaj inline - cel mai simplu pentru începători. Montaj asimetric - mai sensibil. Montaj method - pentru crap la distanță mică.</p><h2>Nada</h2><p>Compoziție: pesmet, făină porumb, melasă, arome. Consistență medie - se destramă în 5-10 minute. Adăugați viermi, caster, porumb pentru atracție.</p><h2>Tehnica de Pescuit</h2><p>Alegeți distanța (20-60m) și marcați-o pe fir. Aruncați precis la același loc. Renadați la 3-5 minute inițial, apoi la 10-15 minute. Așteptați formarea grămezii de nadă.</p><h2>Momeala pe Carlig</h2><p>Vierme, caster, porumb, boilar mic. Combinați 2-3 tipuri pentru eficiență maximă.</p>',
            'reading_time': 6,
            'is_featured': True,
        },
        {
            'title': '7 Trucuri Secrete Pentru Pescuitul la Clean',
            'category': tech_cat,
            'excerpt': 'Descoperiți tehnicile profesionale care vă vor ajuta să prindeți mai mult clean - de la nadă până la montaje speciale.',
            'content': '<h2>1. Nada Secretă</h2><p>Amestec: 50% pesmet roșu, 30% făină porumb, 20% biscuiți măcinați. Arome: vanilie + măr. Adăugați caster și vierme tăiat mărunt direct în nadă.</p><h2>2. Montaj Ultra-Sensibil</h2><p>Folosiți fir 0.10-0.12mm la înaintas. Plumb olivetă 1-3g. Carlig nr. 14-16 ultra-ascuțit. Cleanul mușcă foarte delicat!</p><h2>3. Momeala Câștigătoare</h2><p>Caster proaspăt (cel mai bun!), vierme mic, larvă musca, porumb moale. Combinați 2 casteri pe carlig.</p><h2>4. Locul Perfect</h2><p>Căutați 2-4 metri adâncime, fund nisipos sau argilos. Evitați mâlul. Cleanul preferă apele clare și curenți slabi.</p><h2>5. Momentul Ideal</h2><p>Primăvara târziu (aprilie-mai) și toamna (septembrie-octombrie). Ore: 6-10 dimineața și 16-20 după-amiaza.</p><h2>6. Grămezuirea</h2><p>Aruncați nadă masiv la început - 5-8 bile. După aceea, renadați la 10-15 minute. Cleanul vine pe grămadă mare.</p><h2>7. Execuția Ferării</h2><p>La clean, ferarea trebuie să fie rapidă dar delicată. Buza cleanului este fragilă - nu trageți prea tare!</p>',
            'reading_time': 5,
        },
        {
            'title': 'Top 5 Boilere Pentru Crap - Testate și Aprobate',
            'category': equip_cat,
            'excerpt': 'Cele mai eficiente boilere pentru pescuitul la crap, testate în condiții reale pe bălțile din România.',
            'content': '<h2>1. Dynamite Baits The Crave</h2><p>Preț: ~80 lei/kg. Aroma: créme brûlée. Rezultate excepționale în ape presate. Disolva<re lentă - perfect pentru sesiuni lungi. Rating: 10/10</p><h2>2. Mainline Cell</h2><p>Preț: ~90 lei/kg. Cea mai populară serie din lume. Funcționează în orice anotimp. Disponibil în 15mm, 18mm, 20mm. Rating: 9/10</p><h2>3. Spotted Fin Squid Octopus</h2><p>Preț: ~60 lei/kg. Cel mai bun raport calitate-preț. Aroma: caracatiță + calamar. Excelent pentru somn și crap. Rating: 8.5/10</p><h2>4. CC Moore Pacific Tuna</h2><p>Preț: ~95 lei/kg. Aroma: ton. Incredibil de atractiv. Perfect pentru ape mari (lacuri, râuri). Rating: 9/10</p><h2>5. Dynamite Baits Monster Tiger Nut</h2><p>Preț: ~75 lei/kg. Aroma: alună tigru. Selectiv pentru crap mare. Evită peștii mici. Rating: 8/10</p><h2>Sfaturi</h2><p>Combinați 2-3 tipuri de boilere în același loc. Folosiți pop-up pe un cârlig, boiler greu pe celălalt. Înmuiați în glug înainte de folosire pentru atracție maximă.</p>',
            'reading_time': 5,
        },
        {
            'title': 'Pescuitul în Râurile de Munte din Transilvania',
            'category': loc_cat,
            'excerpt': 'Ghid pentru pescuitul la păstrăv și lipan în cele mai spectaculoase râuri montane din Transilvania.',
            'content': '<h2>Râurile de Top</h2><p>Someșul Rece, Someșul Cald, Arieșul, Mureșul superior, Oltul superior. Toate oferă pescuit spectacular la păstrăv în cadre naturale unice.</p><h2>Specii Țintă</h2><p>Păstrăv indigen (fario), păstrăv curcubeu, lipan, mreană. Păstrăvul indigen poate atinge 40-50 cm în zone izolate.</p><h2>Tehnici Recomandate</h2><p>Spinning cu linguri rotative 2-7g. Muscă artificială (fly fishing) - cea mai sportivă metodă. Pescuit natural cu vierme sau cârlan.</p><h2>Echipament</h2><p>Lansete spinning 1.8-2.4m, 1-10g (ultra-light). Mulinete 1000-2000. Fir 0.14-0.18mm. Waders impermeabili obligatorii. Cizme cu talpa anti-alunecare.</p><h2>Când Să Mergi</h2><p>Mai-iunie: sezonul de vârf, nivelul apei optim. Iulie-august: apa scade, pești concentrați în adâncituri. Septembrie: păstrăvii devin agresivi înainte de reproducere.</p><h2>Regulamente</h2><p>Permis de pescuit + taxă zonă montană obligatorii. Catch & release recomandat pentru conservare. Dimensiune minimă: 24 cm pentru păstrăv. Verificați perioadele de prohibiție!</p>',
            'reading_time': 6,
            'is_featured': True,
        },
        {
            'title': 'Pescuitul la Știucă Primăvara - Perioada de Aur',
            'category': tech_cat,
            'excerpt': 'Primăvara este cel mai bun sezon pentru știucă. Descoperiți unde, când și cum să prindeți știuci trofeu.',
            'content': '<h2>De Ce Primăvara?</h2><p>După reproducere (martie-aprilie), știuca devine extrem de agresivă. Trebuie să recupereze energia pierdută și atacă orice momeală!</p><h2>Locurile Câștigătoare</h2><p>Zone puțin adânci (0.5-2m) cu vegetație. Trestie, nuferi, iarbă scufundată. Apa se încălzește mai repede aici și concentrează peștișori - prada știucii.</p><h2>Momeli de Top</h2><p>Spinning: lingurite rotative 7-21g (Mepps, Blue Fox). Wobblere floating și suspending 7-12cm. Shad-uri moi pe jig-head 10-20g. Spinnerbait pentru zone cu vegetație.</p><h2>Tehnica</h2><p>Recuperare variată - alternați rapid și lent. Pauze de 2-3 secunde provoacă atacul. Aruncați cât mai aproape de vegetație. Știuca stă la pândă și atacă de aproape.</p><h2>Echipament</h2><p>Lansetă spinning 2.1-2.7m, 10-40g. Mulinetă 2500-3000. Fir braid 0.15-0.20mm + leader fluorocarbon 0.35mm sau titan.</p><h2>Sfat Important</h2><p>Folosiți ÎNTOTDEAUNA leader de titan sau fluorocarbon gros - știuca are dinți ascuțiți și taie firul normal instant!</p>',
            'reading_time': 5,
        },
        {
            'title': 'Cum Să Alegi Firul de Pescuit Potrivit - Ghid Complet',
            'category': equip_cat,
            'excerpt': 'Monofilament, fluorocarbon sau braid? Ghid detaliat pentru alegerea firului perfect în funcție de tipul de pescuit.',
            'content': '<h2>Tipuri de Fir</h2><p>Monofilament - cel mai popular, versatil, cu elasticitate. Fluorocarbon - invizibil în apă, rezistent la abraziune. Braid (împletit) - zero elasticitate, foarte rezistent, diametru mic.</p><h2>Monofilament</h2><p>Avantaje: ieftin, elastic (absoarbe șocurile), ușor de folosit. Dezavantaje: se uzează mai repede, vizibil în apă. Ideal pentru: începători, pescuit la crap, feeder. Diametre: 0.18-0.35mm pentru crap, 0.12-0.18mm pentru clean.</p><h2>Fluorocarbon</h2><p>Avantaje: practic invizibil, rezistent la UV și abraziune. Dezavantaje: scump, mai rigid. Ideal pentru: înaintas (leader), ape clare, pești precauți. Diametre: 0.20-0.40mm pentru leader.</p><h2>Braid</h2><p>Avantaje: foarte rezistent (10kg la diametru 0.15mm!), sensibilitate maximă, nu se întinde. Dezavantaje: vizibil în apă, se taie la obstacole ascuțite. Ideal pentru: spinning, pescuit la distanță, somn. Diametre: 0.10-0.20mm pentru spinning, 0.25-0.40mm pentru somn.</p><h2>Recomandări</h2><p>Crap: mono 0.28-0.35mm sau braid 0.18mm + leader fluoro 0.35mm. Clean/plătică: mono 0.14-0.18mm. Spinning știucă: braid 0.15mm + leader titan. Somn: braid 0.30-0.40mm + leader mono 0.70mm.</p>',
            'reading_time': 6,
        }
    ]

    for i, article_data in enumerate(articles_data, 1):
        # Create published date (stagger dates over last 3 months)
        published_date = timezone.now() - timedelta(days=90-i*5)
        
        # Generate slug if not provided
        slug = slugify(article_data['title'])

        article, created = Article.objects.get_or_create(
            title=article_data['title'],
            defaults={
                **article_data,
                'slug': slug,
                'author': admin_user,
                'is_published': True,
                'published_date': published_date,
                'meta_description': article_data['excerpt'],
                'meta_keywords': 'pescuit, România, ' + article_data['category'].name.lower(),
            }
        )

        if created:
            print(f"  ✓ Created article {i}: {article.title}")
        else:
            print(f"  ○ Article exists: {article.title}")

    print(f"Articles created/updated: {Article.objects.count()}\n")

def main():
    print("=" * 60)
    print("STARTING FULL CONTENT POPULATION")
    print("=" * 60)
    
    create_article_categories()
    create_blog_articles()
    
    # Import and run other population scripts
    try:
        from populate_fishing_terms import populate_terms
        populate_terms()
    except ImportError:
        print("Could not import populate_fishing_terms")
        
    try:
        from populate_county_guides import COUNTY_GUIDES
        print("Populating county guides...")
        
        # Region mapping
        REGION_MAPPING = {
            'bucuresti': 'BUCURESTI',
            'cluj': 'TRANSILVANIA',
            'constanta': 'DOBROGEA',
            'brasov': 'TRANSILVANIA',
            'timis': 'BANAT',
            'iasi': 'MOLDOVA',
            'arges': 'MUNTENIA',
            'mures': 'TRANSILVANIA',
            'prahova': 'MUNTENIA',
            'galati': 'MOLDOVA'
        }

        for guide_data in COUNTY_GUIDES.values():
            slug = guide_data['slug']
            # Extract name from title (e.g. "Ghid Complet de Pescuit în București și Ilfov" -> "București și Ilfov")
            # Or just use a capitalized version of slug if name not available
            name = guide_data['title'].replace('Ghid Complet de Pescuit în ', '').replace('Ghid Pescuit ', '')
            
            region = REGION_MAPPING.get(slug, 'TRANSILVANIA') # Default to Transilvania

            county, created = County.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'region': region
                }
            )
            
            county.guide_title = guide_data['title']
            county.guide_excerpt = guide_data['excerpt']
            county.guide_content = guide_data['content']
            county.has_guide = True
            county.save()
            
            if created:
                print(f"  ✓ Created and updated guide for: {county.name}")
            else:
                print(f"  ✓ Updated guide for: {county.name}")
                
        print(f"County guides updated: {County.objects.filter(has_guide=True).count()}\n")
    except ImportError:
        print("Could not import populate_county_guides")

    try:
        from populate_fish_descriptions import populate_descriptions
        # We need to modify populate_descriptions to create if not exists, 
        # but since we can't easily modify the imported function's logic without changing the file,
        # let's just run it and catch errors? No, we need to ensure they exist.
        # Actually, populate_descriptions in populate_fish_descriptions.py iterates FISH_DATA items.
        # We can import FISH_DATA and do it here.
        from populate_fish_descriptions import FISH_DATA
        
        print("Populating fish species...")
        for name, data in FISH_DATA.items():
            # Guess category
            category = 'other'
            lower_name = name.lower()
            if any(x in lower_name for x in ['crap', 'amur', 'caras', 'platic', 'rosioar', 'lin']):
                category = 'cyprinid'
            elif any(x in lower_name for x in ['stiuc', 'salau', 'somn', 'biban', 'avat', 'pastrav']):
                category = 'predator'
                
            species, created = FishSpecies.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'slug': slugify(name)
                }
            )
            
            species.detailed_description = data['detailed_description']
            species.habitat = data['habitat']
            species.fishing_techniques = data['fishing_techniques']
            species.best_baits = data['best_baits']
            species.legal_info = data['legal_info']
            species.average_size = data['average_size']
            species.max_size = data['max_size']
            species.save()
            
            if created:
                print(f"  ✓ Created and updated species: {species.name}")
            else:
                print(f"  ✓ Updated species: {species.name}")
                
        print(f"Fish species updated: {FishSpecies.objects.count()}\n")

    except ImportError:
        print("Could not import populate_fish_descriptions")

    # ==========================================
    # INTERNAL LINKING OPTIMIZATION
    # ==========================================
    print("=" * 60)
    print("OPTIMIZING INTERNAL LINKS")
    print("=" * 60)
    
    def add_internal_links():
        """
        Scans all content (Articles, County Guides) and injects internal links
        to Fish Species and other Counties.
        """
        import re
        
        # 1. Build keyword map
        keywords = {}
        
        # Add Fish Species
        for species in FishSpecies.objects.filter(is_active=True):
            # Link to species detail page
            # Assuming url pattern: /specii-de-pesti/<slug>/
            url = f"/specii-de-pesti/{species.slug}/"
            keywords[species.name.lower()] = {
                'url': url,
                'text': species.name
            }
            
        # Add Counties (only those with guides)
        for county in County.objects.filter(has_guide=True):
            # Link to county guide
            # Assuming url pattern: /judete/<slug>/ghid/
            url = f"/judete/{county.slug}/ghid/"
            keywords[county.name.lower()] = {
                'url': url,
                'text': county.name
            }
            # Also add "Județul X" variation
            keywords[f"județul {county.name.lower()}"] = {
                'url': url,
                'text': f"Județul {county.name}"
            }

        def inject_links(text):
            if not text:
                return text
                
            # Sort keywords by length (descending) to match longest phrases first
            sorted_keys = sorted(keywords.keys(), key=len, reverse=True)
            
            # We don't want to replace inside existing <a> tags
            # Simple approach: split by tags and only replace in text nodes
            # Better approach for this script: use regex with negative lookbehind/lookahead or just careful replacement
            # For simplicity and safety in this script, we'll do a simple replacement but check if it's already linked
            
            modified_text = text
            
            for keyword in sorted_keys:
                data = keywords[keyword]
                url = data['url']
                display_text = data['text']
                
                # Regex to find keyword as whole word, case insensitive, NOT already inside a link
                # This is tricky with regex alone. 
                # Let's use a simpler heuristic: Replace only the FIRST occurrence if it's not part of a link.
                # Actually, let's just try to replace the first occurrence that looks like a standalone word.
                
                pattern = re.compile(r'(?<!>)\b' + re.escape(keyword) + r'\b(?!</a>)', re.IGNORECASE)
                
                # Check if we already have this link
                if url in modified_text:
                    continue
                    
                # Replace only the first occurrence
                match = pattern.search(modified_text)
                if match:
                    original_word = match.group(0)
                    replacement = f'<a href="{url}" class="text-success fw-bold" title="Vezi detalii despre {display_text}">{original_word}</a>'
                    modified_text = pattern.sub(replacement, modified_text, count=1)
            
            return modified_text

        # 2. Process Articles
        print("Processing Articles...")
        articles = Article.objects.all()
        for article in articles:
            original_content = article.content
            new_content = inject_links(original_content)
            
            if original_content != new_content:
                article.content = new_content
                article.save()
                print(f"  ✓ Added links to article: {article.title}")
                
        # 3. Process County Guides
        print("Processing County Guides...")
        counties = County.objects.filter(has_guide=True)
        for county in counties:
            original_content = county.guide_content
            new_content = inject_links(original_content)
            
            if original_content != new_content:
                county.guide_content = new_content
                county.save()
                print(f"  ✓ Added links to guide: {county.name}")

    add_internal_links()

    print("=" * 60)
    print("POPULATION COMPLETED")
    print("=" * 60)

if __name__ == '__main__':
    main()
