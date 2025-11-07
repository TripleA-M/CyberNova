# CyberNova Honeypot Application

## Overview
The CyberNova Honeypot application is designed to attract and analyze malicious traffic. It serves as a decoy to gather information about potential threats and helps in understanding attack patterns.

## Project Structure
The project is organized as follows:

```
cybernova-honeypot
├── app.py                # Main entry point of the Flask application
├── requirements.txt      # Lists project dependencies
├── geoip                 # Contains GeoIP utility functions
│   └── geoip_utils.py    # Functions to retrieve geographical data based on IP
├── scoring               # Contains scoring utility functions
│   └── scoring_utils.py   # Functions to calculate threat scores based on headers
├── templates             # Contains HTML templates
│   └── index.html        # Placeholder for the main HTML template
├── static                # Contains static files like CSS
│   └── styles.css        # CSS styles for the application
└── README.md             # Documentation for the project
```

## Installation
To set up the project, clone the repository and install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Configuration (Secret Key)
This app uses Flask sessions and requires a secret key. Do NOT hardcode it.

1) Create your local `.env` file from the example:

```bash
cp ../../.env.example ../../.env
```

2) Generate a secure key (PowerShell):

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

3) Put the generated value in `../../.env` as `FLASK_SECRET_KEY=...`.

## Usage
Run the application using the following command:

```bash
python app.py
```

The application will start a Flask server, and you can access it via `http://localhost:5000`.

## GeoIP Functionality
The application utilizes the GeoIP API to retrieve geographical data based on the IP addresses of incoming requests. This information can be used to analyze the origin of the traffic.

## Scoring Logic
The scoring system assigns a threat score from 0 to 10 based on the presence or absence of specific HTTP headers and user-agent detection. This scoring helps in identifying potentially malicious requests.

## Contributing
Contributions to the project are welcome. Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

