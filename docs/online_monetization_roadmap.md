# AI Risk Shield — Strategia Wdrożenia Online & Monetyzacji (Go-To-Market Roadmap)

Ten dokument opisuje kompletny plan uruchomienia **AI Risk Shield** produkcyjnie online, podłączenia płatności, automatyzacji maili oraz pozyskiwania pierwszych płacących klientów B2B.

---

## 🎯 1. Model Monetyzacji & Struktura Cennika (Pricing Architecture)

### 🟢 Poziom 1: Lead Magnet / Free AIRS Score Overview (0 PLN)
* **Cel:** Pozyskiwanie leadów B2B (E-mail, Nazwa Firmy, Liczba Pracowników).
* **Co otrzymuje klient:** Szybki, 1-stronicowy podgląd punktacji AIRS Score (`23.8 / 100`) i informacja o flagach ryzyka EU AI Act.
* **Call To Action:** *"Zamów pełny Audyt Wykonawczy z Pakietem Procedur Wdrożeniowych (990 PLN)"*.

---

### 🔵 Poziom 2: Full AIRS Executive Audit & Remediation Pack (990 PLN – 2 490 PLN / €250 – €600)
* **Cel:** Główny produkt dochodowy (B2B Self-Service lub z weryfikacją ludzką).
* **Co otrzymuje klient:**
  - Pełny raport zarządczy (HTML / PDF) z wykresami **Radar Footprint** i **Index Bar**.
  - Szacowanie ryzyka wg **EU AI Act (Annex III / Art. 28 / Art. 50)** i RODO.
  - Szczegółowe procedury naprawcze na **7, 30 i 90 dni**.
  - **Pakiet Wdrożeniowy:** Szablon Polityki AI v1.0, klauzule do umów z klientami, checklisty anonimizacji DLP.
  - Zatwierdzenie przez Certyfikowanego Audytora (Human Review).

---

### 🟣 Poziom 3: Enterprise AI Governance Retainer (3 900 PLN – 6 900 PLN / msc)
* **Cel:** Stały przychód subskrypcyjny (ARR / MRR) dla Software House'ów i korporacji.
* **Co otrzymuje klient:**
  - Ciągłe monitorowanie zmian w prawie (dzięki naszemu silnikowi `kb_updater.py`).
  - Kwartalne re-audyty dojrzałości AI.
  - Dedykowane wsparcie Inspektora Ochrony AI / DPO.

---

## 🚀 2. Architektura Techniczna Online (Online Stack)

```
[ Formularz Tally.so ] 
       │
       ▼ (Webhook)
[ Serwer API AIRS (FastAPI / Node.js) ] ───► [ Silnik AIRS Scoring Engine & KB ]
       │                                                    │
       ▼                                                    ▼
[ Panel Audytora (Dashboard) ] ──(Zatwierdzenie)──► [ Generator PDF / HTML ]
                                                            │
                                                            ▼ (Resend / SendGrid API)
                                                [ Wysyłka Mailem do Klienta ]
```

### Elementy Wdrożenia:
1. **Hosting Aplikacji Webowej & API:** Vercel / Railway / Render (Koszty: ~0 - $20/msc).
2. **Automatyczna Wysyłka E-mail (Transactional Email):** Resend API lub Postmark API.
3. **Bramka Płatności (Checkout):** Stripe / Przelewy24 (automatyczne pobieranie opłaty przed dostarczeniem pełnego raportu).

---

## 📅 3. Harmonogram Działań (Action Plan)

- [ ] **Krok 1:** Przygotowanie serwera produkcyjnego API (`server.py`) i podłączenie Webhooka Tally.so
- [ ] **Krok 2:** Podłączenie wysyłki e-mail z raportem (Resend / SendGrid API)
- [ ] **Krok 3:** Integracja płatności Stripe / Przelewy24
- [ ] **Krok 4:** Strona Landing Page sprzedażowa (z nagłówkami z naszego Playbooka Marketingowego)
- [ ] **Krok 5:** Start Kampanii Lead Generation (LinkedIn Cold Outreach & Content)
