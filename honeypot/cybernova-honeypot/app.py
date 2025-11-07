from flask import Flask, request, render_template, redirect, session, url_for, send_file
import logging
import os
from datetime import timedelta, datetime
import requests

from geoip.geoip_utils import get_geo_data
from scoring.scoring_utils import calculate_fingerprint_score

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
GLOBAL_STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(
    __name__,
    static_folder=GLOBAL_STATIC_DIR,
    template_folder='templates'
)

app.secret_key = "supersecretkey"
app.permanent_session_lifetime = timedelta(minutes=10)

logging.basicConfig(level=logging.INFO)

# Store failed login attempts in memory (for demo; use DB for production)
failed_logins = {}

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
SUDO_EMAIL = "tripelA&M@gmail.com"
SUDO_PASSWORD = "AndreiAntonio2xMarius"
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
# URL of the local Node.js relay that forwards messages to Discord.
# Configure via env var DISCORD_PROXY_URL; default assumes server.js runs on port 3000.
DISCORD_PROXY_URL = os.getenv("DISCORD_PROXY_URL", "http://localhost:3000/send-to-discord")


def send_to_discord(username: str, message: str) -> None:
    """Best-effort notify the Discord relay service.

    Does not raise on failure; logs errors so the main flow isn't blocked.
    """
    try:
        payload = {"username": username, "message": message}
        resp = requests.post(DISCORD_PROXY_URL, json=payload, timeout=5)
        if resp.status_code >= 400:
            logging.error("Discord relay responded with %s: %s", resp.status_code, resp.text)
        else:
            logging.info("Notified Discord relay successfully")
    except Exception as e:
        logging.exception("Failed to notify Discord relay: %s", e)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

@app.route("/", methods=["GET", "POST"])
def index():
    error = request.args.get("error") or session.pop("error", None)

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_agent = request.headers.get("User-Agent")
        ip_address = request.remote_addr

        # Sudo login
        if email == SUDO_EMAIL and password == SUDO_PASSWORD:
            session.permanent = True
            session["email"] = email
            session["password"] = password
            session["user_agent"] = user_agent
            session["ip_address"] = ip_address
            return redirect("/dashboard")
        else:
            # Save failed login for 30 min
            failed_logins[ip_address] = {
                "user_agent": user_agent,
                "timestamp": datetime.utcnow()
            }
            session["failed_ip"] = ip_address
            session["failed_user_agent"] = user_agent
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=30)
            return redirect(url_for("failed_login"))

    return render_template("index.html", error=error)

@app.route("/dashboard")
def dashboard():
    email = session.get("email")
    password = session.get("password")
    user_agent = session.get("user_agent")
    # ip_address is stored but not displayed
    if email == SUDO_EMAIL and password == SUDO_PASSWORD:
        return f"""
        <h2>Bine ai venit, {email}!</h2>
        <p>Parola ta: {password}</p>
        <p>User-Agent: {user_agent}</p>
        <p>Datele tale vor fi reținute 10 minute.</p>
        <p><a href="/view-database">Vezi baza de date</a></p>
        """
    elif email and password:
        return f"""
        <h2>Bine ai venit, {email}!</h2>
        <p>Parola ta: {password}</p>
        <p>User-Agent: {user_agent}</p>
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

    line = f"{ts} - Failed login attempt - IP: {ip}, User-Agent: {user_agent}"
    with open("database.txt", "a") as f:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        f.write(
            f"---\n"
            f"⏰ Data: {ts}\n"
            f"❌ Tip: Failed login attempt\n"
            f"🌐 IPweb: {ip}\n"
            f"🖥️ User-Agent: {user_agent}\n"
            f"---\n"
        )
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        f.write(line + "\n")

    # Also push this event to Discord via the relay service
    send_to_discord(
        username="CyberNova Honeypot",
        message=line,
    )
    # Redirect back to the main page and show "Wrong Password"
>>>>>>> Stashed changes
    return redirect(url_for("index", error="Wrong Password"))

@app.route('/honeypot', methods=['POST'])
def honeypot():
    ip_address = request.remote_addr
    geo_data = get_geo_data(ip_address)
    headers = request.headers
    threat_score = calculate_fingerprint_score(headers)
    logging.info(f"IP Address: {ip_address}, Geo Data: {geo_data}, Threat Score: {threat_score}")
    return {
        "geo_data": geo_data,
        "threat_score": threat_score
    }

@app.route("/view-database")
def view_database():
    email = session.get("email")
    if email == SUDO_EMAIL:
        with open("database.txt", "r") as f:
            entries = f.read().split("---\n")
        formatted = ""
        for entry in entries:
            if entry.strip():
                formatted += f'<div style="background:#fff;border-radius:8px;padding:15px;margin-bottom:15px;box-shadow:0 2px 8px #222e5020;">{entry.strip().replace(chr(10), "<br>")}</div>'
        return f"""
        <h2>Conținutul bazei de date:</h2>
        {formatted}
        <p><a href="/dashboard">Înapoi la dashboard</a></p>
        """
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)