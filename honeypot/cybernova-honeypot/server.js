import express from 'express';
import fetch from 'node-fetch';
import cors from 'cors';
import { config as dotenvConfig } from 'dotenv';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootEnvPath = path.resolve(__dirname, '../../.env');
dotenvConfig({ path: rootEnvPath });

const app = express();
const PORT = process.env.PORT || 3000;
const ADMIN_ROLE_ID = process.env.ADMIN_ROLE_ID;

const DISCORD_WEBHOOK_URL = process.env.DISCORD_WEBHOOK_URL;
if (!DISCORD_WEBHOOK_URL) {
  throw new Error("Missing DISCORD_WEBHOOK_URL environment variable");
}

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.send('Backend server is running!');
});

app.post('/send-to-discord', async (req, res) => {
  const { username, message } = req.body;

  if (!message || !username) {
    return res.status(400).json({ error: 'Username and message are required.' });
  }

  let content = message;
  if (ADMIN_ROLE_ID) {
    content = `<@&${ADMIN_ROLE_ID}> ${message}`;
  }

  const discordPayload = {
    username: username,
    avatar_url: '',
    content,
    ...(ADMIN_ROLE_ID
      ? { allowed_mentions: { parse: [], roles: [ADMIN_ROLE_ID] } }
      : {}),
  };

  try {
    const response = await fetch(DISCORD_WEBHOOK_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(discordPayload),
    });

    if (response.ok) {
      res.status(200).json({ success: true, message: 'Message sent to Discord!' });
    } else {
      console.error('Discord API Error:', await response.text());
      res.status(500).json({ error: 'Failed to send message to Discord.' });
    }
  } catch (error) {
    console.error('Error sending message to Discord:', error);
    res.status(500).json({ error: 'Internal server error.' });
  }
});

app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
  console.log('Remember to replace the DISCORD_WEBHOOK_URL with your secret URL.');
});