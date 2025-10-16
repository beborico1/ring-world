# The Ring World - Project Documentation

## Key Findings

### Project Overview
- **Type**: Pygame-based game with AI and networking capabilities
- **Main Entry Point**: `src/main.py`
- **AI Model**: Uses TensorFlow/Keras (model file: `game_model.keras`)
- **Network Features**: WebSocket-based multiplayer support

### Dependencies
The project requires the following Python packages:
- `pygame` - Game engine and graphics
- `tensorflow` - Machine learning/AI player
- `websockets` - Network multiplayer functionality

### Setup Instructions

#### 1. Create Virtual Environment
```bash
cd /Users/luisrico/dev/irvine/2024/Luis_Rico/Extra/the-ring-world
python3 -m venv venv
```

#### 2. Install Dependencies
```bash
source venv/bin/activate
pip install pygame tensorflow websockets
```

#### 3. Run the Game
```bash
source venv/bin/activate
python -m src.main
```

### Project Structure
```
the-ring-world/
├── assets/           # Game assets
├── game_model.keras  # Pre-trained AI model
├── saves/            # Saved game states
├── src/
│   ├── ai/          # AI player implementation
│   ├── controllers/ # Game controllers
│   ├── handlers/    # Event handlers
│   ├── managers/    # Game managers (render, network, save/load)
│   ├── renderers/   # Rendering systems
│   ├── systems/     # Game systems (circle, menu)
│   ├── utils/       # Utility functions
│   ├── game.py      # Main game class
│   └── main.py      # Entry point
└── venv/            # Virtual environment (created)
```

### Notable Components
- **GameController**: Central game coordination (`src/controllers/game_controller.py`)
- **StrategicAIPlayer**: AI opponent using trained Keras model (`src/ai/strategic_ai_player.py`)
- **NetworkManager**: WebSocket-based multiplayer (`src/managers/network/network_manager.py`)
- **CircleSystem**: Core game mechanics (`src/systems/circle_system.py`)
- **SaveLoadManager**: Game state persistence (`src/managers/save_load_manager.py`)

### Known Issues
- Minor deprecation warning from pygame's use of `pkg_resources` (harmless, can be ignored)

### Quick Start Command
For future runs, use this one-liner from the project directory:
```bash
source venv/bin/activate && python -m src.main
```

---
*Documentation generated on 2025-10-14*
