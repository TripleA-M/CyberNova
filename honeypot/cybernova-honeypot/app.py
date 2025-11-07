from flask import Flask, request, render_template, redirect, session, url_for
import logging
import os
import secrets
from datetime import timedelta, datetime
from dotenv import load_dotenv, find_dotenv

from geoip.geoip_utils import get_geo_data
from scoring.scoring_utils import calculate_fingerprint_score

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
GLOBAL_STATIC_DIR = os.path.join(BASE_DIR, 'static')

load_dotenv(find_dotenv())  # load environment variables from nearest .env if present

app = Flask(
    __name__,
    static_folder=GLOBAL_STATIC_DIR,
    template_folder='templates'
)

# Prefer FLASK_SECRET_KEY from environment; fall back to ephemeral dev key (not for production)
_env_secret = os.getenv("FLASK_SECRET_KEY")
if not _env_secret:
    _env_secret = secrets.token_hex(32)
    logging.warning("FLASK_SECRET_KEY not set; using a temporary in-memory key. Set it in a .env file or environment for production.")
app.secret_key = _env_secret
app.permanent_session_lifetime = timedelta(minutes=10)

logging.basicConfig(level=logging.INFO)

# Store failed login attempts in memory (for demo; use DB for production)
failed_logins = {}

@app.route("/", methods=["GET", "POST"])
def index():
    # show error message if provided via query string or session
    error = request.args.get("error") or session.pop("error", None)

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_agent = request.headers.get("User-Agent")
        ip_address = request.remote_addr

        # Demo: Accept only password "123456"
        if password == "123456":
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
            # redirect to failed-login endpoint which will redirect back to index with message
            return redirect(url_for("failed_login"))

    return render_template("index.html", error=error)



@app.route("/dashboard")
def dashboard():
    email = session.get("email")
    password = session.get("password")
    user_agent = session.get("user_agent")
    # ip_address is stored but not displayed
    if email and password:
        return f"""
        <h2>Bine ai venit, {email}!</h2>
        <p>Parola ta: {password}</p>
        <p>User-Agent: {user_agent}</p>
        <p>Datele tale vor fi reținute 10 minute.</p>
        """
    return redirect("/")

@app.route("/failed-login")
def failed_login():
    ip = session.get("failed_ip")
    user_agent = session.get("failed_user_agent")
    with open("database.txt", "a") as f:
        f.write(f"Failed login attempt - IP: {ip}, User-Agent: {user_agent}\n")
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

if __name__ == "__main__":
    app.run(debug=True)