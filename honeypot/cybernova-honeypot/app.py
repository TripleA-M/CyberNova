from flask import Flask, request, render_template
import logging
from geoip.geoip_utils import get_geo_data
from scoring.scoring_utils import calculate_fingerprint_score

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

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