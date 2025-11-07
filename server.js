// Import required packages
import express from 'express';
import fetch from 'node-fetch'; // For making requests to Discord
import cors from 'cors'; // To allow requests from your frontend

const app = express();
const PORT = process.env.PORT || 3000;

// --- IMPORTANT ---
// Store your secret Webhook URL as an environment variable.
// DO NOT hard-code it in your file like this for production.
// Example: process.env.DISCORD_WEBHOOK_URL
const DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/143629365451c4765877/gRFc_p-wj2BMU2-Ty8veSkKiH_CHrIxsFQBlXuVwsr_tE02XSnvBD7XbXJEJ1kM9ekSV;

// --- Middleware ---
// 1. Allow Cross-Origin Requests (from your website)
app.use(cors());
// 2. Parse JSON bodies (from your website's fetch request)
app.use(express.json());

// --- Routes ---
// 1. A simple test route
app.get('/', (req, res) => {
  res.send('Backend server is running!');
});

// 2. The main endpoint to receive messages from your frontend
app.post('/send-to-discord', async (req, res) => {
  const { username, message } = req.body;

  if (!message || !username) {
    return res.status(400).json({ error: 'Username and message are required.' });
  }

  // Create the payload for the Discord Webhook
  const discordPayload = {
    username: username, // You can customize the bot's name
    avatar_url: '', // You can add a URL to a custom avatar
    content: message,
  };

  try {
    // Send the POST request to Discord
    const response = await fetch(DISCORD_WEBHOOK_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(discordPayload),
    });

    if (response.ok) {
      // Discord accepted the message
      res.status(200).json({ success: true, message: 'Message sent to Discord!' });
    } else {
      // Discord returned an error
      console.error('Discord API Error:', await response.text());
      res.status(500).json({ error: 'Failed to send message to Discord.' });
    }
  } catch (error) {
    console.error('Error sending message to Discord:', error);
    res.status(500).json({ error: 'Internal server error.' });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
  console.log('Remember to replace the DISCORD_WEBHOOK_URL with your secret URL.');
});