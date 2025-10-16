# Free Hosting Alternatives for Ring World Server

Railway trial expired? No problem! Here are several **completely free** alternatives.

## 🏆 Recommended: Render.com

**Best for:** Production-ready, reliable, automatic SSL

### Steps:

1. **Sign up**: https://render.com
2. **Prepare your code**:
   ```bash
   cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world

   # Initialize git if needed
   git init
   git add .
   git commit -m "Add server"

   # Create GitHub repo and push
   git remote add origin https://github.com/YOUR_USERNAME/ring-world.git
   git push -u origin main
   ```

3. **Deploy on Render**:
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - **Name**: ring-world-server
     - **Root Directory**: `server`
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python server.py`
   - Click "Create Web Service"

4. **Get your URL**:
   - After deployment, copy the URL (e.g., `https://ring-world-server.onrender.com`)
   - Update client: `src/utils/settings.py`
   ```python
   "URL": "wss://ring-world-server.onrender.com",
   ```

**Pros:**
- ✅ Free tier: 750 hours/month
- ✅ Automatic SSL (wss://)
- ✅ Easy setup
- ✅ Custom domains

**Cons:**
- ⚠️ Sleeps after 15 min inactivity (30-60s wake time)

---

## 🚀 Fly.io

**Best for:** No sleep, better performance

### Steps:

1. **Install Fly CLI**:
   ```bash
   brew install flyctl  # macOS
   # or: curl -L https://fly.io/install.sh | sh
   ```

2. **Sign up and login**:
   ```bash
   flyctl auth signup
   # or if you have account: flyctl auth login
   ```

3. **Deploy**:
   ```bash
   cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world/server

   # Initialize (follow prompts)
   flyctl launch

   # Deploy
   flyctl deploy
   ```

4. **Get URL**:
   ```bash
   flyctl status
   ```
   Use the hostname shown (e.g., `wss://ring-world-server.fly.dev`)

**Pros:**
- ✅ Free tier: 3 VMs, 160GB/month
- ✅ No sleep/pause
- ✅ Better for real-time apps
- ✅ Global deployment

**Cons:**
- ⚠️ Requires credit card (but won't charge on free tier)

---

## 🎨 Glitch.com

**Best for:** Quick testing, simplest setup

### Steps:

1. Go to https://glitch.com
2. Click "New Project" → "glitch-hello-python"
3. Delete default files
4. Upload your server files:
   - `server.py`
   - `requirements.txt`
   - `glitch.json` (already created in this folder)
5. Glitch auto-deploys!
6. Click "Share" → copy the live site URL

**Use in client:**
```python
"URL": "wss://your-project-name.glitch.me",
```

**Pros:**
- ✅ Easiest setup (no CLI needed)
- ✅ Web-based editor
- ✅ Instant preview
- ✅ No credit card required

**Cons:**
- ⚠️ Limited resources
- ⚠️ Project sleeps after 5 min

---

## 🔥 Cyclic.sh

**Best for:** Modern Python hosting

### Steps:

1. Sign up: https://app.cyclic.sh
2. Connect GitHub
3. Select your repository
4. Cyclic auto-detects Python and deploys

**Pros:**
- ✅ Easy GitHub integration
- ✅ Automatic deployments
- ✅ No sleep

**Cons:**
- ⚠️ Newer platform (less proven)

---

## 🏠 Self-Hosting with Ngrok (Development/Testing)

**Best for:** Local development, testing before deploying

### Steps:

1. **Install ngrok**:
   ```bash
   brew install ngrok  # macOS
   # or download from: https://ngrok.com/download
   ```

2. **Sign up** at https://ngrok.com (free)

3. **Set auth token**:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```

4. **Run your server locally**:
   ```bash
   cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world/server
   python server.py
   ```

5. **Expose it** (in another terminal):
   ```bash
   ngrok http 8765
   ```

6. **Use the ngrok URL**:
   - Copy the `Forwarding` URL (e.g., `https://abc123.ngrok.io`)
   - Update client settings:
   ```python
   "URL": "wss://abc123.ngrok.io",
   ```

**Pros:**
- ✅ Completely free
- ✅ No deployment needed
- ✅ Great for testing

**Cons:**
- ⚠️ URL changes each restart (unless paid plan)
- ⚠️ Your computer must stay on
- ⚠️ Not for production

---

## 💻 Self-Hosting on VPS

If you have a VPS (DigitalOcean, Linode, etc.) or access to a server:

### Using Docker:

1. **Create Dockerfile** (already in server folder):
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY server.py .
   EXPOSE 8765
   CMD ["python", "server.py"]
   ```

2. **Build and run**:
   ```bash
   docker build -t ring-world-server .
   docker run -p 8765:8765 ring-world-server
   ```

3. **Set up nginx reverse proxy** with SSL for wss://

---

## 📊 Comparison Table

| Platform | Setup Difficulty | Sleeps? | Free Tier Limit | Credit Card? | Best For |
|----------|-----------------|---------|-----------------|--------------|----------|
| **Render.com** | Easy | Yes (15min) | 750hrs/mo | No | Production |
| **Fly.io** | Medium | No | 3 VMs, 160GB | Yes* | Performance |
| **Glitch** | Very Easy | Yes (5min) | Limited | No | Quick tests |
| **Ngrok** | Easy | No | Unlimited | No | Development |
| **Cyclic** | Easy | No | Limited | No | Modern stack |

*Won't charge on free tier

---

## 🎯 My Recommendation

**For you right now:**

1. **Quick test**: Use **Ngrok** (5 minutes setup)
2. **Production**: Use **Render.com** (best balance of ease + reliability)
3. **Performance**: Use **Fly.io** (if you're okay with credit card requirement)

---

## 🛠️ After Deployment

Once deployed, update your client configuration:

1. **Edit** `src/utils/settings.py`:
```python
NETWORK_CONFIG: Dict[str, Any] = {
    "URL": "wss://your-server-url-here",  # Replace with your URL
    "RECONNECT_DELAY": 5,
    "MAX_RECONNECT_ATTEMPTS": 5,
    "HEARTBEAT_INTERVAL": 30,
}
```

2. **Rebuild web version** (if deployed):
```bash
python -m pygbag main.py
```

3. **Test the connection** in your game's Online mode!

---

## 🐛 Troubleshooting

**Server not responding:**
- Check if it's sleeping (first request may take 30-60s on free tiers)
- Verify you're using `wss://` (not `ws://` or `https://`)
- Check server logs in the hosting dashboard

**Can't connect from web version:**
- Web browsers require SSL (wss://)
- Check browser console for errors (F12)
- Ensure CORS is enabled (usually automatic on these platforms)

**Performance issues:**
- Free tiers may have limited resources
- Consider upgrading to paid tier for production
- Use Fly.io for better performance on free tier

---

## 💡 Pro Tips

1. **Multiple servers**: Deploy to multiple platforms and switch URLs if one goes down
2. **Custom domain**: Most platforms support custom domains (even on free tier)
3. **Monitoring**: Set up UptimeRobot (free) to ping your server every 5 min (prevents sleeping on Render)
4. **Logs**: Always check server logs when debugging connection issues

---

Need help? Check the platform's documentation:
- Render: https://render.com/docs
- Fly.io: https://fly.io/docs
- Glitch: https://glitch.com/help
- Ngrok: https://ngrok.com/docs
