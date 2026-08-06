# AI Risk Shield — Multilingual Questionnaire Specification (EN / PL)

This document contains the exact question text, options, and block types in both **English (Primary International)** and **Polish (Local Market)** for your Tally.so form (`https://tally.so/r/dWokLD`).

---

## 📌 Section A: Company Information / Information o Firmie

### Q1. Company Name / Nazwa Firmy
* **Type:** Input Text (Short Text)
* **EN Label:** Company Name
* **PL Label:** Nazwa firmy

### Q2. Corporate Email / Email Służbowy
* **Type:** Input Email
* **EN Label:** Corporate Email (where the report will be sent)
* **PL Label:** Służbowy adres e-mail (na który prześlemy raport)

### Q3. Country of Operation / Kraj Prowadzenia Działalności
* **Type:** Dropdown
* **EN Label:** Primary Country of Operation
* **PL Label:** Główny kraj prowadzenia działalności

### Q4. Industry / Branża
* **Type:** Dropdown
* **EN Label:** Industry Sector
* **PL Label:** Sektor / Branża

### Q5. Company Size / Wielkość Firmy
* **Type:** Multiple Choice
* **EN Options:**
  - 1-9 employees
  - 10-49 employees
  - 50-249 employees
  - 250+ employees
* **PL Options:**
  - 1-9 pracowników
  - 10-49 pracowników
  - 50-249 pracowników
  - 250+ pracowników

---

## 📌 Section B: AI Adoption & Licensing / Wykorzystanie AI i Licencjonowanie

### Q6. AI Tools in Use / Używane Narzędzia AI
* **Type:** Checkboxes
* **EN Label:** Which AI tools does your organization currently use?
* **PL Label:** Z jakich narzędzi AI korzysta obecnie Twoja firma?
* **Options (Both):** ChatGPT, Claude, Microsoft Copilot, Gemini, GitHub Copilot, Midjourney, Perplexity, Jasper, Canva AI, Custom LLM APIs, Other

### Q7. Account Licensing Tier / Wersje Licencji i Konta (CRITICAL RODO/GDPR CHECK)
* **Type:** Multiple Choice
* **EN Label:** Do employees use company-managed paid subscriptions or personal free accounts?
* **EN Options:**
  - `100% company-managed enterprise subscriptions (Zero Data Retention guaranteed)`
  - `Mix of company plans and personal accounts`
  - `Mostly personal free accounts`
  - `Not sure / We do not track AI account licensing`
* **PL Label:** Czy pracownicy korzystają z płatnych subskrypcji firmowych, czy z darmowych kont osobistych?
* **PL Options:**
  - `100% konta firmowe (Enterprise / Team z gwarancją braku trenowania modeli na naszych danych)`
  - `Mieszane — część pracowników ma konta firmowe, część używa darmowych kont osobistych`
  - `Głównie darmowe konta osobiste pracowników`
  - `Nie wiemy / Nie kontrolujemy licencjonowania kont AI`

---

## 📌 Section C: Data Protection & Confidentiality / Ochrona Danych i Poufność

### Q8. Confidential Data Uploads / Wgrywanie Danych Poufnych
* **Type:** Multiple Choice
* **EN Label:** Do employees upload confidential customer or company information into AI tools?
* **EN Options:**
  - `Yes`
  - `No`
  - `Not sure / We do not currently monitor employee AI prompts`
* **PL Label:** Czy pracownicy wgrywają poufne dane klientów lub firmy do narzędzi AI?
* **PL Options:**
  - `Tak`
  - `Nie`
  - `Nie wiemy / Nie monitorujemy treści promptów wpisywanych przez pracowników`

---

## 📌 Section E: AI Governance & Policy / Nadzór i Polityka AI

### Q9. Official AI Usage Policy / Oficjalna Polityka Korzystania z AI
* **Type:** Multiple Choice
* **EN Label:** Does your company have an official AI Usage Policy?
* **EN Options:**
  - `Yes, we have a formally approved AI Policy`
  - `Informal guidelines exist, but no official written policy`
  - `Drafting an AI policy is currently in progress`
  - `No, we do not currently have an AI policy`
* **PL Label:** Czy Twoja firma posiada oficjalną Politykę Korzystania z AI (AI Usage Policy)?
* **PL Options:**
  - `Tak, mamy oficjalnie zatwierdzoną politykę AI`
  - `Nie formalnie, ale istnieją nieoficjalne wytyczne/zasady`
  - `Właśnie przygotowujemy projekt polityki`
  - `Nie, nie posiadamy żadnej polityki AI`

---

## 📌 Section F: High-Risk AI Systems & Automation / Systemy Wysokiego Ryzyka

### Q10. High-Risk System Categories / Zastosowania Wysokiego Ryzyka (EU AI Act Annex III & Art. 50)
* **Type:** Checkboxes
* **EN Label:** Is AI used for any of the following automated functions?
* **EN Options:**
  - Candidate recruitment & talent selection
  - Automated CV screening & candidate scoring
  - Employee performance monitoring & task allocation
  - Customer credit scoring or financial risk evaluation
  - Customer support chatbots / Automated messaging (Art. 50 Transparency)
  - None of the above
* **PL Label:** Czy AI jest wykorzystywane w Twojej firmie do któregokolwiek z poniższych zastosowań?
* **PL Options:**
  - Rekrutacja i selekcja kandydatów
  - Skanowanie i ocena CV
  - Ocena i wydajność pracowników
  - Segmentacja klientów lub scoring kredytowy
  - Automatyczne chatboty obsługi klienta / wysyłka wiadomości (Art. 50 EU AI Act)
  - Żadne z powyższych

---

## 📌 Section H: Technical Architecture / Architektura Techniczna (EU AI Act Art. 28)

### Q11. Custom AI Software & APIs / Autorskie Oprogramowanie AI i API
* **Type:** Multiple Choice
* **EN Label:** Does your company develop custom AI features, fine-tune models, or integrate LLM APIs into your products?
* **EN Options:**
  - `Yes, we build custom AI features / RAG / API integrations into our products`
  - `Yes, we fine-tune or train custom AI models`
  - `No, we only use off-the-shelf third-party AI applications`
* **PL Label:** Czy Twoja firma tworzy własne oprogramowanie z integracją LLM API, bazami RAG lub trenuje własne modele AI?
* **PL Options:**
  - `Tak, tworzymy własne funkcje AI / integracje LLM API / bazy RAG w naszych produktach`
  - `Tak, dostrajamy (fine-tuning) lub trenujemy własne modele AI`
  - `Nie, korzystamy wyłącznie z gotowych zewnętrznych aplikacji AI (off-the-shelf)`
