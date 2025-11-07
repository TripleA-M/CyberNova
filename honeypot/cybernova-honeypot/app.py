from flask import Flask, request, render_template, redirect, session
import logging
import os
from datetime import timedelta
from geoip.geoip_utils import get_geo_data
from scoring.scoring_utils import calculate_fingerprint_score

# Configure Flask to use the ROOT project's `static` directory so the top-level
# `static/styles.css` is the one served. This allows `url_for('static', filename='styles.css')`
# in templates to resolve to the global stylesheet.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
GLOBAL_STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(
    __name__,
    static_folder=GLOBAL_STATIC_DIR,  # Serve the root static directory
    template_folder='templates'       # Keep templates local
)

app.secret_key = "supersecretkey"
app.permanent_session_lifetime = timedelta(minutes=10)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session.permanent = True
        session["email"] = request.form["email"]
        session["password"] = request.form["password"]
        session["user_agent"] = request.headers.get("User-Agent")
        return redirect("/dashboard")
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    email = session.get("email")
    password = session.get("password")
    user_agent = session.get("user_agent")
    if email and password:
        return f"""
        <h2>Bine ai venit, {email}!</h2>
        <p>Parola ta: {password}</p>
        <p>User-Agent: {user_agent}</p>
        <p>Datele tale vor fi reținute 10 minute.</p>
        """
    return redirect("/")

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