# Ring World WebSocket Server

This is the WebSocket server for the Ring World multiplayer game.

## Deployment to Railway

### Step 1: Install Railway CLI (if not already installed)
```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway
```bash
railway login
```

### Step 3: Initialize and Deploy
```bash
cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world/server
railway init
railway up
```

### Step 4: Get the Deployment URL
After deployment, Railway will provide you with a URL. You need to update the client configuration.

1. Go to your Railway dashboard
2. Find your project
3. Copy the deployment URL (it will look like: `https://your-project.up.railway.app`)
4. Update the client configuration in `../src/utils/settings.py`:
   - Change `NETWORK_CONFIG["URL"]` from `wss://ring-world-production.up.railway.app` to your new URL
   - Make sure to use `wss://` (WebSocket Secure) instead of `https://`

Example:
```python
NETWORK_CONFIG: Dict[str, Any] = {
    "URL": "wss://your-project.up.railway.app",
    # ... rest of config
}
```

## Local Testing

To test the server locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

The server will run on `ws://localhost:8765` by default.

To test locally, update the client settings temporarily:
```python
"URL": "ws://localhost:8765",
```

## Alternative Deployment Options

### Render.com
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python server.py`
4. Deploy

### Heroku
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`

## Environment Variables

The server uses the following environment variable:
- `PORT`: The port to run the server on (automatically set by Railway)

## Server Features

- Room-based multiplayer (2 players per room)
- Automatic color assignment (red/blue)
- Move synchronization
- Disconnect handling
- Reconnection support
