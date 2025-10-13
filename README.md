# CyberNova
Conceptul de Bază:
Vei construi o aplicație web simplă care imită o pagină de autentificare (login). Scopul acesteia nu este să autentifice utilizatori, ci să funcționeze ca o capcană digitală.

Cum Funcționează:

Un utilizator (sau un atacator) introduce un nume de utilizator și o parolă pe pagina ta falsă.

În loc să verifice dacă datele sunt corecte, sistemul tău va captura și salva următoarele informații:

Numele de utilizator și parola introduse.

Adresa IP a vizitatorului.

User-Agent-ul (informații despre browser-ul și sistemul său de operare).

Focalizarea pentru Concurs:
Pentru acest hackathon, accentul principal nu este pe crearea unei pagini web complicate sau cu un design complex. Punctul central al proiectului tău este sistemul din spate, adică:

Logging (Înregistrarea): Salvarea eficientă a datelor capturate într-un fișier.

Alerting (Alertarea): Trimiterea unei notificări instantanee pe un canal de Discord de fiecare dată când cineva încearcă să se "autentifice".