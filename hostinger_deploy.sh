#!/bin/bash

# 🚀 Script de deployment pentru Hostinger - Modificări Prețuri 12h/24h
# IMPORTANT: Rulează acest script pe serverul Hostinger prin SSH

echo "🚀 Începe deployment-ul modificărilor pentru prețuri 12h/24h..."

# Verifică dacă suntem în directorul corect
if [ ! -f "manage.py" ]; then
    echo "❌ Eroare: Nu sunt în directorul proiectului Django!"
    echo "Te rog să navighezi în directorul unde se află manage.py"
    exit 1
fi

# 1. Backup baza de date
echo "📦 Creez backup baza de date..."
BACKUP_FILE="backup_before_price_changes_$(date +%Y%m%d_%H%M%S).sql"
# Înlocuiește cu datele tale de conectare la baza de date
# mysqldump -u DB_USER -p DB_NAME > $BACKUP_FILE
echo "⚠️  IMPORTANT: Asigură-te că ai făcut backup la baza de date!"
echo "   Comandă: mysqldump -u DB_USER -p DB_NAME > $BACKUP_FILE"

# 2. Pull ultimele modificări
echo "📥 Pull modificări de pe GitHub..."
git pull origin main

if [ $? -ne 0 ]; then
    echo "❌ Eroare la git pull! Verifică conexiunea și permisiunile."
    exit 1
fi

# 3. Activează mediul virtual (dacă există)
if [ -d "venv" ]; then
    echo "🐍 Activez mediul virtual..."
    source venv/bin/activate
elif [ -d "env" ]; then
    echo "🐍 Activez mediul virtual..."
    source env/bin/activate
else
    echo "⚠️  Nu am găsit mediul virtual. Continuez fără..."
fi

# 4. Instalează dependențele (dacă e necesar)
echo "📦 Verific dependențele..."
pip install -r requirements.txt

# 5. CRUCIAL: Rulează migrația
echo "🗃️  Rulez migrația pentru noile câmpuri de preț..."
python manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ Eroare la migrație! Verifică logs-urile pentru detalii."
    echo "💡 Poți face rollback cu: python manage.py migrate main 0016"
    exit 1
fi

# 6. Colectează fișierele statice
echo "📁 Colectez fișierele statice..."
python manage.py collectstatic --noinput

# 7. Restart aplicația
echo "🔄 Restart aplicația..."
if [ -f "tmp/restart.txt" ]; then
    touch tmp/restart.txt
    echo "✅ Aplicația a fost restartată (Passenger)"
else
    echo "⚠️  Nu am găsit tmp/restart.txt. Încearcă să restartezi manual aplicația."
fi

# 8. Verificări finale
echo "🔍 Verific că aplicația funcționează..."
python manage.py check

if [ $? -eq 0 ]; then
    echo "✅ Deployment finalizat cu succes!"
    echo ""
    echo "🎯 Verificări finale:"
    echo "   1. Accesează site-ul și verifică că lacurile afișează ambele prețuri"
    echo "   2. Testează panoul de administrare (/admin)"
    echo "   3. Încearcă să editezi un lac existent"
    echo "   4. Încearcă să creezi un lac nou"
    echo ""
    echo "📊 Modificări aplicate:"
    echo "   - Câmp price_per_day → price_12h + price_24h"
    echo "   - Template-uri actualizate pentru afișarea ambelor prețuri"
    echo "   - Panoul admin actualizat cu noile câmpuri"
    echo ""
    echo "🆘 În caz de probleme:"
    echo "   - Verifică logs: tail -f logs/error.log"
    echo "   - Rollback migrație: python manage.py migrate main 0016"
    echo "   - Restaurare backup: mysql -u DB_USER -p DB_NAME < $BACKUP_FILE"
else
    echo "❌ Deployment a eșuat! Verifică erorile de mai sus."
    exit 1
fi
