# Complete Deployment Guide for Ring World

This guide covers deploying both the game client (web version) and the multiplayer server.

## Part 1: Deploy the WebSocket Server (for Online Multiplayer)

### Option A: Deploy to Railway (Recommended)

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Navigate to server directory**:
```bash
cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world/server
```

3. **Login to Railway**:
```bash
railway login
```

4. **Initialize and Deploy**:
```bash
railway init
railway up
```

5. **Get your deployment URL**:
   - Go to https://railway.app/dashboard
   - Find your project
   - Copy the deployment URL (e.g., `https://ring-world-production.up.railway.app`)

6. **Update the client configuration**:
   - Edit `src/utils/settings.py`
   - Update the NETWORK_CONFIG URL:
   ```python
   NETWORK_CONFIG: Dict[str, Any] = {
       "URL": "wss://your-project.up.railway.app",  # Replace with your URL
       "RECONNECT_DELAY": 5,
       "MAX_RECONNECT_ATTEMPTS": 5,
       "HEARTBEAT_INTERVAL": 30,
   }
   ```
   - **Important**: Use `wss://` (not `https://`)

### Option B: Deploy to Render

1. Create account at https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: ring-world-server
   - **Root Directory**: server
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
5. Click "Create Web Service"
6. Copy the deployment URL and update client settings as above

## Part 2: Deploy the Game (Web Version)

### Method 1: Automatic Deployment with GitHub Actions (Recommended)

1. **Create GitHub Repository**:
```bash
cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"
```

2. **Create repository on GitHub**:
   - Go to https://github.com/new
   - Name it "ring-world" or similar
   - Don't initialize with README
   - Click "Create repository"

3. **Push to GitHub**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/ring-world.git
git branch -M main
git push -u origin main
```

4. **Enable GitHub Pages**:
   - Go to repository Settings
   - Navigate to "Pages" section
   - Under "Source", select "GitHub Actions"
   - The workflow will automatically build and deploy

5. **Access your game**:
   - Wait for the GitHub Action to complete (check Actions tab)
   - Your game will be available at: `https://YOUR_USERNAME.github.io/ring-world/`

### Method 2: Manual Deployment to GitHub Pages

1. **Build the web version**:
```bash
cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world
source venv/bin/activate
python -m pygbag main.py
```

2. **Create gh-pages branch**:
```bash
# If you haven't already initialized git
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ring-world.git
git push -u origin main

# Create gh-pages branch
git checkout --orphan gh-pages
git rm -rf .
```

3. **Copy build files**:
```bash
cp -r build/web/* .
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages
```

4. **Configure GitHub Pages**:
   - Go to repository Settings → Pages
   - Set source to `gh-pages` branch
   - Click Save

5. **Access your game**:
   - Your game will be at: `https://YOUR_USERNAME.github.io/ring-world/`

### Method 3: Deploy to Itch.io

1. **Build the web version**:
```bash
source venv/bin/activate
python -m pygbag main.py
```

2. **Create a ZIP file**:
```bash
cd build
zip -r ring-world-web.zip web/
```

3. **Upload to Itch.io**:
   - Go to https://itch.io/game/new
   - Fill in game details
   - Under "Uploads", upload `ring-world-web.zip`
   - Set "Kind of project" to "HTML"
   - Check "This file will be played in the browser"
   - Set viewport: 1280x800 (or your preferred size)
   - Publish!

## Part 3: Testing Everything

### Test the Server

1. **Test locally first**:
```bash
cd server
pip install -r requirements.txt
python server.py
```

2. **Update client to use local server**:
   - Temporarily change URL in `src/utils/settings.py` to `"ws://localhost:8765"`
   - Run the game locally
   - Try the Online mode

3. **Test deployed server**:
   - Update URL to your deployed server (with `wss://`)
   - Test from the web version

### Test the Web Version

1. **Test locally**:
   - After building with Pygbag, it should open automatically at `http://localhost:8000`
   - Test all game modes (except AI - not supported in web)

2. **Test deployed version**:
   - Visit your GitHub Pages or Itch.io URL
   - Test all functionality
   - Check browser console for errors (F12)

## Troubleshooting

### Server Issues

**"Connection failed" or "Can't connect to server"**:
- Verify server is running: visit `https://your-server-url` in browser
- Check you're using `wss://` (not `ws://` or `https://`)
- Ensure server has been deployed successfully

**"Room full" message**:
- Each room only supports 2 players
- Try a different room code

### Web Version Issues

**"Black screen" or "Game won't load"**:
- Check browser console for errors (F12)
- Ensure assets are loading correctly
- Try a different browser (Chrome/Firefox recommended)

**"AI mode not working"**:
- This is expected - TensorFlow is not supported in web version
- Consider hiding AI mode button in web version

**"Online mode not working in web version"**:
- Ensure server uses HTTPS/WSS (required for browser security)
- Check CORS settings on server if needed

## Next Steps

After deployment:

1. **Update README.md** with your live URLs
2. **Test both local and web versions** thoroughly
3. **Share the link** with friends to test multiplayer
4. **Monitor server usage** on Railway/Render dashboard

## Cost Considerations

- **Railway**: Free tier includes 500 hours/month
- **Render**: Free tier available with limitations
- **GitHub Pages**: Completely free for public repositories
- **Itch.io**: Free hosting for games

## Security Notes

- The server implementation is basic and suitable for casual games
- For production use, consider adding:
  - Authentication
  - Rate limiting
  - Input validation
  - Logging and monitoring
  - Database for game state persistence

## Maintenance

**Keeping server alive**:
- Free tier servers may sleep after inactivity
- First connection might be slow (wake-up time)
- Consider upgrading to paid tier for always-on server

**Updating the game**:
- Push changes to GitHub
- GitHub Actions will auto-deploy (if using that method)
- For manual deployment, rebuild and redeploy

## Resources

- **Pygbag Documentation**: https://pygame-web.github.io/
- **Railway Docs**: https://docs.railway.app/
- **GitHub Pages Docs**: https://docs.github.com/pages
- **WebSocket Documentation**: https://websockets.readthedocs.io/
