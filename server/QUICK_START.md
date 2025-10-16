# Quick Start: Deploy Server in 5 Minutes

## Option 1: Render.com (Easiest)

**No CLI needed, just a web browser!**

### Step 1: Push to GitHub

```bash
cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world

# If not already a git repo
git init
git add .
git commit -m "Add Ring World server"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/ring-world.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to https://render.com and sign up (free, use GitHub login)
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect GitHub"** → Select your `ring-world` repository
4. Fill in:
   - **Name**: `ring-world-server`
   - **Root Directory**: `server`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
5. Click **"Create Web Service"**
6. Wait 2-3 minutes for deployment
7. Copy your URL (e.g., `https://ring-world-server.onrender.com`)

### Step 3: Update Your Game

Edit `/Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world/src/utils/settings.py`:

```python
NETWORK_CONFIG: Dict[str, Any] = {
    "URL": "wss://ring-world-server.onrender.com",  # Your Render URL
    "RECONNECT_DELAY": 5,
    "MAX_RECONNECT_ATTEMPTS": 5,
    "HEARTBEAT_INTERVAL": 30,
}
```

### Done! 🎉

Test by running your game and selecting "Online" mode.

---

## Option 2: Ngrok (Fastest for Testing)

**Perfect for immediate testing without deployment**

### Step 1: Install Ngrok

```bash
brew install ngrok
```

### Step 2: Run Server Locally

```bash
cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world/server
pip install -r requirements.txt
python server.py
```

Keep this terminal open.

### Step 3: Expose with Ngrok

Open a **new terminal**:

```bash
ngrok http 8765
```

### Step 4: Copy URL

Look for the line like:
```
Forwarding   https://abc123.ngrok.io -> http://localhost:8765
```

Copy the `https://` URL.

### Step 5: Update Game

Edit `src/utils/settings.py`:

```python
"URL": "wss://abc123.ngrok.io",  # Your ngrok URL
```

### Done! 🎉

**Note**: Your computer must stay on, and the URL changes each time you restart ngrok.

---

## Option 3: Fly.io (Best Performance)

**No sleep, better for production**

### Step 1: Install & Login

```bash
# Install
brew install flyctl

# Sign up (or login)
flyctl auth signup
# or: flyctl auth login
```

### Step 2: Deploy

```bash
cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world/server

# Launch (follow prompts, press Enter for defaults)
flyctl launch

# Deploy
flyctl deploy
```

### Step 3: Get URL

```bash
flyctl status
```

Copy the hostname (e.g., `ring-world-server.fly.dev`)

### Step 4: Update Game

```python
"URL": "wss://ring-world-server.fly.dev",
```

### Done! 🎉

---

## Troubleshooting

### "Can't connect to server"

1. **Check URL format**: Must be `wss://` (not `ws://` or `https://`)
2. **Wait 30-60 seconds**: Free servers sleep, first connection is slow
3. **Check server logs**: In Render/Fly dashboard
4. **Test server directly**: Visit `https://your-server-url` in browser

### "Connection refused"

1. Server might be sleeping (Render/Glitch)
2. Try again in 30 seconds
3. Check if deployment succeeded in dashboard

### "SSL certificate error"

1. Use `wss://` (not `ws://`)
2. Ensure server has SSL (all platforms above provide it)
3. Check browser console (F12) for specific error

---

## Which One Should I Use?

**For testing now**: Use **Ngrok** (2 minutes setup)

**For production**: Use **Render** (5 minutes setup, no CLI needed)

**For best performance**: Use **Fly.io** (requires credit card but free tier)

---

## Next Steps

After server is deployed:

1. ✅ Test online mode in desktop version
2. ✅ Rebuild and deploy web version
3. ✅ Share game with friends!

See `FREE_HOSTING_ALTERNATIVES.md` for more options and details.
