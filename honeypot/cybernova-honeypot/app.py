from flask import Flask, request, render_template, redirect, session, url_for, send_file
import logging
import os
from datetime import timedelta, datetime
import requests
from werkzeug.security import generate_password_hash, check_password_hash
try:
    import importlib
    _dotenv = importlib.import_module("dotenv")
    load_dotenv = getattr(_dotenv, "load_dotenv", lambda *args, **kwargs: False)
except Exception:  # Allow running even if python-dotenv isn't installed yet
    def load_dotenv(*args, **kwargs):
        return False
from markupsafe import escape, Markup

from geoip.geoip_utils import get_geo_data
from scoring.scoring_utils import calculate_fingerprint_score

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Load environment variables from repo root .env (if present)
load_dotenv(os.path.join(BASE_DIR, '.env'))
GLOBAL_STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(
    __name__,
    static_folder=GLOBAL_STATIC_DIR,
    template_folder='templates'
)

# Secrets and session configuration
SECRET_KEY = os.getenv("SECRET_KEY") or os.urandom(24)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes=10)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

logging.basicConfig(level=logging.INFO)

# Store failed login attempts in memory (for demo; use DB for production)
failed_logins = {}

# URL of the local Node.js relay that forwards messages to Discord.
# Configure via env var DISCORD_PROXY_URL; default assumes server.js runs on port 3000.
DISCORD_PROXY_URL = os.getenv("DISCORD_PROXY_URL", "http://localhost:3000/send-to-discord")
DISCORD_NOTIFY_USERNAME = os.getenv("DISCORD_NOTIFY_USERNAME", "CyberNova Bot")


def send_to_discord(username: str, message: str) -> None:
    """Best-effort notify the Discord relay service.

    Does not raise on failure; logs errors so the main flow isn't blocked.
    """
    try:
        payload = {"username": username or DISCORD_NOTIFY_USERNAME, "message": message}
        resp = requests.post(DISCORD_PROXY_URL, json=payload, timeout=5)
        if resp.status_code >= 400:
            logging.error("Discord relay responded with %s: %s", resp.status_code, resp.text)
        else:
            logging.info("Notified Discord relay successfully")
    except Exception as e:
        logging.exception("Failed to notify Discord relay: %s", e)

SUDO_EMAIL = os.getenv("SUDO_EMAIL", "tripelA&M@gmail.com")
SUDO_PASSWORD = os.getenv("SUDO_PASSWORD", "AndreiAntonio2xMarius")

USERS_FILE = "users.txt"

def save_user(email, password):
    hashed = generate_password_hash(password)
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{email},{hashed}\n")

def get_user(email):
    if not os.path.exists(USERS_FILE):
        return None
    with open(USERS_FILE, encoding="utf-8", errors="replace") as f:
        for line in f:
            user_email, user_hash = line.strip().split(",", 1)
            if user_email == email:
                return user_hash
    return None

ip_sessions = {}      # {ip: {"start": datetime, "blocked_until": datetime, "fail_count": int}}
blocked_ips = set()   # IP-uri blocate

@app.route("/", methods=["GET", "POST"])
def index():
    error = request.args.get("error") or session.pop("error", None)
    now = datetime.utcnow()
    ip_address = request.remote_addr

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        action = request.form.get("action")
        user_agent = request.headers.get("User-Agent")
        ip_address = request.remote_addr

        # Doar login SUDO
        if action == "login":
            if email == SUDO_EMAIL and password == SUDO_PASSWORD:
                session["email"] = email
                session["is_admin"] = True
                session["user_agent"] = user_agent
                session["ip_address"] = ip_address
                session.permanent = True
                ts = datetime.utcnow().isoformat() + "Z"
                send_to_discord(
                    DISCORD_NOTIFY_USERNAME,
                    f"[Login] @Admin SUDO login\n⏰ {ts}\n📧 Email: {email}\n🌐 IP: {ip_address}\n🖥️ UA: {user_agent}"
                )
                return redirect("/dashboard")
            else:
                ts = datetime.utcnow().isoformat() + "Z"
                # Compute a basic threat score from current request headers
                try:
                    threat_score = calculate_fingerprint_score(request.headers)
                except Exception:
                    logging.exception("Failed to compute threat score")
                    threat_score = 0
                send_to_discord(
                    DISCORD_NOTIFY_USERNAME,
                    f"[Security] @Admin Failed SUDO login\n⏰ {ts}\n📧 Email: {email}\n🌐 IP: {ip_address}\n🖥️ UA: {user_agent}\n🧮 Threat Score: {threat_score}"
                )
                with open("database.txt", "a", encoding="utf-8") as f:
                    f.write(
                        f"---\n"
                        f"⏰ Data: {ts}\n"
                        f"❌ Tip: Failed login attempt\n"
                        f"🌐 IPweb: {ip_address}\n"
                        f"🖥️ User-Agent: {user_agent}\n"
                        f"🧮 Threat Score: {threat_score}\n"
                        f"---\n"
                    )
                error = "Email sau parolă greșită!"
        else:
            error = "Doar autentificare SUDO este permisă momentan!"

    return render_template("index.html", error=error)

@app.route("/dashboard")
def dashboard():
    email = session.get("email")
    user_agent = session.get("user_agent")
    is_admin = session.get("is_admin", False)
    # ip_address is stored but not displayed
    if is_admin and email == SUDO_EMAIL:
        return f"""
        <h2>Bine ai venit, {escape(email)}</h2>
        <p>User-Agent: {escape(user_agent or '')}</p>
        <p>Datele tale vor fi reținute 10 minute.</p>
        <p><a href="/view-database">Vezi baza de date</a></p>
        """
    elif email:
        return f"""
        <h2>Bine ai venit, {escape(email)}</h2>
        <p>User-Agent: {escape(user_agent or '')}</p>
        <p>Datele tale vor fi reținute 10 minute.</p>
        <p>Nu ai permisiuni pentru a vedea baza de date.</p>
        """
    return redirect("/")

@app.route("/failed-login")
def failed_login():
    ip = session.get("failed_ip")
    user_agent = session.get("failed_user_agent")
    ts = None
    if ip and ip in failed_logins:
        ts_obj = failed_logins[ip].get("timestamp")
        if ts_obj:
            ts = ts_obj.isoformat() + "Z" if isinstance(ts_obj, datetime) else str(ts_obj)
    if not ts:
        ts = datetime.utcnow().isoformat() + "Z"

    # Compute a basic threat score from the current request headers
    try:
        threat_score = calculate_fingerprint_score(request.headers)
    except Exception:
        logging.exception("Failed to compute threat score")
        threat_score = 0

    with open("database.txt", "a", encoding="utf-8") as f:
        f.write(
            f"---\n"
            f"⏰ Data: {ts}\n"
            f"❌ Tip: Failed login attempt\n"
            f"🌐 IPweb: {ip}\n"
            f"🖥️ User-Agent: {user_agent}\n"
            f"🧮 Threat Score: {threat_score}\n"
            f"---\n"
        )
    # Notify Discord about failed login attempt
    send_to_discord(
        DISCORD_NOTIFY_USERNAME,
        f"[Security] @Admin Failed login attempt\n⏰ {ts}\n🌐 IP: {ip}\n🖥️ UA: {user_agent}\n🧮 Threat Score: {threat_score}"
    )
    return redirect(url_for("index", error="Wrong Password"))

@app.route('/honeypot', methods=['POST'])
def honeypot():
    ip_address = request.remote_addr
    geo_data = get_geo_data(ip_address)
    headers = request.headers
    threat_score = calculate_fingerprint_score(headers)
    logging.info(f"IP Address: {ip_address}, Geo Data: {geo_data}, Threat Score: {threat_score}")
    # Persist honeypot hit to local database with consistent format
    try:
        ts = datetime.utcnow().isoformat() + "Z"
        user_agent = request.headers.get("User-Agent")
        with open("database.txt", "a", encoding="utf-8") as f:
            f.write(
                f"---\n"
                f"⏰ Data: {ts}\n"
                f"❌ Tip: Honeypot hit\n"
                f"🌐 IPweb: {ip_address}\n"
                f"🖥️ User-Agent: {user_agent}\n"
                f"🧮 Threat Score: {threat_score}\n"
                f"---\n"
            )
    except Exception:
        logging.exception("Failed to persist honeypot hit to database.txt")
    # Notify Discord about honeypot hit
    try:
        ts = datetime.utcnow().isoformat() + "Z"
        geo_summary = ", ".join([f"{k}:{v}" for k, v in (geo_data or {}).items()])
        send_to_discord(
            DISCORD_NOTIFY_USERNAME,
            f"[Honeypot] @Admin Probe detected\n⏰ {ts}\n🌐 IP: {ip_address}\n📍 Geo: {geo_summary}\n🧮 Threat Score: {threat_score}"
        )
    except Exception:
        logging.exception("Failed sending honeypot notification")
    return {
        "geo_data": geo_data,
        "threat_score": threat_score
    }

@app.route("/view-database")
def view_database():
    is_admin = session.get("is_admin", False)
    email = session.get("email")
    if is_admin and email == SUDO_EMAIL:
        with open("database.txt", "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()
        safe_content = Markup(escape(raw).replace("\n", "<br>"))
        return f"""
        <h2>Conținutul bazei de date:</h2>
        <div style="background:#f4f6fa;padding:15px;border-radius:8px;">{safe_content}</div>
        <p><a href="/dashboard">Înapoi la dashboard</a></p>
        """
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)