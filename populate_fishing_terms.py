#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to populate fishing dictionary with relevant terms
Adds ~70 fishing-related terms across all categories
"""
import os
import sys
import django

if __name__ == "__main__":
    # Fix pentru encoding Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
from django.conf import settings
if not settings.configured:
    django.setup()

from django.utils.text import slugify
from main.models import FishingTerm

# Comprehensive fishing terms database
FISHING_TERMS = [
    # EQUIPMENT TERMS (Echipamente)
    {
        'term': 'Lanseta',
        'category': 'equipment',
        'definition': 'Instrument lung și flexibil folosit pentru aruncarea momelii și prinderea peștilor. Lanseta are o lungime și o acțiune specifice în funcție de tipul de pescuit (carp fishing, feeder, spinning, etc.).',
        'example_usage': 'Pentru pescuitul la crap, se recomandă o lanseta de 12-13 ft (feet) cu acțiune medium-fast.'
    },
    {
        'term': 'Mulineta',
        'category': 'equipment',
        'definition': 'Dispozitiv mecanic montat pe lanseta, care permite înfășurarea și derularea firului de pescuit. Există mai multe tipuri: cu tambur fix, cu tambur rotativ (baitcasting), și cu tambur deschis.',
        'example_usage': 'O mulinetă cu tambur fix mărimea 6000 este ideală pentru pescuitul la crap în lacuri mari.'
    },
    {
        'term': 'Feeder',
        'category': 'equipment',
        'definition': 'Metodă de pescuit care folosește un coș special (feeder) umplut cu nadă, care eliberează treptat hrana pentru a atrage peștii în apropierea cârligului. De asemenea, denumește și lanseta specializată pentru această tehnică.',
        'example_usage': 'Pescuitul la feeder este foarte eficient pentru plătică, caras și crap în apele stătătoare.'
    },
    {
        'term': 'Rod Pod',
        'category': 'equipment',
        'definition': 'Suport metalic independent pentru lansete, folosit în special în pescuitul la carp. Permite montarea simultană a 2-4 lansete într-o configurație stabilă, cu avertizoare și swingere.',
        'example_usage': 'Rod pod-ul este esențial pentru pescuitul la crap pe sesiuni lungi, oferind stabilitate în orice teren.'
    },
    {
        'term': 'Swinger',
        'category': 'equipment',
        'definition': 'Indicator mecanic de atac, montat între lanseta și rod pod. Se mișcă în sus la atac, semnalizând muș catura. Poate fi iluminat pentru pescuitul nocturn.',
        'example_usage': 'Swinger-ul s-a ridicat brusc, semnalând un atac puternic de crap.'
    },
    {
        'term': 'Avertizor electronic',
        'category': 'equipment',
        'definition': 'Dispozitiv electronic care emite un sunet și/sau lumină când detectează mișcarea firului la atac. Indispensabil în pescuitul modern la crap.',
        'example_usage': 'Avertizorul electronic a sunat în miezul nopții, anunțând o captură mare.'
    },
    {
        'term': 'Epuisette',
        'category': 'equipment',
        'definition': 'Plasă mare pe cadru metalic cu mâner lung, folosită pentru ridicarea peștelui din apă fără a-l răni. Esențială pentru pescuitul catch & release.',
        'example_usage': 'Folosește întotdeauna epuisette pentru a scoate peștele din apă, evitând să-l rănești.'
    },
    {
        'term': 'Boilies',
        'category': 'equipment',
        'definition': 'Momeală sferică făcută din făină, ouă și diverse arome, fierută și uscată. Standard în pescuitul modern la crap. Disponibile în diametre de 10-24 mm și numeroase arome.',
        'example_usage': 'Am prins un crap de 12 kg folosind boilies cu aromă de strawberry de 20 mm.'
    },
    {
        'term': 'Pelete',
        'category': 'equipment',
        'definition': 'Boabe cilindrice comprimate din făină de pește, cereale și uleiuri, folosite ca nadă sau momeală. Foarte atractive pentru crap, somn, și alte specii de fund.',
        'example_usage': 'Peletele de halibut sunt extrem de eficiente ca nadă pentru crap în apele reci.'
    },
    {
        'term': 'Hair Rig',
        'category': 'equipment',
        'definition': 'Montaj în care momeala (boilie) este prinsă pe un fir subțire ("păr") legat de cârlig, permițând peștelui să înghită momeala fără să simtă cârligul.',
        'example_usage': 'Hair rig-ul a revoluționat pescuitul la crap, crescând dramatic rata de capturi.'
    },
    {
        'term': 'Cârlig',
        'category': 'equipment',
        'definition': 'Instrument metalic curbat cu vârf ascuțit, folosit pentru prinderea peștelui. Mărimile variază de la nr. 24 (foarte mic) la 1/0, 2/0 (foarte mare). Tipuri: wide gape, curved, circle hook.',
        'example_usage': 'Pentru pescuitul la crap folosesc cârlige wide gape mărimea 4-6, pentru prindere sigură.'
    },
    {
        'term': 'Plumb',
        'category': 'equipment',
        'definition': 'Greutate metalică (din plumb sau alte materiale) care permite scufundarea momelii la adâncimea dorită și menținerea ei pe fund.',
        'example_usage': 'În curent puternic, am folosit un plumb de 120 g pentru a menține montajul pe loc.'
    },
    {
        'term': 'Buzz Bar',
        'category': 'equipment',
        'definition': 'Bara orizontală metalică montată pe rod pod, pe care se fixează avertizoarele electronice. Permite o organizare ordonată a echipamentului.',
        'example_usage': 'Buzz bar-ul frontal suportă trei avertizoare, câte unul pentru fiecare lanseta.'
    },
    {
        'term': 'Matză',
        'category': 'equipment',
        'definition': 'Saltea sau pat gonflabil special conceput pentru pescari, oferind confort în timpul sesiunilor lungi de pescuit. Indispensabilă pentru pescuitul nocturn.',
        'example_usage': 'După o noapte pe matză lângă apă, pescuitul devine o adevărată aventură.'
    },
    {
        'term': 'Bivvy',
        'category': 'equipment',
        'definition': 'Cort special pentru pescari, cu deschidere frontală largă care permite monitorizarea lansetelordin interior. Protecție împotriva vremii în sesiuni lungi.',
        'example_usage': 'Bivvy-ul mă protejează de ploaie și vânt în timpul sesiunilor de carp fishing.'
    },

    # TECHNIQUES TERMS (Tehnici)
    {
        'term': 'Feeder Fishing',
        'category': 'techniques',
        'definition': 'Tehnică de pescuit care folosește un coș (feeder) umplut cu nadă, care atrage peștii în zona cârligului. Foarte eficientă pentru specii de fund.',
        'example_usage': 'Feeder fishing este tehnica mea preferată pentru pescuitul plăticii în Dunăre.'
    },
    {
        'term': 'Carp Fishing',
        'category': 'techniques',
        'definition': 'Pescuit sportiv specializat pentru captura crapului, folosind echipament și tehnici specifice: lansete lungi, boilies, montaje speciale (hair rig, chod rig).',
        'example_usage': 'Carp fishing în România a devenit extrem de popular, cu lacuri specializate în toată țara.'
    },
    {
        'term': 'Spinning',
        'category': 'techniques',
        'definition': 'Tehnică activă de pescuit pentru prădători, în care pescarul aruncă și recuperează continuu momeli artificiale (linguriță, wobbler, shad) pentru a simula pești vii.',
        'example_usage': 'Spinning-ul pentru știucă este cel mai dinamic și spectaculos stil de pescuit.'
    },
    {
        'term': 'Jigging',
        'category': 'techniques',
        'definition': 'Tehnică verticală de pescuit pentru prădători, în care momeala (jig) este mișcată în sus-jos pentru a atrage peștele. Foarte eficientă pentru clean și somn.',
        'example_usage': 'Jigging vertical de pe barcă mi-a adus cei mai mari cleani din lacul de acumulare.'
    },
    {
        'term': 'Trolling',
        'category': 'techniques',
        'definition': 'Tehnică de pescuit în care momeala este trase în spatele unei bărci în mișcare lentă, acoperind zone mari de apă pentru găsirea peștilor prădători.',
        'example_usage': 'Trolling-ul în lacurile mari este eficient pentru localizarea bancurilor de clean.'
    },
    {
        'term': 'Drop Shot',
        'category': 'techniques',
        'definition': 'Montaj în care cârligul este legat pe firul principal, iar plumbul atârnă la capătul firului. Permite menținerea momelii la o înălțime constantă față de fund.',
        'example_usage': 'Drop shot cu shad mic este devastator pentru biban în zonele cu vegetație.'
    },
    {
        'term': 'Method Feeder',
        'category': 'techniques',
        'definition': 'Variant de feeder care folosește un coș special în formă de racoletă, pe care se modelează nadă compactă. Momeala este îngropată în nadă, iar peștele o găsește în timpul hrănirii.',
        'example_usage': 'Method feeder cu porumb și pellets a dat rezultate excelente la crap.'
    },
    {
        'term': 'Chod Rig',
        'category': 'techniques',
        'definition': 'Montaj special pentru carp fishing, în care momeala plutește deasupra fundului acoperit cu nămol sau vegetație, prezentând-o într-un mod extrem de natural.',
        'example_usage': 'Chod rig-ul este perfect pentru lacurile cu fund mâlos unde alte montaje se înfundă.'
    },
    {
        'term': 'Spodding',
        'category': 'techniques',
        'definition': 'Tehnică de momire la distanță mare folosind o rachetă specială (spod) care se umple cu boilies și pellets, aruncându-le precis în zona de pescuit.',
        'example_usage': 'Spodding-ul îmi permite să momesc la 100-120 metri distanță cu precizie.'
    },
    {
        'term': 'PVA Bag',
        'category': 'techniques',
        'definition': 'Săculeț solubil în apă (PVA) umplut cu pellets, boilies măcinate și momeală, care se dizolvă la contactul cu apa creând un nor atractiv de hrană.',
        'example_usage': 'PVA bag-ul asigură că momeala ajunge pe fund exact înconjurată de hrană.'
    },
    {
        'term': 'Fly Fishing',
        'category': 'techniques',
        'definition': 'Tehnică sofisticată de pescuit folosind momeli artificiale ultra-ușoare (muște) și echipament specializat. Standard pentru pescuitul păstrăvului în râuri montane.',
        'example_usage': 'Fly fishing pentru păstrăv în râurile Carpaților este o artă ce necesită ani de practică.'
    },

    # REGULATIONS TERMS (Regulamente)
    {
        'term': 'Catch & Release',
        'category': 'regulations',
        'definition': 'Practică de pescuit în care peștele capturat este eliberat imediat înapoi în apă, fără rănire. Promovează conservarea resurselor piscicole și practicile etice de pescuit.',
        'example_usage': 'În lacurile de carp fishing, catch & release este obligatoriu pentru protejarea stocului de pește.'
    },
    {
        'term': 'Dimensiune minimă',
        'category': 'regulations',
        'definition': 'Lungimea minimă legală la care un pește poate fi păstrat. Peștii sub această dimensiune trebuie eliberați pentru a permite reproducerea.',
        'example_usage': 'Dimensiunea minimă pentru știucă este 40 cm - exemplarele mai mici trebuie eliberate.'
    },
    {
        'term': 'Perioadă de prohibiție',
        'category': 'regulations',
        'definition': 'Interval de timp în care pescuitul unei anumite specii este interzis, de obicei în perioada de reproducere, pentru protejarea stocurilor.',
        'example_usage': 'Perioada de prohibiție pentru știucă este 15 februarie - 30 aprilie.'
    },
    {
        'term': 'Licență de pescuit',
        'category': 'regulations',
        'definition': 'Autorizație oficială necesară pentru practicarea pescuitului recreativ sau sportiv, emisă de autoritățile competente după plata taxei legale.',
        'example_usage': 'Este obligatoriu să ai licență de pescuit valabilă când pescuiești în ape publice.'
    },
    {
        'term': 'Cotă de captură',
        'category': 'regulations',
        'definition': 'Cantitatea maximă de pește care poate fi păstrată într-o zi de pescuit, stabilită prin regulament pentru fiecare specie și zonă de pescuit.',
        'example_usage': 'Cota zilnică pentru clean este 2 exemplare pe pescar în majoritatea apelor.'
    },
    {
        'term': 'Pescuit recreativ',
        'category': 'regulations',
        'definition': 'Pescuit practicat ca activitate de agrement, nu în scop comercial, cu respectarea reglementărilor și cotelor stabilite pentru fiecare specie.',
        'example_usage': 'Pescuitul recreativ necesită licență valabilă și respectarea tuturor regulamentelor locale.'
    },
    {
        'term': 'Pescuit sportiv',
        'category': 'regulations',
        'definition': 'Formă de pescuit competițională sau de performanță, desfășurată conform regulilor sportive, adesea în cadrul concursurilor organizate.',
        'example_usage': 'Pescuitul sportiv la crap implică competiții pe multiple zile cu reguli stricte.'
    },
    {
        'term': 'Specie protejată',
        'category': 'regulations',
        'definition': 'Specie de pește a cărei captură este restricționată sau interzisă complet datorită statusului de conservare vulnerabil sau în pericol.',
        'example_usage': 'Sturionul este specie strict protejată - pescuitul este interzis complet.'
    },

    # GENERAL TERMS (Termeni Generali)
    {
        'term': 'Momeală',
        'category': 'general',
        'definition': 'Substanță sau obiect fixat pe cârlig pentru a atrage și prinde peștele. Poate fi naturală (vierme, porumb) sau artificială (wobbler, linguriță).',
        'example_usage': 'Vierele roșu este o momeală universală pentru majoritatea speciilor de pești.'
    },
    {
        'term': 'Nadă',
        'category': 'general',
        'definition': 'Amestec de substanțe aromate folosit pentru a atrage peștii în zona de pescuit. Se aruncă în apă înainte și în timpul pescuitului pentru a crea un nor atractiv.',
        'example_usage': 'Nada din pesmet, biscuiți și aromă de vanilie atrage eficient plătica și carasul.'
    },
    {
        'term': 'Eschă',
        'category': 'general',
        'definition': 'Termen generic pentru orice tip de momeală folosită în pescuit, fie naturală (vierme, pește viu), fie artificială.',
        'example_usage': 'Alegerea eschetei potrivite este esențială pentru succesul pescuitului.'
    },
    {
        'term': 'Captură',
        'category': 'general',
        'definition': 'Peștele prins în urma activității de pescuit. Poate fi păstrat (în limitele legale) sau eliberat (catch & release).',
        'example_usage': 'Captura zilei a fost un crap oglindă de 8 kg, eliberat după fotografiere.'
    },
    {
        'term': 'Atac',
        'category': 'general',
        'definition': 'Momentul în care peștele mușcă din momeală, semnalizat prin mișcarea plutei, tensionarea firului sau sunetul avertizorului.',
        'example_usage': 'Atacul crapului a fost violent - swinger-ul s-a ridicat instant și avertizorul a început să sune.'
    },
    {
        'term': 'Groundbait',
        'category': 'general',
        'definition': 'Termen englezesc pentru nadă, amestec de substanțe folosit pentru atragerea peștelui. În România se folosește termenul "nadă".',
        'example_usage': 'Groundbait-ul special pentru crap conține boilies măcinate, pellets și arome puternice.'
    },
    {
        'term': 'Linguriță rotativă',
        'category': 'general',
        'definition': 'Momeală artificială metalică cu paletă care se rotește în timpul recuperării, creând vibrații și reflexii care atrag peștii prădători.',
        'example_usage': 'Linguriță rotativă argintie nr. 3 este ideală pentru clean și știucă în apele clare.'
    },
    {
        'term': 'Wobbler',
        'category': 'general',
        'definition': 'Momeală artificială în formă de pește, fabricată din plastic sau lemn, care imită mișcarea unui pește viu prin oscilații laterale.',
        'example_usage': 'Wobbler-ul cu aromă de firetiger este devastator pentru știucă în timpul verii.'
    },
    {
        'term': 'Shad',
        'category': 'general',
        'definition': 'Momeală artificială din silicon sau plastic moale, în formă de pește, montată pe cap jig. Foarte versatilă pentru pescuitul prădătorilor.',
        'example_usage': 'Shad-ul de 12 cm în culoare motoroil este preferatul meu pentru clean.'
    },
    {
        'term': 'Twister',
        'category': 'general',
        'definition': 'Momeală din silicon cu corpul alungit și codiță curbată care vibrează în apă, imitând mișcarea unui vierme sau larvă.',
        'example_usage': 'Twister-ul galben este irezistibil pentru biban în apele tulburi.'
    },
    {
        'term': 'Plută',
        'category': 'general',
        'definition': 'Indicator plutitor fixat pe fir care semnalizează atacul peștelui prin scufundare sau deplasare laterală. Disponibilă în diverse forme și greutăți.',
        'example_usage': 'Pluta sensibilă de 1 gram este perfectă pentru pescuitul fin la roșioară.'
    },
    {
        'term': 'Undița',
        'category': 'general',
        'definition': 'Modalitate tradițională de pescuit folosind o prăjină simplă (fără mulinetă) cu fir fix și plută. Prima metodă învățată de majoritatea pescarilor.',
        'example_usage': 'Am învățat să pescuiesc cu undița când aveam 7 ani, prinzând caraș și roșioară.'
    },
    {
        'term': 'Lipan',
        'category': 'general',
        'definition': 'Larvă de insectă acvatică folosită ca momeală naturală pentru pești de dimensiuni mici și medii. Foarte eficientă la undiță și feeder.',
        'example_usage': 'Lipanul este momeala preferată pentru caras, roșioară și plătică.'
    },
    {
        'term': 'Vierme roșu',
        'category': 'general',
        'definition': 'Momeală naturală clasică, universal valabilă pentru aproape toate speciile de pești. Se găsește în solul umed sau se achiziționează din magazine.',
        'example_usage': 'Viermele roșu a fost și rămâne cea mai sigură momeală pentru pescuitul la undiță.'
    },
    {
        'term': 'Porumb fiert',
        'category': 'general',
        'definition': 'Boabe de porumb fierte și aromate, una dintre cele mai eficiente și economice momeli pentru crap, amur și alte specii de fund.',
        'example_usage': 'Porumbul fiert cu aromă dulce este momeala mea standard pentru crap.'
    },
    {
        'term': 'Crap oglindă',
        'category': 'general',
        'definition': 'Varietate de crap caracterizată prin solzi mari și rari, dispuși neregulat pe corp. Foarte căutat de pescarii sportivi datorită aspectului spectacular.',
        'example_usage': 'Am prins un crap oglindă superb de 15 kg - cel mai frumos pește din cariera mea.'
    },
    {
        'term': 'Crap salopetă',
        'category': 'general',
        'definition': 'Varietate de crap cu solzi dispuși doar pe o bandă de-a lungul liniei laterale și pe spate, restul corpului fiind fără solzi.',
        'example_usage': 'Crapul salopetă este mai rar întâlnit decât crapul oglindă, dar la fel de spectaculos.'
    },
    {
        'term': 'Sesiune',
        'category': 'general',
        'definition': 'Perioadă de pescuit planificată, de obicei de minimum 12-24 ore (overnight) până la mai multe zile, în care pescarul rămâne lângă apă.',
        'example_usage': 'Sesiunea de weekend în Delta a fost fabuloasă - 5 crapi peste 10 kg.'
    },
    {
        'term': 'Spot',
        'category': 'general',
        'definition': 'Locație specifică în apă unde se aruncă momeala, aleasă strategic pentru maximizarea șanselor de captură. De obicei momită anterior.',
        'example_usage': 'Spot-ul meu secret de crap este lângă o groapă la 60 metri de mal.'
    },
    {
        'term': 'Run',
        'category': 'general',
        'definition': 'Englezism pentru "fuga" peștelui după muș care - momentul de panică când crapul sau alt pește mare începe să tragă violent firul.',
        'example_usage': 'Run-ul a fost atât de puternic încât a luat 50 metri de fir înainte să-l pot opri.'
    },
    {
        'term': 'Marker float',
        'category': 'general',
        'definition': 'Plutitor special folosit pentru măsurarea adâncimii și marcarea spot-urilor de pescuit la distanță mare. Esențial în carp fishing.',
        'example_usage': 'Cu marker float-ul am găsit o groapă perfectă la 80 metri - spot ideal pentru crap.'
    },
    {
        'term': 'Bite alarm',
        'category': 'general',
        'definition': 'Termen englezesc pentru avertizor electronic - dispozitiv care semnalizează atacul prin sunet și lumină.',
        'example_usage': 'Bite alarm-ul meu are sensibilitate reglabilă și LED-uri colorate pentru pescuitul nocturn.'
    },

    # SPECIES-RELATED TERMS
    {
        'term': 'Cyprinide',
        'category': 'species',
        'definition': 'Familie de pești de apă dulce care include crapul, carasul, roșioara, plătica și alte specii. Caracteristici: corp acoperit de solzi, lipsa dinților pe maxilare.',
        'example_usage': 'Ciprinidele reprezintă majoritatea speciilor pescuite în apele dulci din România.'
    },
    {
        'term': 'Prădător',
        'category': 'species',
        'definition': 'Pește carnin care se hrănește cu alte pești sau animale acvatice. Include știuca, cleanul, somnul, bibanul. Pescuitul necesită momeli care imită pești vii.',
        'example_usage': 'Prădătorii sunt cei mai spectaculoși pești de prins - atacurile sunt violente și dinamice.'
    },
    {
        'term': 'Pești de fund',
        'category': 'species',
        'definition': 'Specii care caută hrana pe fundul apei: crap, caras, somn, mreană. Pescuitul se face cu montaje de fund și momeli care ajung la adâncime.',
        'example_usage': 'Peștii de fund sunt cei mai receptivi la momire - nada creează un nor atractiv pe fund.'
    },
    {
        'term': 'Pești de suprafață',
        'category': 'species',
        'definition': 'Specii care se hrănesc la suprafața apei sau în straturile superioare: obleț, avat, clean (în anumite condiții).',
        'example_usage': 'Peștii de suprafață atacă violent topwater lures în timpul verii.'
    },
    {
        'term': 'Biban țăruș',
        'category': 'species',
        'definition': 'Termen popular pentru bibanul european (Perca fluviatilis), datorită spinilor ascuțiți de pe înotătoarea dorsală care seamănă cu țăruși.',
        'example_usage': 'Ai grijă când prinzi bibanul țăruș - spinii pot înțepa dureros.'
    },

    # SEASONAL & CONDITIONS
    {
        'term': 'Sezon de vară',
        'category': 'general',
        'definition': 'Perioada caldă (iunie-august) când peștii sunt foarte activi, metabolismul este accelerat și atacurile sunt frecvente. Ideal pentru majoritatea speciilor.',
        'example_usage': 'Sezonul de vară este ideal pentru carp fishing - peștii sunt activi 24/7.'
    },
    {
        'term': 'Pescuit nocturn',
        'category': 'general',
        'definition': 'Pescuit practicat noaptea, când mulți pești prădători (clean, somn) și ciprinide mari (crap) sunt mai activi. Necesită echipament special: frontale, lumini chimice.',
        'example_usage': 'Pescuitul nocturn de somn cu clonc este o experiență de neuitat - atacurile sunt brutale.'
    },
]

def populate_terms():
    """Populate fishing terms dictionary"""
    print("=" * 80)
    print("POPULARE DICȚIONAR TERMENI DE PESCUIT")
    print("=" * 80)
    print()

    created_count = 0
    exists_count = 0
    error_count = 0

    category_counts = {
        'equipment': 0,
        'techniques': 0,
        'regulations': 0,
        'general': 0,
        'species': 0
    }

    print(f"[1/1] Procesez {len(FISHING_TERMS)} termeni...")
    print("-" * 80)

    for term_data in FISHING_TERMS:
        try:
            # Check if term already exists
            existing = FishingTerm.objects.filter(term__iexact=term_data['term']).first()

            if existing:
                print(f"○ Există: {term_data['term']}")
                exists_count += 1
                continue

            # Create slug
            slug = slugify(term_data['term'])

            # Ensure unique slug
            base_slug = slug
            counter = 1
            while FishingTerm.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            # Create term
            term = FishingTerm.objects.create(
                term=term_data['term'],
                slug=slug,
                definition=term_data['definition'],
                category=term_data['category'],
                example_usage=term_data.get('example_usage', ''),
                is_active=True
            )

            print(f"✓ Creat: {term_data['term']} ({term_data['category']})")
            created_count += 1
            category_counts[term_data['category']] += 1

        except Exception as e:
            print(f"✗ Eroare la {term_data['term']}: {str(e)}")
            error_count += 1

    print("-" * 80)
    print()

    # Final statistics
    print("=" * 80)
    print("STATISTICI FINALE")
    print("=" * 80)
    print(f"✓ Termeni creați:    {created_count}")
    print(f"○ Termeni existenți: {exists_count}")
    print(f"✗ Erori:             {error_count}")
    print(f"─ Total procesați:   {len(FISHING_TERMS)}")
    print()
    print("DISTRIBUȚIE PE CATEGORII:")
    print(f"  • Echipamente:     {category_counts['equipment']} termeni")
    print(f"  • Tehnici:         {category_counts['techniques']} termeni")
    print(f"  • Regulamente:     {category_counts['regulations']} termeni")
    print(f"  • Termeni generali: {category_counts['general']} termeni")
    print(f"  • Specii:          {category_counts['species']} termeni")
    print("=" * 80)
    print()

    if created_count > 0:
        print("✓ Dicționarul a fost populat cu succes!")
        print("Pagina /dictionar-pescuit/ acum conține termeni relevanți.")
    print()

if __name__ == '__main__':
    populate_terms()
