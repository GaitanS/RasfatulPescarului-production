# 🚀 Ghid Deployment - Modificări Prețuri 12h/24h

## ⚠️ IMPORTANT: Backup înainte de deployment!

### Pasul 1: Backup baza de date (pe Hostinger)
```bash
# Conectează-te la Hostinger prin SSH sau phpMyAdmin
# Exportă baza de date înainte de orice modificare
mysqldump -u username -p database_name > backup_before_price_changes_$(date +%Y%m%d_%H%M%S).sql
```

### Pasul 2: Commit modificările locale
```bash
# Adaugă toate fișierele modificate
git add main/admin.py
git add main/forms.py  
git add main/models.py
git add main/views.py
git add templates/index/index.html
git add templates/lakes/create_lake.html
git add templates/lakes/delete_lake.html
git add templates/lakes/edit_lake.html
git add templates/lakes/my_lakes.html
git add templates/locations/county_lakes.html
git add templates/locations/lake_detail.html
git add templates/locations/list.html
git add main/migrations/0017_add_price_12h_24h_fields.py

# Commit cu mesaj descriptiv
git commit -m "feat: Split price field into 12h and 24h separate fields

- Replace single price_per_day with price_12h and price_24h fields
- Update all templates to display both prices
- Update admin interface with new fields
- Add migration to preserve existing data
- Maintain backward compatibility with price_per_day property"
```

### Pasul 3: Push pe GitHub
```bash
git push origin main
```

### Pasul 4: Deployment pe Hostinger

#### A. Conectare SSH la Hostinger
```bash
ssh username@your-domain.com
cd public_html  # sau calea către proiectul tău
```

#### B. Pull modificările
```bash
git pull origin main
```

#### C. Activează mediul virtual (dacă folosești)
```bash
source venv/bin/activate  # sau calea către venv-ul tău
```

#### D. Instalează/actualizează dependențele (dacă e necesar)
```bash
pip install -r requirements.txt
```

#### E. **CRUCIAL: Rulează migrația**
```bash
python manage.py migrate
```

#### F. Colectează fișierele statice
```bash
python manage.py collectstatic --noinput
```

#### G. Restart aplicația
```bash
# Pentru Passenger (Hostinger folosește de obicei Passenger)
touch tmp/restart.txt

# SAU dacă ai acces la restart manual
sudo systemctl restart your-app-name
```

### Pasul 5: Verificare post-deployment

#### A. Testează site-ul
- Accesează site-ul principal
- Verifică că lacurile afișează ambele prețuri
- Testează panoul de administrare
- Verifică că poți edita lacurile cu noile câmpuri

#### B. Verifică logs pentru erori
```bash
tail -f logs/error.log  # sau calea către log-urile tale
```

### Pasul 6: Actualizare date existente (dacă e necesar)

Dacă ai lacuri existente cu date în vechiul câmp `price_per_day`, poți rula acest script pentru a popula noile câmpuri:

```python
# Script pentru actualizarea datelor existente
python manage.py shell

# În shell-ul Django:
from main.models import Lake
from decimal import Decimal

# Pentru fiecare lac existent, setează prețurile bazate pe vechiul preț
for lake in Lake.objects.all():
    if hasattr(lake, 'price_per_day_old'):  # dacă mai există vechiul câmp
        # Estimează prețul pentru 12h ca fiind ~60% din prețul pe zi
        lake.price_12h = lake.price_per_day_old * Decimal('0.6')
        lake.price_24h = lake.price_per_day_old
        lake.save()
        print(f"Actualizat {lake.name}: 12h={lake.price_12h}, 24h={lake.price_24h}")
```

## 🔍 Verificări finale

### Checklist post-deployment:
- [ ] Site-ul se încarcă fără erori
- [ ] Lacurile afișează ambele prețuri (12h și 24h)
- [ ] Panoul admin funcționează cu noile câmpuri
- [ ] Poți crea lacuri noi cu ambele prețuri
- [ ] Poți edita lacurile existente
- [ ] Nu există erori în logs

### În caz de probleme:

#### Rollback rapid:
```bash
# Dacă ceva merge prost, poți face rollback
git log --oneline -5  # vezi ultimele commit-uri
git reset --hard COMMIT_HASH_ANTERIOR  # înlocuiește cu hash-ul anterior
python manage.py migrate main 0016  # rollback la migrația anterioară
```

#### Restaurare backup:
```bash
# Dacă e nevoie să restaurezi baza de date
mysql -u username -p database_name < backup_before_price_changes_TIMESTAMP.sql
```

## 📞 Support

Dacă întâmpini probleme:
1. Verifică logs-urile pentru erori specifice
2. Asigură-te că migrația s-a rulat cu succes
3. Verifică că toate fișierele au fost actualizate corect
4. Testează pas cu pas fiecare funcționalitate

## 🎯 Rezultatul final

După deployment, vei avea:
- Câmpuri separate pentru prețuri 12h și 24h
- Toate template-urile actualizate
- Panoul admin funcțional cu noile câmpuri
- Datele existente păstrate și funcționale
