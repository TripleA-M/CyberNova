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

## Usage
Run the application using the following command:

```bash
python app.py
```

The application will start a Flask server, and you can access it via `http://localhost:5000`.

### Discord Notifications (Webhook Integration)
Failed login attempts are appended to `database.txt` and simultaneously forwarded to a Discord channel via a local Node.js relay (`server.js`).

1. Create a Discord Webhook (Server Settings → Integrations → Webhooks) and copy its URL.
2. In the repository root (same level as `package.json`), create a `.env` file containing:
	```env
	DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/XXXXXXXX/YYYYYYYY
	```
3. Start the relay service (from repo root or the `cybernova-honeypot` directory):
	```bash
	node server.js
	```
4. (Optional) If the relay runs on a different host/port, set the environment variable for the Flask app before starting it:
	```bash
	set DISCORD_PROXY_URL=http://localhost:3000/send-to-discord  # Windows PowerShell: $env:DISCORD_PROXY_URL="http://localhost:3000/send-to-discord"
	```
5. Launch the Flask honeypot:
	```bash
	python app.py
	```

When an incorrect password is submitted (anything except `123456`), a log line is saved to `database.txt` and pushed to Discord with the username `CyberNova Honeypot`.

If the relay or Discord is unreachable, the application continues running; errors are logged to the console.

## GeoIP Functionality
The application utilizes the GeoIP API to retrieve geographical data based on the IP addresses of incoming requests. This information can be used to analyze the origin of the traffic.

## Scoring Logic
The scoring system assigns a threat score from 0 to 10 based on the presence or absence of specific HTTP headers and user-agent detection. This scoring helps in identifying potentially malicious requests.

## Contributing
Contributions to the project are welcome. Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

