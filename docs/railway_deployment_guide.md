# AI Risk Shield — Instrukcja Wdrożenia na Railway (Railway Deployment Guide)

Projekt **AI Risk Shield** jest w 100% przygotowany do automatycznego wdrożenia produkcyjnego w chmurze **Railway (railway.app)**.

---

## 🛠️ Przygotowane Pliki Konfiguracyjne w Projekcie

- [Procfile](file:///c:/Users/Kris/Documents/AIRiskShield/Procfile): `web: uvicorn airs_engine.server:app --host 0.0.0.0 --port $PORT`
- [requirements.txt](file:///c:/Users/Kris/Documents/AIRiskShield/requirements.txt): Pakiety `fastapi`, `uvicorn`, `jinja2`, `requests`
- [runtime.txt](file:///c:/Users/Kris/Documents/AIRiskShield/runtime.txt): Środowisko `python-3.11.8`
- [airs_engine/server.py](file:///c:/Users/Kris/Documents/AIRiskShield/airs_engine/server.py): Produkcyjny serwer API & Webhook z obsługą zmiennej środowiskowej `$PORT`.

---

## 🚀 Krok po kroku: Wdrożenie na Railway w 2 minuty

### Krok 1: Wrzucenie zmian na GitHub
Jeśli tworzysz nowe zgłoszenia lub zmieniasz kod, zrób push do swojego repozytorium GitHub:
```bash
git add .
git commit -m "Add production FastAPI webhook server & Railway config"
git push origin main
```

### Krok 2: Uruchomienie Projektu w Railway (railway.app)
1. Zaloguj się na [railway.app](https://railway.app) (możesz zalogować się swoim kontem GitHub).
2. Kliknij **"New Project"** ➔ Wybierz **"Deploy from GitHub repo"**.
3. Wybierz swoje repozytorium **`Kris-Shield/airiskshield`**.
4. Railway automatycznie wykryje plik `Procfile` i `requirements.txt` oraz rozpocznie budowanie aplikacji!

### Krok 3: Wygenerowanie Publicznego Adresu URL (Domain)
1. W panelu projektu w Railway wejdź w zakładkę **Settings** swojego serwisu.
2. W sekcji **Networking** kliknij **"Generate Domain"** (dostaniesz adres np. `https://airiskshield-production.up.railway.app`).

---

## 🔗 Podłączenie Webhooka w Tally.so

1. Otwórz swój formularz na [Tally.so](https://tally.so/r/dWokLD).
2. Przejdź do zakładki **Integrations** ➔ Wybierz **Webhooks**.
3. Wklej publiczny URL z Railway z dociętą ścieżką webhooka:
   👉 **`https://twoja-nazwa.up.railway.app/api/webhook/tally`**
4. Kliknij **"Test Webhook"** / **"Save"**.

OD TEGO MOMENTU KAŻDA WYPEŁNIONA ANKIETA Z TALLY BĘDZIE AUTOMATYCZNIE PRZETWARZANA W CHMURZE PRZEZ TWÓJ SERWER AIRS! 🎉
