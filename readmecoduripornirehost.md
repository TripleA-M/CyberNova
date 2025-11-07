DO NOT MODIFY THIS MD

run all Win: 

pwsh -File .\run_all.ps1

run all Mac:

chmod +x ./run_all.sh
./run_all.sh

mkdir CYBERNOVA 

CD CYBERNOVA

python3 -m venv .venv - PT MACOS 
py -3 -m venv .venv - WIN

. .venv/bin/activate - MACOS
.venv\Scripts\activate - WIN

pip install Flask

pip install Flask request

python -m pip install requests

honeypot\cybernova-honeypot -> app.py -> right click -> Reveal in File explorer -> copy destination -> VS Code Terminal -> CD destination 

python app.py



Comenzi bot:
(In doua terminale diferite)

node honeypot/cybernova-honeypot/server.js

python honeypot/cybernova-honeypot/app.py