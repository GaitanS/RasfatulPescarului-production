# 🚀 Ghid Rapid de Deployment pe Hostinger

## ⚠️ IMPORTANT: Backup înainte de orice!

### Pasul 1: Backup Baza de Date
```bash
# Conectează-te la Hostinger prin SSH
ssh username@your-domain.com

# Navighează în directorul proiectului
cd public_html  # sau calea către proiectul tău

# Creează backup
mysqldump -u DB_USER -p DB_NAME > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Pasul 2: Deployment Automat
```bash
# Rulează scriptul de deployment
./hostinger_deploy.sh
```

**SAU manual:**

```bash
# Pull modificările
git pull origin main

# Activează mediul virtual (dacă ai)
source venv/bin/activate

# Rulează migrația (CRUCIAL!)
python manage.py migrate

# Colectează fișierele statice
python manage.py collectstatic --noinput

# Restart aplicația
touch tmp/restart.txt
```

### Pasul 3: Verificare
```bash
# Rulează scriptul de verificare
python verify_deployment.py
```

### Pasul 4: Test Manual
1. **Accesează site-ul** - verifică că lacurile afișează prețurile "X Lei/12h • Y Lei/24h"
2. **Testează admin** - `/admin` - verifică că poți edita lacurile cu noile câmpuri
3. **Creează lac nou** - testează că formularul funcționează cu ambele prețuri

## 🆘 În caz de probleme

### Rollback rapid:
```bash
# Rollback migrație
python manage.py migrate main 0016

# Rollback cod
git reset --hard HEAD~1

# Restaurare backup
mysql -u DB_USER -p DB_NAME < backup_TIMESTAMP.sql
```

### Verificare logs:
```bash
tail -f logs/error.log
# sau
tail -f /path/to/your/logs/error.log
```

## ✅ Checklist Final

- [ ] Backup baza de date creat
- [ ] Git pull executat cu succes
- [ ] Migrația rulată fără erori
- [ ] Fișierele statice colectate
- [ ] Aplicația restartată
- [ ] Site-ul afișează prețurile 12h/24h
- [ ] Panoul admin funcționează
- [ ] Poți crea/edita lacuri

## 📞 Support

Dacă întâmpini probleme:
1. Verifică că migrația s-a rulat: `python manage.py showmigrations main`
2. Verifică logs pentru erori specifice
3. Testează pas cu pas fiecare funcționalitate
4. În caz de urgență, folosește rollback-ul

## 🎯 Ce s-a schimbat

- **Înainte**: Un câmp `price_per_day`
- **Acum**: Două câmpuri `price_12h` și `price_24h`
- **Compatibilitate**: Proprietatea `price_per_day` încă funcționează (returnează `price_24h`)
- **Template-uri**: Toate actualizate pentru a afișa ambele prețuri
- **Admin**: Configurat cu noile câmpuri
