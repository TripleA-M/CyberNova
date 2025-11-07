# CyberNova
1. Obiectivul Proiectului

Proiectul CH2.0 este un Honeypot de Threat Intelligence conceput pentru a identifica, clasifica și analiza instrumentele automate de atac (credential stuffers, config scrapers, boți) prin simularea unei vulnerabilități API tentante. Scopul nu este furtul de date, ci colectarea de informații avansate despre atacator (fingerprinting).

2.Sistemul este împărțit în trei componente principale:
frontend/Momeală                   Simplu HTML/CSS                      Servește ca o pagină inițială de login.
Backend/Motorul Honeypot           Python (Flask/FastAPI)               Gestionează endpoint-urile API, analizează cererile,        
                                                                         integrează API-urile externe și scrie log-urile.

Alertare/Reporting                 Discord Webhook sau Telegram Bot      Notificare instantanee și structurată a evenimentelor de 
                                                                         înaltă gravitate.



 3. Specificații Tehnice ale Backend-ului

Motorul Honeypot trebuie să expună minim două endpoint-uri:

A. Endpoint-ul Momeală (The Lure)

Ruta: POST /api/v1/auth/test (simulează o verificare de credențiale în masă)

Logică:

Captură: Loghează IP-ul, User-Agent-ul și orice date primite în corpul cererii (simulând datele de login).

Răspuns Tentant: Returnează un răspuns HTTP 200 OK cu un payload JSON care conține lista falsă de credențiale eșuate și link-ul capcană de actualizare a cheii API.    


B. Endpoint-ul Capcană (The Trap)

Ruta: GET /api/v1/key/update (aceasta este calea pe care o va accesa instrumentul automat al atacatorului)

Logică:

Fingerprinting Avansat: Aceasta este funcția critică. Loghează absolut toate headerele HTTP primite, inclusiv headerele non-standard (ex: X-Requested-With, Sec-Fetch-Mode) și verifică dacă parametrii agent și ip din URL (trimiși din payload-ul momeală) au fost rezolvați corect de instrumentul atacatorului.

Scor de Amenințare (Threat Scoring):

Integrare cu o API GeoIP gratuită (e.g., ip-api.com).

Analiza User-Agent-ului împotriva unei liste de User-Agente cunoscute de boți.

Punctaj pentru prezența/absența headerelor specifice.

Alertare: Declanșează o notificare de mare prioritate (Alert Level: CRITICAL) către canalul de Discord.
Logging și Alertare (Output-ul Proiectului)

A. Logging (Fișier)

Toate datele capturate vor fi salvate într-un fișier attacks.log sau într-o bază de date simplă (SQLite) cu formatul:
Alertare (Discord Webhook)

Alertele trebuie să fie clare și să includă scorul de amprentare (Fingerprint Score) pentru vizualizare rapidă.

Titlu:  CRITICAL ALERT: Tool Fingerprinted (Score: 9/10)

Corpul Alertei: Detalii despre IP, Geolocație, și o listă a headerelor neobișnuite detectate care au contribuit la scor.
Pașii de Implementare (Roadmap)

Acest roadmap ne va ghida în implementarea secvențială:

Configurare Inițială: Configurare proiect (Flask/FastAPI), structură de foldere.

Implementare Endpoint A (Momeala): Crearea rutei POST /api/v1/auth/test și a răspunsului JSON.

Implementare Endpoint B (Capcana): Crearea rutei GET /api/v1/key/update și a logicii de colectare a headerelor complete.

Integrare GeoIP: Implementarea funcției care interoghează o API externă pentru geolocație pe baza IP-ului.

Logica Fingerprinting & Scoring: Dezvoltarea algoritmului de atribuire a scorului de amenințare.

Implementare Alertare: Setarea Discord Webhook-ului (sau Telegram Bot-ului) pentru a trimite mesajul structurat.

Testare Finală: Testarea sistemului cu cereri cURL și simulări de bot.

