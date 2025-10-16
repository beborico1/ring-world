# The Ring World

A strategic board game built with Pygame featuring AI opponents and online multiplayer.

![Ring World](assets/icon.png)

## Features

- **Offline Mode**: Play locally against yourself or a friend
- **AI Mode**: Challenge an AI opponent powered by a trained neural network
- **Training Mode**: Watch AI agents learn and improve
- **Online Multiplayer**: Play against other players over the internet (requires server)

## Quick Start

### Play Online

Visit the live web version: [Your GitHub Pages URL will be here after deployment]

### Run Locally

1. **Install Dependencies**:
```bash
cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world
source venv/bin/activate
pip install pygame tensorflow websockets
```

2. **Run the Game**:
```bash
python -m src.main
```

## Web Deployment

The game can be played directly in the browser using WebAssembly.

### Automatic Deployment (GitHub Pages)

1. Push your code to GitHub
2. Enable GitHub Pages in repository settings
3. The GitHub Action will automatically build and deploy

See [WEB_DEPLOYMENT.md](WEB_DEPLOYMENT.md) for detailed instructions.

## Online Multiplayer Setup

To enable online multiplayer, you need to deploy the WebSocket server.

### Deploy Server to Railway

1. **Navigate to server directory**:
```bash
cd server
```

2. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

3. **Deploy**:
```bash
railway login
railway init
railway up
```

4. **Update Client Configuration**:
After deployment, update `src/utils/settings.py` with your server URL:
```python
NETWORK_CONFIG: Dict[str, Any] = {
    "URL": "wss://your-project.up.railway.app",
    # ...
}
```

See [server/README.md](server/README.md) for detailed server deployment instructions.

## Project Structure

```
the-ring-world/
├── assets/              # Game assets (images, sounds)
├── src/                 # Source code
│   ├── ai/             # AI player implementation
│   ├── controllers/    # Game controllers
│   ├── handlers/       # Event handlers
│   ├── managers/       # Game managers
│   ├── renderers/      # Rendering systems
│   ├── systems/        # Game systems
│   ├── utils/          # Utility functions
│   ├── game.py         # Main game class
│   └── main.py         # Entry point (desktop)
├── server/             # WebSocket server for multiplayer
├── saves/              # Saved game states
├── main.py             # Entry point (web version)
└── game_model.keras    # Trained AI model

```

## Development

### Local Development

```bash
# Activate virtual environment
source venv/bin/activate

# Run the game
python -m src.main
```

### Build Web Version

```bash
# Build for web
python -m pygbag main.py

# The build will be available at build/web/
# Open index.html in a browser or use the local server that Pygbag starts
```

## Technologies

- **Pygame**: Game engine and graphics
- **TensorFlow/Keras**: AI opponent
- **WebSockets**: Online multiplayer
- **Pygbag**: Web deployment (WebAssembly)

## Known Limitations

### Web Version

- AI mode is not available (TensorFlow not supported in WebAssembly)
- Online multiplayer requires a deployed WebSocket server with SSL

## Contributing

This project was created as part of the Irvine internship program.

## License

[Add your license here]

## Credits

Developed by Luis Rico

## Support

For issues or questions, please open an issue on GitHub.
