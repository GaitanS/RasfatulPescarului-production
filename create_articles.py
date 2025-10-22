#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pentru crearea articolelor de blog de test
"""
import os
import sys
import django

# Fix pentru encoding Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import ArticleCategory, Article
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def main():
    admin = User.objects.filter(is_superuser=True).first()

    # Obțin categoriile
    cat_tehnici = ArticleCategory.objects.get(slug='tehnici-pescuit')
    cat_echip = ArticleCategory.objects.get(slug='echipamente')
    cat_locatii = ArticleCategory.objects.get(slug='locatii-pescuit')

    articles_created = 0

    print("Creez articole de blog...\n")

    # Articol 2: Echipament
    article2, created = Article.objects.get_or_create(
        slug='top-10-lansete-pescuit-carp-2025',
        defaults={
            'title': 'Top 10 Lansete pentru Pescuitul la Crap în 2025',
            'category': cat_echip,
            'author': admin,
            'excerpt': 'Cele mai bune lansete pentru pescuit la crap - analiză detaliată și recomandări pentru toate bugetele.',
            'content': '<h2>Introducere</h2><p>Alegerea lansetei potrivite este crucială. În acest ghid vă prezentăm top 10 lansete evaluate după performanță și raport calitate-preț.</p><h2>1. Fox Horizon X5</h2><p>Preț: ~1,200 lei. Cea mai bună lansetă premium cu performanțe excepționale la distanță.</p><h2>2. Daiwa Emblem Carp</h2><p>Preț: ~650 lei. Cel mai bun raport calitate-preț.</p><h2>Concluzie</h2><p>Investește înțelept și alege lanseta care corespunde nevoilor tale specifice.</p>',
            'reading_time': 7,
            'is_published': True,
            'is_featured': True,
            'published_date': timezone.now() - timedelta(days=7),
            'meta_description': 'Top 10 lansete pescuit carp 2025',
            'meta_keywords': 'lansete carp, echipament pescuit'
        }
    )
    if created:
        articles_created += 1
        print(f"[OK] Articol creat: {article2.title}")

    # Articol 3
    article3, created = Article.objects.get_or_create(
        slug='pescuit-delta-dunarii-ghid',
        defaults={
            'title': 'Pescuit în Delta Dunării - Ghid Complet',
            'category': cat_locatii,
            'author': admin,
            'excerpt': 'Ghid complet pentru pescuitul în Delta Dunării - locații, specii, echipament și sfaturi practice.',
            'content': '<h2>De Ce Delta?</h2><p>Delta Dunării este paradisul pescarilor din România cu peste 45 specii de pești.</p><h2>Specii</h2><p>Somn, șalău, știucă, crap în abundență.</p><h2>Când</h2><p>Primăvara este cea mai bună perioadă.</p><h2>Echipament</h2><p>Lansete spinning, vestă salvare obligatorie.</p>',
            'reading_time': 6,
            'is_published': True,
            'published_date': timezone.now() - timedelta(days=14),
            'meta_description': 'Ghid pescuit Delta Dunării',
            'meta_keywords': 'pescuit delta, somn, salau'
        }
    )
    if created:
        articles_created += 1
        print(f"[OK] Articol creat: {article3.title}")

    # Articol 4: Tehnici
    article4, created = Article.objects.get_or_create(
        slug='tehnici-pescuit-somn-noapte',
        defaults={
            'title': 'Tehnici de Pescuit la Somn Noaptea - Ghid Expert',
            'category': cat_tehnici,
            'author': admin,
            'excerpt': 'Descoperă cele mai eficiente tehnici pentru pescuitul la somn în timpul nopții, inclusiv alegerea monturilor și momeli.',
            'content': '<h2>Introducere</h2><p>Somnul este cel mai activ noaptea, când iese în căutarea hranei. Pescuitul nocturn necesită echipament specific și tehnici adaptate.</p><h2>Echipament Esențial</h2><p>Lansete puternice 2.7-3m, 100-300g. Mulinete robuste cu frână puternică. Fir monofilament 0.50-0.70mm sau braid 0.30-0.40mm.</p><h2>Momeli Eficiente</h2><p>Clonc viu (cea mai bună opțiune), boilar mare (24-30mm), păstrăv mort, calamar. Somnul preferă momeli mari și aromate.</p><h2>Montaje Recomandate</h2><p>Montaj cu plumb inline 80-200g pentru funduri nisipoase. Montaj cu plumb pierdut pentru zone cu obstacole. Carlige 6/0-10/0 foarte ascuțite.</p><h2>Locația Perfectă</h2><p>Căutați adâncituri de 3-8 metri, zone cu copaci căzuți, pontoane. Somnul patrulează aproape de maluri noaptea.</p><h2>Sfaturi Importante</h2><p>Fiți atenți la sonerie - atacul este violent. Folosiți lanternă frontală cu lumină roșie. Mănuși groase pentru manipulare în siguranță.</p>',
            'reading_time': 6,
            'is_published': True,
            'published_date': timezone.now() - timedelta(days=21),
            'meta_description': 'Tehnici pescuit somn noaptea',
            'meta_keywords': 'somn, pescuit nocturn, tehnici'
        }
    )
    if created:
        articles_created += 1
        print(f"[OK] Articol creat: {article4.title}")

    # Articol 5: Echipament
    article5, created = Article.objects.get_or_create(
        slug='alegerea-mulinetei-perfecte',
        defaults={
            'title': 'Cum Să Alegi Mulineta Perfectă Pentru Tipul Tău de Pescuit',
            'category': cat_echip,
            'author': admin,
            'excerpt': 'Ghid complet pentru alegerea mulinetei potrivite - criterii tehnice, mărci recomandate și sfaturi practice.',
            'content': '<h2>Tipuri de Mulinete</h2><p>Există două mari categorii: mulinete cu tambur fix (spinning) și mulinete cu tambur rotativ (multiplier). Pentru majoritatea pescarilor, mulinetele spinning sunt ideale.</p><h2>Criterii de Selecție</h2><p>Dimensiunea (1000-8000) - alegere în funcție de peștele țintă. Raportul de recuperare (5.0:1 până la 7.0:1). Numărul de rulmenți (minim 4-5 pentru performanță). Capacitatea tambur - verificați ce lungime de fir încape.</p><h2>Frâna</h2><p>Frâna frontală este mai precisă și puternică. Frâna posterioară se ajustează mai ușor în timpul pescuitului. Pentru crap și somn, frâna trebuie să reziste la 8-15 kg.</p><h2>Mărci Recomandate</h2><p>Shimano - cele mai fiabile, durabilitate excepțională. Daiwa - raport calitate-preț excelent. Okuma - opțiune bugetară bună. Penn - perfecte pentru pescuit la somn.</p><h2>Întreținere</h2><p>Curățați după fiecare pescuit în ape sărate. Ungere rulmenți anual. Verificați frâna regulat. Păstrați în loc uscat.</p>',
            'reading_time': 5,
            'is_published': True,
            'is_featured': True,
            'published_date': timezone.now() - timedelta(days=28),
            'meta_description': 'Ghid alegere mulineta pescuit',
            'meta_keywords': 'mulineta, echipament, spinning'
        }
    )
    if created:
        articles_created += 1
        print(f"[OK] Articol creat: {article5.title}")

    # Articol 6: Locații
    article6, created = Article.objects.get_or_create(
        slug='top-balti-pescuit-langa-bucuresti',
        defaults={
            'title': 'Top 10 Bălți de Pescuit în Apropierea Bucureștiului',
            'category': cat_locatii,
            'author': admin,
            'excerpt': 'Cele mai bune locații de pescuit la maxim 100 km de București - cu detalii despre specii, prețuri și facilități.',
            'content': '<h2>1. Snagov</h2><p>La 40 km nord de București. Specii: crap, caras, știucă, biban. Prețuri: 30-50 lei/zi. Facilități: pontoane, parcare, restaurant.</p><h2>2. Comana</h2><p>La 35 km sud. Specii: somn, crap, șalău. Prețuri: 40-80 lei/zi. Zonă protejată cu natură superbă.</p><h2>3. Băneasa</h2><p>În București. Specii: crap, caras. Gratis pentru permis București. Foarte accesibil.</p><h2>4. Căldărușani</h2><p>La 45 km nord-est. Specii: crap mare (10+ kg), somn, știucă. Prețuri: 50-100 lei/zi.</p><h2>5. Buftea</h2><p>La 20 km nord-vest. Specii: crap, caras, biban. Prețuri: 30-60 lei/zi. Popular la weekend.</p><h2>Sfaturi</h2><p>Rezervați loc din timp la weekend. Verificați dacă permit pescuit nocturn. Întrebați despre regulamente speciale.</p>',
            'reading_time': 7,
            'is_published': True,
            'published_date': timezone.now() - timedelta(days=35),
            'meta_description': 'Top balti pescuit Bucuresti',
            'meta_keywords': 'balti pescuit, Bucuresti, locatii'
        }
    )
    if created:
        articles_created += 1
        print(f"[OK] Articol creat: {article6.title}")

    # Articol 7: Tehnici
    article7, created = Article.objects.get_or_create(
        slug='pescuit-feeder-incepatori',
        defaults={
            'title': 'Pescuitul la Feeder pentru Începători - Tot Ce Trebuie Să Știi',
            'category': cat_tehnici,
            'author': admin,
            'excerpt': 'Ghid complet de inițiere în pescuitul la feeder - echipament, tehnici, momeli și sfaturi practice.',
            'content': '<h2>Ce Este Feederul?</h2><p>Feederul este o tehnică de pescuit de fund care folosește un coș (feeder) umplut cu nadă pentru a atrage peștele. Ideală pentru crap, caras, plătică și clean.</p><h2>Echipament Necesar</h2><p>Lansetă feeder 3.6-3.9m, 40-120g. Mulinetă 3000-4000 cu bobină de rezervă. Fir principal 0.20-0.25mm. Shock leader 0.28-0.30mm. Cosuri feeder diverse mărimi (20-80g).</p><h2>Montajul</h2><p>Montaj inline - cel mai simplu pentru începători. Montaj asimetric - mai sensibil. Montaj method - pentru crap la distanță mică.</p><h2>Nada</h2><p>Compoziție: pesmet, făină porumb, melasă, arome. Consistență medie - se destramă în 5-10 minute. Adăugați viermi, caster, porumb pentru atracție.</p><h2>Tehnica de Pescuit</h2><p>Alegeți distanța (20-60m) și marcați-o pe fir. Aruncați precis la același loc. Renadați la 3-5 minute inițial, apoi la 10-15 minute. Așteptați formarea grămezii de nadă.</p><h2>Momeala pe Carlig</h2><p>Vierme, caster, porumb, boilar mic. Combinați 2-3 tipuri pentru eficiență maximă.</p>',
            'reading_time': 6,
            'is_published': True,
            'is_featured': True,
            'published_date': timezone.now() - timedelta(days=42),
            'meta_description': 'Ghid pescuit feeder incepatori',
            'meta_keywords': 'feeder, tehnici pescuit, incepatori'
        }
    )
    if created:
        articles_created += 1
        print(f"[OK] Articol creat: {article7.title}")

    # Articol 8: Tehnici
    article8, created = Article.objects.get_or_create(
        slug='trucuri-pescuit-la-clean',
        defaults={
            'title': '7 Trucuri Secrete Pentru Pescuitul la Clean',
            'category': cat_tehnici,
            'author': admin,
            'excerpt': 'Descoperiți tehnicile profesionale care vă vor ajuta să prindeți mai mult clean - de la nadă până la montaje speciale.',
            'content': '<h2>1. Nada Secretă</h2><p>Amestec: 50% pesmet roșu, 30% făină porumb, 20% biscuiți măcinați. Arome: vanilie + măr. Adăugați caster și vierme tăiat mărunt direct în nadă.</p><h2>2. Montaj Ultra-Sensibil</h2><p>Folosiți fir 0.10-0.12mm la înaintas. Plumb olivetă 1-3g. Carlig nr. 14-16 ultra-ascuțit. Cleanul mușcă foarte delicat!</p><h2>3. Momeala Câștigătoare</h2><p>Caster proaspăt (cel mai bun!), vierme mic, larvă musca, porumb moale. Combinați 2 casteri pe carlig.</p><h2>4. Locul Perfect</h2><p>Căutați 2-4 metri adâncime, fund nisipos sau argilos. Evitați mâlul. Cleanul preferă apele clare și curenți slabi.</p><h2>5. Momentul Ideal</h2><p>Primăvara târziu (aprilie-mai) și toamna (septembrie-octombrie). Ore: 6-10 dimineața și 16-20 după-amiaza.</p><h2>6. Grămezuirea</h2><p>Aruncați nadă masiv la început - 5-8 bile. După aceea, renadați la 10-15 minute. Cleanul vine pe grămadă mare.</p><h2>7. Execuția Ferării</h2><p>La clean, ferarea trebuie să fie rapidă dar delicată. Buza cleanului este fragilă - nu trageți prea tare!</p>',
            'reading_time': 5,
            'is_published': True,
            'published_date': timezone.now() - timedelta(days=49),
            'meta_description': 'Trucuri pescuit clean',
            'meta_keywords': 'clean, tehnici, trucuri pescuit'
        }
    )
    if created:
        articles_created += 1
        print(f"[OK] Articol creat: {article8.title}")

    # Articol 9: Echipament
    article9, created = Article.objects.get_or_create(
        slug='top-5-boilere-pentru-crap',
        defaults={
            'title': 'Top 5 Boilere Pentru Crap - Testate și Aprobate',
            'category': cat_echip,
            'author': admin,
            'excerpt': 'Cele mai eficiente boilere pentru pescuitul la crap, testate în condiții reale pe bălțile din România.',
            'content': '<h2>1. Dynamite Baits The Crave</h2><p>Preț: ~80 lei/kg. Aroma: créme brûlée. Rezultate excepționale în ape presate. Disolva<re lentă - perfect pentru sesiuni lungi. Rating: 10/10</p><h2>2. Mainline Cell</h2><p>Preț: ~90 lei/kg. Cea mai populară serie din lume. Funcționează în orice anotimp. Disponibil în 15mm, 18mm, 20mm. Rating: 9/10</p><h2>3. Spotted Fin Squid Octopus</h2><p>Preț: ~60 lei/kg. Cel mai bun raport calitate-preț. Aroma: caracatiță + calamar. Excelent pentru somn și crap. Rating: 8.5/10</p><h2>4. CC Moore Pacific Tuna</h2><p>Preț: ~95 lei/kg. Aroma: ton. Incredibil de atractiv. Perfect pentru ape mari (lacuri, râuri). Rating: 9/10</p><h2>5. Dynamite Baits Monster Tiger Nut</h2><p>Preț: ~75 lei/kg. Aroma: alună tigru. Selectiv pentru crap mare. Evită peștii mici. Rating: 8/10</p><h2>Sfaturi</h2><p>Combinați 2-3 tipuri de boilere în același loc. Folosiți pop-up pe un cârlig, boiler greu pe celălalt. Înmuiați în glug înainte de folosire pentru atracție maximă.</p>',
            'reading_time': 5,
            'is_published': True,
            'published_date': timezone.now() - timedelta(days=56),
            'meta_description': 'Top boilere carp fishing',
            'meta_keywords': 'boilere, crap, echipament'
        }
    )
    if created:
        articles_created += 1
        print(f"[OK] Articol creat: {article9.title}")

    # Articol 10: Locații
    article10, created = Article.objects.get_or_create(
        slug='pescuit-munti-rauri-tranzilvenia',
        defaults={
            'title': 'Pescuitul în Râurile de Munte din Transilvania',
            'category': cat_locatii,
            'author': admin,
            'excerpt': 'Ghid pentru pescuitul la păstrăv și lipan în cele mai spectaculoase râuri montane din Transilvania.',
            'content': '<h2>Râurile de Top</h2><p>Someșul Rece, Someșul Cald, Arieșul, Mureșul superior, Oltul superior. Toate oferă pescuit spectacular la păstrăv în cadre naturale unice.</p><h2>Specii Țintă</h2><p>Păstrăv indigen (fario), păstrăv curcubeu, lipan, mreană. Păstrăvul indigen poate atinge 40-50 cm în zone izolate.</p><h2>Tehnici Recomandate</h2><p>Spinning cu linguri rotative 2-7g. Muscă artificială (fly fishing) - cea mai sportivă metodă. Pescuit natural cu vierme sau cârlan.</p><h2>Echipament</h2><p>Lansete spinning 1.8-2.4m, 1-10g (ultra-light). Mulinete 1000-2000. Fir 0.14-0.18mm. Waders impermeabili obligatorii. Cizme cu talpa anti-alunecare.</p><h2>Când Să Mergi</h2><p>Mai-iunie: sezonul de vârf, nivelul apei optim. Iulie-august: apa scade, pești concentrați în adâncituri. Septembrie: păstrăvii devin agresivi înainte de reproducere.</p><h2>Regulamente</h2><p>Permis de pescuit + taxă zonă montană obligatorii. Catch & release recomandat pentru conservare. Dimensiune minimă: 24 cm pentru păstrăv. Verificați perioadele de prohibiție!</p>',
            'reading_time': 6,
            'is_published': True,
            'is_featured': True,
            'published_date': timezone.now() - timedelta(days=63),
            'meta_description': 'Pescuit rauri munte Transilvania',
            'meta_keywords': 'pastrav, rauri munte, Transilvania'
        }
    )
    if created:
        articles_created += 1
        print(f"[OK] Articol creat: {article10.title}")

    # Articol 11: Tehnici
    article11, created = Article.objects.get_or_create(
        slug='pescuit-la-stiuca-primavara',
        defaults={
            'title': 'Pescuitul la Știucă Primăvara - Perioada de Aur',
            'category': cat_tehnici,
            'author': admin,
            'excerpt': 'Primăvara este cel mai bun sezon pentru știucă. Descoperiți unde, când și cum să prindeți știuci trofeu.',
            'content': '<h2>De Ce Primăvara?</h2><p>După reproducere (martie-aprilie), știuca devine extrem de agresivă. Trebuie să recupereze energia pierdută și atacă orice momeală!</p><h2>Locurile Câștigătoare</h2><p>Zone puțin adânci (0.5-2m) cu vegetație. Trestie, nuferi, iarbă scufundată. Apa se încălzește mai repede aici și concentrează peștișori - prada știucii.</p><h2>Momeli de Top</h2><p>Spinning: lingurite rotative 7-21g (Mepps, Blue Fox). Wobblere floating și suspending 7-12cm. Shad-uri moi pe jig-head 10-20g. Spinnerbait pentru zone cu vegetație.</p><h2>Tehnica</h2><p>Recuperare variată - alternați rapid și lent. Pauze de 2-3 secunde provoacă atacul. Aruncați cât mai aproape de vegetație. Știuca stă la pândă și atacă de aproape.</p><h2>Echipament</h2><p>Lansetă spinning 2.1-2.7m, 10-40g. Mulinetă 2500-3000. Fir braid 0.15-0.20mm + leader fluorocarbon 0.35mm sau titan.</p><h2>Sfat Important</h2><p>Folosiți ÎNTOTDEAUNA leader de titan sau fluorocarbon gros - știuca are dinți ascuțiți și taie firul normal instant!</p>',
            'reading_time': 5,
            'is_published': True,
            'published_date': timezone.now() - timedelta(days=70),
            'meta_description': 'Pescuit stiuca primavara',
            'meta_keywords': 'stiuca, spinning, primavara'
        }
    )
    if created:
        articles_created += 1
        print(f"[OK] Articol creat: {article11.title}")

    # Articol 12: Echipament
    article12, created = Article.objects.get_or_create(
        slug='cum-sa-alegi-firul-de-pescuit',
        defaults={
            'title': 'Cum Să Alegi Firul de Pescuit Potrivit - Ghid Complet',
            'category': cat_echip,
            'author': admin,
            'excerpt': 'Monofilament, fluorocarbon sau braid? Ghid detaliat pentru alegerea firului perfect în funcție de tipul de pescuit.',
            'content': '<h2>Tipuri de Fir</h2><p>Monofilament - cel mai popular, versatil, cu elasticitate. Fluorocarbon - invizibil în apă, rezistent la abraziune. Braid (împletit) - zero elasticitate, foarte rezistent, diametru mic.</p><h2>Monofilament</h2><p>Avantaje: ieftin, elastic (absoarbe șocurile), ușor de folosit. Dezavantaje: se uzează mai repede, vizibil în apă. Ideal pentru: începători, pescuit la crap, feeder. Diametre: 0.18-0.35mm pentru crap, 0.12-0.18mm pentru clean.</p><h2>Fluorocarbon</h2><p>Avantaje: practic invizibil, rezistent la UV și abraziune. Dezavantaje: scump, mai rigid. Ideal pentru: înaintas (leader), ape clare, pești precauți. Diametre: 0.20-0.40mm pentru leader.</p><h2>Braid</h2><p>Avantaje: foarte rezistent (10kg la diametru 0.15mm!), sensibilitate maximă, nu se întinde. Dezavantaje: vizibil în apă, se taie la obstacole ascuțite. Ideal pentru: spinning, pescuit la distanță, somn. Diametre: 0.10-0.20mm pentru spinning, 0.25-0.40mm pentru somn.</p><h2>Recomandări</h2><p>Crap: mono 0.28-0.35mm sau braid 0.18mm + leader fluoro 0.35mm. Clean/plătică: mono 0.14-0.18mm. Spinning știucă: braid 0.15mm + leader titan. Somn: braid 0.30-0.40mm + leader mono 0.70mm.</p>',
            'reading_time': 6,
            'is_published': True,
            'published_date': timezone.now() - timedelta(days=77),
            'meta_description': 'Ghid alegere fir pescuit',
            'meta_keywords': 'fir pescuit, monofilament, braid'
        }
    )
    if created:
        articles_created += 1
        print(f"[OK] Articol creat: {article12.title}")

    print(f"\n[OK] Total articole noi: {articles_created}")
    print(f"[OK] Total articole in baza: {Article.objects.count()}")

if __name__ == '__main__':
    main()
