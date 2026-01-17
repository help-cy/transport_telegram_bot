# HelpCy Telegram Bot

A modern, well-structured Telegram bot built with aiogram 3.x following clean architecture principles and SOLID design patterns.

## Features

- ✅ Clean architecture with separated concerns
- ✅ Modular and extensible structure
- ✅ Command handlers (`/start`, `/help`, `/info`)
- ✅ Interactive keyboard buttons
- ✅ Inline keyboards with callbacks
- ✅ Error handling and logging
- ✅ Environment-based configuration
- ✅ Type hints throughout the codebase

## Project Structure

```
helpcy_telegram_bot/
├── src/
│   ├── bot/
│   │   ├── handlers/          # Message and command handlers
│   │   │   ├── start.py       # Start, help, info commands
│   │   │   ├── callback.py    # Callback query handlers
│   │   │   └── messages.py    # Text message handlers
│   │   ├── keyboards/         # Keyboard layouts
│   │   │   ├── reply.py       # Reply keyboard buttons
│   │   │   └── inline.py      # Inline keyboard buttons
│   │   ├── middleware/        # Middleware components
│   │   │   ├── logging.py     # Logging middleware
│   │   │   └── error.py       # Error handling middleware
│   │   └── utils/             # Utility functions
│   │       └── logger.py      # Logger setup
│   ├── config/                # Configuration files
│   │   └── settings.py        # Settings and env variables
│   ├── models/                # Data models
│   │   └── user.py            # User model
│   └── services/              # Business logic services
│       └── bot_service.py     # Main bot service
├── tests/                     # Unit and integration tests
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore rules
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd helpcy_telegram_bot
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and add your bot token:

```env
BOT_TOKEN=your_bot_token_here
LOG_LEVEL=INFO
```

## Usage

### Running the bot

```bash
python main.py
```

### Getting a bot token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the token and paste it into your `.env` file

## Architecture

### Clean Architecture Principles

- **Separation of Concerns**: Each module has a single, well-defined responsibility
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Interface Segregation**: Small, focused interfaces
- **Single Responsibility**: Each class/function does one thing well

### Code Style

- All function arguments are named explicitly
- Each argument is on a new line for better readability
- No inline comments in code
- Self-documenting code with clear naming
- Type hints for all functions

## Development

### Adding new commands

1. Create a handler in `src/bot/handlers/`
2. Register it in `src/services/bot_service.py`
3. Update keyboards if needed

### Adding new keyboards

1. Add keyboard layouts in `src/bot/keyboards/`
2. Import and use in handlers

### Adding middleware

1. Create middleware in `src/bot/middleware/`
2. Register in the bot service

## Testing

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this project for your own purposes.

## Support

For issues and questions, please open an issue on GitHub.
