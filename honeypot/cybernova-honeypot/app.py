from flask import Flask, request, render_template, redirect, session, url_for, send_file
import logging
import os
from datetime import timedelta, datetime

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

SUDO_EMAIL = "tripelA&M@gmail.com"
SUDO_PASSWORD = "AndreiAntonio2xMarius"

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
    # try to use timestamp stored in memory, otherwise use current UTC time
    ts = None
    if ip and ip in failed_logins:
        ts_obj = failed_logins[ip].get("timestamp")
        if ts_obj:
            ts = ts_obj.isoformat() + "Z" if isinstance(ts_obj, datetime) else str(ts_obj)
        if not ts:
            ts = datetime.utcnow().isoformat() + "Z"

    with open("database.txt", "a") as f:
        f.write(f"{ts} - Failed login attempt - IP: {ip}, User-Agent: {user_agent}\n")
    # Redirect back to the main page and show "Wrong Password"
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
            content = f.read().replace("\n", "<br>")
        return f"""
        <h2>Conținutul bazei de date:</h2>
        <div style="background:#f4f6fa;padding:15px;border-radius:8px;">{content}</div>
        <p><a href="/dashboard">Înapoi la dashboard</a></p>
        """
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)