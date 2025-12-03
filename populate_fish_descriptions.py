#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to populate fish species descriptions in the database
Adds detailed information for all 23 species
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

from main.models import FishSpecies

# Comprehensive fish species data
FISH_DATA = {
    'Amur': {
        'detailed_description': 'Amurul (Ctenopharyngodon idella) este un pește fitofag originar din China, introdus în România pentru combaterea vegetației acvatice. Are corpul alungit, solzi mari și lucios, colorație verzui-argintie pe spate și alb-argintie pe abdomen. Este un pește foarte rezistent și cu creștere rapidă.',
        'habitat': 'Preferă apele calme și calde ale lacurilor de acumulare și bălților. Se adaptează bine în ape stătătoare cu vegetație abundentă. Tolerează temperaturi ridicate ale apei și conținut scăzut de oxigen.',
        'fishing_techniques': 'Pescuitul la amur se practică cu lanseta la feeder sau cu undiță de fund. Montajul hair rig este foarte eficient. Se recomandă folosirea unui avertizor electronic deoarece atacurile pot fi bruște și violente.',
        'best_baits': 'Porumb fiert, boilies, paste vegetale, pâine, fire de iarbă. Este atras de aromele dulci și fructate. Porumbul este cea mai populară momeală.',
        'legal_info': 'Dimensiune minimă de captură: 40 cm. Nu există perioadă de prohibiție. Se poate păstra în anumite limite stabilite de regulamentele locale.',
        'average_size': '50-80 cm, 3-8 kg',
        'max_size': '120 cm, 40 kg'
    },
    'Avat': {
        'detailed_description': 'Avatul (Aspius aspius) este un pește prădător din familia ciprinidelor, cu corp alungit fusiform, gură mare orientată în sus. Are colorație argintie strălucitoare, înotătoare roșcate. Este un prădător agresiv care vânează în bancuri.',
        'habitat': 'Preferă apele deschise ale râurilor mari și lacurilor de acumulare. Se găsește în zonele cu curent moderat, la suprafața apei sau în straturile mijlocii. Frecvent în zonele cu bancuri de pești mici.',
        'fishing_techniques': 'Pescuitul la spinning cu momeli artificiale (linguriță, wobbler, shad). Tehnica casting și retrieving rapidă. Foarte eficient pescuitul de suprafață în timpul verii.',
        'best_baits': 'Linguriță rotativă, wobbler, momeli de suprafață (popper), shad-uri, twister. Pește viu pentru pescuitul la plutitor. Preferă momelilenelele care imită pești mici.',
        'legal_info': 'Dimensiune minimă: 40 cm. Prohibiție: 1 aprilie - 31 mai. Specie protejată în unele zone.',
        'average_size': '40-60 cm, 1-3 kg',
        'max_size': '120 cm, 12 kg'
    },
    'Babușcă': {
        'detailed_description': 'Babușca (Barbus barbus) este un ciprinid de apă curgătoare, cu corp alungit, botul prelungit cu 4 mustăți. Are colorație brun-verzuie pe spate și alb-gălbuie pe abdomen. Pește de bancuri care caută hrana pe fund.',
        'habitat': 'Specific râurilor cu curent moderat până la puternic, fund pietros sau nisipos. Preferă zonele cu oxigen abundant. Se găsește în băltile râurilor, la vărsarea afluentelor.',
        'fishing_techniques': 'Pescuit la feeder sau cu undiță simplă de fund. Montaj cu plumb culisant. Nada abundentă este esențială. Momirea locului se face cu nadă fină.',
        'best_baits': 'Vierme, mălai, cârnaț, caise, brânză, paste. Nadă din fulgi de ovăz, pesmet, mălai.',
        'legal_info': 'Dimensiune minimă: 25 cm. Prohibiție: 15 aprilie - 15 iunie în unele râuri.',
        'average_size': '30-40 cm, 0.5-1.5 kg',
        'max_size': '90 cm, 12 kg'
    },
    'Biban': {
        'detailed_description': 'Bibanul (Perca fluviatilis) este un pește prădător recognoscibil după dungile verticale închise pe corp și înotătoarele roșii. Are spinii ascuțiți pe înotătoarea dorsală. Foarte răspândit în apele României.',
        'habitat': 'Se adaptează ușor la diverse tipuri de ape: râuri, lacuri, bălți. Preferă zonele cu vegetație, piloni, trunchiuri scufundate. Activ în special dimineața și seara.',
        'fishing_techniques': 'Pescuit la spinning cu momeli mici artificiale, drop-shot, jigging vertical. Eficient și pescuitul la pluta vie cu pește mic. Tehnica Carolina rig pentru zona litorală.',
        'best_baits': 'Twister mic, shad 5-7 cm, linguriță rotativă nr. 0-2, vierme, pește viu mic. Culori: alb, galben, portocaliu.',
        'legal_info': 'Dimensiune minimă: 10 cm. Nu există prohibiție. Cotă: 10 kg/zi în unele ape.',
        'average_size': '15-25 cm, 50-200 g',
        'max_size': '50 cm, 3 kg'
    },
    'Boarță': {
        'detailed_description': 'Boarța (Abramis bjoerkna) seamănă cu plătica dar este mai mică și are corpul mai înalt. Colorație argintie, înotătoare cenușii. Pește de banc care trăiește în ape stătătoare.',
        'habitat': 'Lacuri, bălți, râuri cu curent lent. Preferă zonele cu vegetație, fundul moale cu mâl. Se găsește în bancuri numeroase la diferite adâncimi.',
        'fishing_techniques': 'Pescuit la undiță simplă cu plută sau cu elastic. Montaj fin, cârlig mic nr. 14-18. Momire cu nadă fină.',
        'best_baits': 'Vierme roșu, colorat, cașcaval, paste, lipan. Nadă din pesmet, biscuiți, mălai.',
        'legal_info': 'Nu există restricții de dimensiune sau prohibiție. Pescuit liber.',
        'average_size': '15-20 cm, 50-150 g',
        'max_size': '35 cm, 800 g'
    },
    'Caras': {
        'detailed_description': 'Carasul (Carassius carassius) este un pește foarte rezistent, cu corp înalt și comprimat lateral. Colorație variabilă: aurie, argintie sau închisă. Nu are mustăți. Supraviețuiește în condiții extreme de temperatură și oxigen.',
        'habitat': 'Bălți, iazuri, lacuri cu fund mâlos și vegetație abundentă. Rezistă la îngheț și secetă. Se adaptează în ape cu oxigen redus unde alte specii nu supraviețuiesc.',
        'fishing_techniques': 'Pescuit la undiță cu plută, feeder ușor. Momire abundentă a locului. Atacuri lente, necesită răbdare. Plutăprecisă și sensibilă.',
        'best_baits': 'Vierme, porumb, lipan, coceni, paste dulci. Nadă cu aromă dulce: vanilie, căpșuni.',
        'legal_info': 'Nu există restricții speciale. Dimensiune recomandată: 15 cm.',
        'average_size': '15-25 cm, 200-500 g',
        'max_size': '50 cm, 3 kg'
    },
    'Caras argintiu': {
        'detailed_description': 'Carasul argintiu (Carassius gibelio) este o specie invazivă, foarte prolifică, cu corp mai alungit decât carasul comun. Colorație argintie strălucitoare. Se reproduce partenogenetic (fără masculi).',
        'habitat': 'Se adaptează la orice tip de apă: râuri, lacuri, bălți, canale. Extrem de rezistent, colonizează rapid noi habitate. Concurează și elimină alte specii.',
        'fishing_techniques': 'Similar cu carasul comun: undiță cu plută, feeder. Se prinde ușor, atacuri repetate. Montaj simplu cu plută fixă sau glisantă.',
        'best_baits': 'Vierme, porumb, lipan, paste. Acceptă aproape orice momeală de origine vegetală sau animală.',
        'legal_info': 'Specie invazivă, fără restricții de captură. Se recomandă prelevarea din mediu.',
        'average_size': '15-20 cm, 200-400 g',
        'max_size': '45 cm, 3 kg'
    },
    'Clean': {
        'detailed_description': 'Cleanul (Sander lucioperca) este un pește prădător valoros, cu corp alungit, colorație verzui-gri cu dungi verticale închise. Are dinți canini dezvoltați. Prădător nocturn foarte apreciat de pescari.',
        'habitat': 'Lacuri de acumulare, râuri mari, zone adânci cu fund nisipos sau pietros. Preferă apele limpezi și reci. Activ în special noaptea și în zori.',
        'fishing_techniques': 'Pescuit la spinning cu shad, twister, wobbler. Jigging vertical foarte eficient. Pescuit la pluta vie cu pește viu. Trolling în lacuri mari.',
        'best_baits': 'Shad 8-12 cm, twister, wobbler, pește viu (clean mic, bibanțică). Culori: alb, galben, portocaliu. Noaptea: fosforescente.',
        'legal_info': 'Dimensiune minimă: 40 cm (variază pe ape). Prohibiție: 1 aprilie - 31 mai. Cotă: 2-5 exemplare/zi.',
        'average_size': '40-60 cm, 1-3 kg',
        'max_size': '130 cm, 20 kg'
    },
    'Crap': {
        'detailed_description': 'Crapul (Cyprinus carpio) este cel mai pescuit pește în România, cu corp masiv acoperit de solzi mari. Există trei varietăți: crap comun (complet solzos), crap oglindă (solzi mari rari), crap salopetă (solzi doar pe linie). Are 4 mustăți.',
        'habitat': 'Lacuri, bălți, râuri cu curent lent, fund mâlos. Preferă zonele cu vegetație, adâncimi de 2-5 m. Se deplasează pe trasee fixe în căutarea hranei.',
        'fishing_techniques': 'Pescuit sportiv la crap cu echipament specializat: lansete carp de 12-13 ft, mulinetă cu fir gros, avertizoare electronice. Montaje: hair rig, chod rig, ronnie rig. Momire cu boilies, pelete, porumb.',
        'best_baits': 'Boilies (10-24 mm) în diverse arome, porumb fiert, pelete, tigernuts, paste. PVA stick sau PVA bag. Nadă: boilies măcinate, pelete, porumb.',
        'legal_info': 'Dimensiune minimă: 35-40 cm (variază). Nu există prohibiție generală. Multe lacuri practică catch & release obligatoriu.',
        'average_size': '40-60 cm, 2-5 kg',
        'max_size': '120 cm, 40 kg'
    },
    'Fitofag': {
        'detailed_description': 'Fitofagul este denumirea colectivă pentru peștii care se hrănesc predominant cu vegetație: amur, cosaș, babuță de Mureș. În România, termenul se referă în principal la amur și la alte specii erbivore introduse.',
        'habitat': 'Ape stătătoare sau cu curent lent, cu vegetație abundentă. Lacuri de acumulare, bălți amenajate special. Zone eutrofizate cu exces de vegetație acvatică.',
        'fishing_techniques': 'Metode similare cu pescuitul la crap: feeder, undiță de fund cu avertizor. Montaje speciale pentru momeli vegetale. Momire cu iarbă proaspătă.',
        'best_baits': 'Porumb, firăde iarbă, boilies vegetale, paste cu aromă de iarbă, lăturaș. Nadă din ovăz, porumb măcinat.',
        'legal_info': 'Restricții similare cu amurul. Dimensiune minimă: 40 cm pentru amur. Fără prohibiție.',
        'average_size': '50-70 cm, 3-7 kg',
        'max_size': '120 cm, 40 kg'
    },
    'Linul': {
        'detailed_description': 'Linul (Tinca tinca) are corp compact, acoperit cu un strat protector de mucus, colorație verzuie-măslinie închisă. Are o singură pereche de mustăți scurte. Pește de fund, rezistent la temperaturi scăzute.',
        'habitat': 'Bălți, lacuri, râuri cu curent foarte lent, preferă fundul mâlos cu vegetație. Activ în special dimineața devreme și seara. Hibernează în mâl.',
        'fishing_techniques': 'Pescuit la undiță de fund cu plută sau feeder ușor. Montaj fin, cârlig nr. 8-12. Momire cu nadă fină pe fundul mâlos. Atacuri lente și precaute.',
        'best_baits': 'Vierme roșu, greier, lipan, porumb, paste. Nadă din pesmet, biscuiți, aromă de scorțișoară sau vanilie.',
        'legal_info': 'Dimensiune minimă: 20 cm în unele ape. Nu există prohibiție generală.',
        'average_size': '25-35 cm, 500 g - 1 kg',
        'max_size': '70 cm, 7.5 kg'
    },
    'Mreană': {
        'detailed_description': 'Mreana (Barbus meridionalis) este un ciprinid de râu, cu corp alungit, botușal proeminentcu 4 mustăți. Colorație verzui-brun cu pete închise pe corp. Pește de bancuri care caută hrana pe fund.',
        'habitat': 'Râuri cu curent moderat până la puternic, apă rece și oxigenată. Preferă fundul pietros sau nisipos. Frecventă în zonele montane și de deal.',
        'fishing_techniques': 'Pescuit la undiță de fund, feeder. Nada este esențială pentru atragerea bancului. Momire cu nadă fină, hrană abundentă.',
        'best_baits': 'Vierme, cârnaț, caise, mălai, paste aromate. Nadă din fulgi de ovăz, biscuiți, mălai, pesmet.',
        'legal_info': 'Dimensiune minimă: 20-25 cm. Prohibiție în perioada de reproducere (aprilie-iunie) în unele ape.',
        'average_size': '20-30 cm, 200-500 g',
        'max_size': '60 cm, 4 kg'
    },
    'Obleț': {
        'detailed_description': 'Oblețul (Alburnus alburnus) este un pește mic de suprafață, cu corp foarte comprimat lateral, colorație argintie strălucitoare. Se mișcă în bancuri numeroase. Hrana pentru pești prădători.',
        'habitat': 'Râuri, lacuri, bălți. Se găsește la suprafață sau în straturile superioare ale apei. Bancuri numeroase în zonele cu insecte.',
        'fishing_techniques': 'Pescuit la undiță cu plută mică, montaj fin cu cârlig nr. 18-22. Se folosește ca momeală vie pentru prădători (clean, șalău).',
        'best_baits': 'Vierme mic, colorat, muște artificiale. Pentru captura rapidă: cârlig mic gol sau cu bucățică de vierme.',
        'legal_info': 'Nu există restricții. Folosit ca momeală vie în pescuitul la prădători.',
        'average_size': '10-15 cm, 10-30 g',
        'max_size': '25 cm, 60 g'
    },
    'Plătică': {
        'detailed_description': 'Plătica (Abramis brama) are corp foarte înalt și comprimat lateral, formă romboidală. Colorație argintie cu reflexe aurii. Pește de bancuri care caută hrana pe fund.',
        'habitat': 'Râuri cu curent lent, lacuri de acumulare, bălți. Preferă fundul mâlos, adâncimi de 3-8 m. Activ în special noaptea și în zori.',
        'fishing_techniques': 'Pescuit la feeder cu coș, undiță de fund cu fir elastic. Momire abundentă cu nadă fină. Montaj cu fir 0.16-0.20 mm, cârlig nr. 10-14.',
        'best_baits': 'Vierme roșu, lipan, porumb, cașcaval, paste aromate. Nadă din pesmet, biscuiți, aromă de vanilie sau migdale.',
        'legal_info': 'Dimensiune minimă: 25-30 cm (variază pe ape). Fără prohibiție generală.',
        'average_size': '30-40 cm, 500 g - 1.5 kg',
        'max_size': '75 cm, 6 kg'
    },
    'Păstrăv curcubeu': {
        'detailed_description': 'Păstrăvul curcubeu (Oncorhynchus mykiss) este o specie introdusă, recognoscibilă după banda laterală roz-roșiatică și petele negre pe corp și înotătoare. Prădător activ de apă rece.',
        'habitat': 'Râuri montane și de deal cu apă rece (sub 20°C), oxigenată, curent rapid, fund pietros. Se cultivă în păstrăvării.',
        'fishing_techniques': 'Pescuit la muștă artificială (fly fishing), spinning cu linguriță și wobbler mic, undiță simplă cu plutitor. Tehnica upstream casting.',
        'best_baits': 'Linguriță rotativă 2-4 g, wobbler 3-5 cm, muște artificiale, vierme, pește viu mic. Preferă momeli în mișcare.',
        'legal_info': 'Dimensiune minimă: 20-24 cm (variază). Prohibiție: 1 octombrie - 1 martie în râuri naturale. Cotă zilnică limitată.',
        'average_size': '25-35 cm, 200-500 g',
        'max_size': '80 cm, 9 kg'
    },
    'Păstrăv indigen': {
        'detailed_description': 'Păstrăvul indigen (Salmo trutta fario) este păstrăvul autohton al râurilor montane, cu colorație variabilă: brun-verzui cu pete roșii și negre. Prădător teritorial foarte apreciat.',
        'habitat': 'Râuri montane cu apă foarte rece, limpede, oxigenată, curent rapid. Zonele cu cascade, praguri, adâncituri. Necesită habitat nealter at.',
        'fishing_techniques': 'Pescuit la muștă artificială - tehnica clasică fly fishing. Spinning ultra-light cu momeli mici. Respectarea habitatului este esențială.',
        'best_baits': 'Muște artificiale (uscate, nimfe, streamere), linguriță 1-3 g, micro wobbler, vierme de râu. Momeli naturale în culori discrete.',
        'legal_info': 'Specie protejată! Dimensiune minimă: 24-26 cm. Prohibiție: 1 octombrie - 1 martie. Catch & release recomandat. Cotă: 1-3 exemplare/zi.',
        'average_size': '20-30 cm, 150-400 g',
        'max_size': '100 cm, 15 kg (marmorate rar)'
    },
    'Roșioară': {
        'detailed_description': 'Roșioara (Rutilus rutilus) este un ciprinid cu corp ovoid, comprimat lateral. Înotătoarea caudală și anală sunt roșii-portocalii. Colorație argintie cu reflexe aurii. Pește de bancuri foarte răspândit.',
        'habitat': 'Râuri cu curent lent, lacuri, bălți. Se adaptează în diverse condiții. Preferă zonele cu vegetație, la adâncimi mici și medii.',
        'fishing_techniques': 'Pescuit la undiță cu plută, feeder ușor. Montaj fin cu cârlig nr. 12-16. Pescuit dinamic cu schimbarea frecventă a adâncimii.',
        'best_baits': 'Vierme roșu, lipan, porumb, colorat, paste. Nadă din pesmet, biscuiți, aromă de vanilie sau anason.',
        'legal_info': 'Nu există restricții speciale. Dimensiune recomandată: 15 cm.',
        'average_size': '15-20 cm, 50-150 g',
        'max_size': '45 cm, 1.8 kg'
    },
    'Somn': {
        'detailed_description': 'Somnul (Silurus glanis) este cel mai mare pește de apă dulce din Europa, prădător nocturn cu corp alungit fără solzi, cap mare aplatizat, gură largă cu numeroși dinți mici și 6 mustăți. Colorație verzui-cenușie marmorată.',
        'habitat': 'Râuri mari, lacuri de acumulare, zone adânci cu trunchiuri scufundate, piloni, denivelări. Preferă apele tulburi și calde. Activ în special noaptea.',
        'fishing_techniques': 'Pescuit la clonc (wobbler mare, firulină masivă), vertical jigging, pescuit cu pește viu. Echipament foarte rezistent: lansete heavy, mulinetă mare, fir peste 0.50 mm.',
        'best_baits': 'Pește viu mare (crap, caras, clean), bucăți de pește, caracatiță, carne, păsări. Momeli artificiale mari: shad 20-30 cm, wobbler, firulină.',
        'legal_info': 'Dimensiune minimă: 70-90 cm (variază pe ape). Prohibiție: 1 aprilie - 31 mai. Cotă: 1-2 exemplare/zi. Catch & release recomandat pentru exemplare mari.',
        'average_size': '80-150 cm, 10-40 kg',
        'max_size': '280 cm, 150 kg'
    },
    'Sturion': {
        'detailed_description': 'Sturionul este o familie de pești cartilaginoși primitivi, cu corp alungit acoperit de scuturi osoase, bot alungit, gură inferioară cu 4 mustăți. În România au existat 6 specii în Dunăre și Marea Neagră, majoritatea critice sau dispărute.',
        'habitat': 'Istoric: Dunărea inferioară, Marea Neagră, migrații în amonte pentru reproducere. Preferă apele adânci, fund nisipos sau pietros. Specie anadromă (trăiește în mare, se reproduce în râuri).',
        'fishing_techniques': 'PESCUITUL COMERCIAL ȘI RECREATIV INTERZIS! Specie protejată strict. Orice captură accidentală trebuie eliberată imediat.',
        'best_baits': 'NU SE APLICĂ - pescuitul este interzis.',
        'legal_info': 'SPECIE STRICT PROTEJATĂ! Pescuitul interzis complet. Captură accidentală trebuie raportată și eliberată imediat. Pedepse severe pentru braconaj. Programele de repopulare în curs.',
        'average_size': 'Variabil: 80-200 cm, 10-100 kg (depinde de specie)',
        'max_size': '600 cm, 1.200 kg (Huso huso - morun/beluga - dispărut din România)'
    },
    'Șalău': {
        'detailed_description': 'Șalăul (Sander lucioperca) - vezi Clean. În România, denumirile șalău și clean se referă la aceeași specie. Șalău este denumirea tradițională românească, clean este împrumutul din limba maghiară.',
        'habitat': 'Identic cu cleanul: lacuri de acumulare, râuri mari, zone adânci cu fund nisipos sau pietros.',
        'fishing_techniques': 'Identic cu cleanul: spinning, jigging, pescuit cu pește viu.',
        'best_baits': 'Identic cu cleanul: shad, twister, wobbler, pește viu.',
        'legal_info': 'Identic cu cleanul: Dimensiune minimă 40 cm, prohibiție 1 aprilie - 31 mai.',
        'average_size': '40-60 cm, 1-3 kg',
        'max_size': '130 cm, 20 kg'
    },
    'Știucă': {
        'detailed_description': 'Știuca (Esox lucius) este un super-prădător cu corp alungit fusiform, bot alungit aplatizat ca ciocul de rață, gură mare cu dinți ascuțiți. Colorație verzuie marmorată, perfectă pentru camuflaj. Vânează din pândă.',
        'habitat': 'Râuri, lacuri, bălți, preferă zonele cu vegetație, trestii, stuf. Se ascunde în pândă așteptând prada. Poate fi găsită la toate adâncimile.',
        'fishing_techniques': 'Pescuit la spinning - cel mai eficient: wobbler, shad, linguriță rotativă, spinnerbait, buzzbait. Pescuit cu pește viu la pluta vie. Topwater fishing spectaculos vara.',
        'best_baits': 'Wobbler 8-15 cm (firetiger, perch), shad 10-15 cm, linguriță rotativă 10-20 g, spinnerbait, pește viu (caras, clean). Momeli zgomotoase și cu vibrații puternice.',
        'legal_info': 'Dimensiune minimă: 40-50 cm (variază). Prohibiție: 15 februarie - 30 aprilie (perioadă reproducere). Cotă: 1-3 exemplare/zi.',
        'average_size': '50-80 cm, 1-4 kg',
        'max_size': '150 cm, 25 kg'
    }
}

def populate_descriptions():
    """Populate fish species descriptions"""
    print("=" * 80)
    print("POPULARE DESCRIERI SPECII DE PEȘTI")
    print("=" * 80)
    print()

    updated_count = 0
    not_found_count = 0
    skipped_count = 0

    print(f"[1/1] Procesez {len(FISH_DATA)} specii...")
    print("-" * 80)

    for fish_name, data in FISH_DATA.items():
        try:
            # Try to find the species by name
            fish = FishSpecies.objects.filter(name__iexact=fish_name).first()

            if not fish:
                print(f"✗ Nu găsesc: {fish_name}")
                not_found_count += 1
                continue

            # Check if already has description
            if fish.detailed_description and len(fish.detailed_description) > 100:
                print(f"○ Există deja: {fish_name}")
                skipped_count += 1
                continue

            # Update all fields
            fish.detailed_description = data['detailed_description']
            fish.habitat = data['habitat']
            fish.fishing_techniques = data['fishing_techniques']
            fish.best_baits = data['best_baits']
            fish.legal_info = data['legal_info']
            fish.average_size = data['average_size']
            fish.max_size = data['max_size']
            fish.save()

            print(f"✓ Actualizat: {fish_name}")
            updated_count += 1

        except Exception as e:
            print(f"✗ Eroare la {fish_name}: {str(e)}")
            not_found_count += 1

    print("-" * 80)
    print()

    # Final statistics
    print("=" * 80)
    print("STATISTICI FINALE")
    print("=" * 80)
    print(f"✓ Specii actualizate: {updated_count}")
    print(f"○ Specii cu date existente: {skipped_count}")
    print(f"✗ Specii negăsite/erori: {not_found_count}")
    print(f"─ Total procesate: {len(FISH_DATA)}")
    print("=" * 80)
    print()

    if updated_count > 0:
        print("✓ Descrierile au fost populate cu succes!")
        print("Pagina /specii-de-pesti/ acum afișează informații complete.")
    print()

if __name__ == '__main__':
    populate_descriptions()
