# CyberNova
1. Obiectivul Proiectului

Proiectul CH2.0 este un Honeypot de Threat Intelligence conceput pentru a identifica, clasifica și analiza instrumentele automate de atac (credential stuffers, config scrapers, boți) prin simularea unei vulnerabilități API tentante. Scopul nu este furtul de date, ci colectarea de informații avansate despre atacator (fingerprinting).

2.Sistemul este împărțit în trei componente principale:
frontend/Momeală                   Simplu HTML/CSS                      Servește ca o pagină inițială de login.
Backend/Motorul Honeypot           Python (Flask/FastAPI)               Gestionează endpoint-urile API, analizează cererile,        
                                                                         integrează API-urile externe și scrie log-urile.

Alertare/Reporting                 Discord Webhook sau Telegram Bot      Notificare instantanee și structurată a evenimentelor de 
                                                                         înaltă gravitate.