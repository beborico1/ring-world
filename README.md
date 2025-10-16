# The Ring World

A strategic board game built with Pygame featuring AI opponents and online multiplayer.

![Ring World](assets/icon.png)

## Features

- **Offline Mode**: Play locally against yourself or a friend
- **AI Mode**: Challenge an AI opponent powered by a trained neural network
- **Training Mode**: Watch AI agents learn and improve
- **Online Multiplayer**: Play against other players over the internet (requires server)

## Quick Start

### Play Now (Desktop - Recommended)

**Download and play the full-featured desktop version with AI and online multiplayer!**

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

## Online Multiplayer

**Multiplayer server is LIVE!** ✅

The game connects to: `wss://ring-world-server.onrender.com`

To play online:
1. Run the game locally (`python -m src.main`)
2. Select "Online" mode
3. Enter a room code to create/join a game
4. Share the room code with a friend!

**Note**: The server sleeps after 15 min of inactivity (free tier). First connection may take 30-60 seconds to wake up.

### Want to deploy your own server?

See [server/README.md](server/README.md) and [server/FREE_HOSTING_ALTERNATIVES.md](server/FREE_HOSTING_ALTERNATIVES.md) for deployment options.

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
