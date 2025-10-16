# Ring World - Web Deployment Guide

This guide explains how to build and host the Ring World game on the web using Pygbag.

## Prerequisites

- Python 3.10 or higher
- Pygbag installed (`pip install pygbag`)

## Building for Web

### Step 1: Build the Web Version

From the project root directory, run:

```bash
cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world
python -m pygbag .
```

This will:
1. Create a `build/web` directory
2. Convert your Pygame code to WebAssembly
3. Generate HTML and JavaScript files

### Step 2: Test Locally

Pygbag automatically starts a local server after building. The game will be available at:
```
http://localhost:8000
```

If you need to restart the server:
```bash
python -m pygbag . --build
```

## Hosting Options

### Option 1: GitHub Pages (Recommended)

1. **Initialize Git Repository** (if not already done):
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Create GitHub Repository**:
   - Go to GitHub and create a new repository named `ring-world`
   - Don't initialize with README (we already have files)

3. **Push to GitHub**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/ring-world.git
git branch -M main
git push -u origin main
```

4. **Build and Deploy**:
```bash
# Build the web version
python -m pygbag . --build

# Create a gh-pages branch
git checkout -b gh-pages

# Copy build files to root
cp -r build/web/* .

# Commit and push
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages
```

5. **Enable GitHub Pages**:
   - Go to your repository settings
   - Navigate to "Pages"
   - Set source to `gh-pages` branch
   - Your game will be live at: `https://YOUR_USERNAME.github.io/ring-world/`

### Option 2: Itch.io

1. Build the web version:
```bash
python -m pygbag . --build
```

2. Compress the `build/web` folder:
```bash
cd build
zip -r ring-world-web.zip web/
```

3. Upload to Itch.io:
   - Go to https://itch.io/game/new
   - Upload the `ring-world-web.zip` file
   - Set "Kind of project" to "HTML"
   - Check "This file will be played in the browser"
   - Set viewport dimensions (recommended: 1280x800)
   - Publish!

### Option 3: Netlify

1. Build the web version:
```bash
python -m pygbag . --build
```

2. Install Netlify CLI:
```bash
npm install -g netlify-cli
```

3. Deploy:
```bash
cd build/web
netlify deploy --prod
```

## Important Notes

### TensorFlow/Keras Limitation

The AI mode (neural network) will NOT work in the web version because:
- TensorFlow is not supported in Pygbag/WebAssembly
- The `game_model.keras` file cannot be loaded in the browser

**Recommended**: Remove AI mode from the web version menu, or show a "Not available in web version" message.

### WebSocket Limitations

For the online multiplayer to work in the web version:
1. The WebSocket server must use WSS (secure WebSocket)
2. Update `src/utils/settings.py` to use your deployed server URL
3. The server must have valid SSL certificates

### Optimizing for Web

To reduce load times:

1. **Reduce Asset Sizes**:
   - Compress images
   - Use smaller sound files
   - Reduce model sizes

2. **Remove Unused Files**:
   - Comment out AI imports if not using
   - Remove unused assets

## Troubleshooting

### Build Fails

If the build fails:
```bash
# Clean build directory
rm -rf build/

# Try building again with verbose output
python -m pygbag . --build --PYBUILD=3.11
```

### Game Doesn't Load

1. Check browser console for errors (F12)
2. Ensure all imports are compatible with Pygbag
3. Check that all file paths are relative

### Black Screen

If you see a black screen:
1. Check that Pygame initialization is correct
2. Verify screen dimensions
3. Check browser console for JavaScript errors

## Performance Tips

1. **Reduce FPS for Web**: In web version, 30-60 FPS is recommended
2. **Simplify Graphics**: Use simpler rendering for better performance
3. **Async/Await**: Ensure proper `await asyncio.sleep(0)` in main loop

## File Structure After Build

```
build/web/
├── index.html          # Main HTML file
├── game.html          # Game container
├── pygame-script.js   # Pygame WebAssembly loader
├── archive/           # Compiled game code
└── assets/            # Game assets
```

## Resources

- Pygbag Documentation: https://pygame-web.github.io/
- Pygame Web Examples: https://github.com/pygame-web/pygbag
- WebAssembly Limitations: https://pygame-web.github.io/wiki/pygbag/
