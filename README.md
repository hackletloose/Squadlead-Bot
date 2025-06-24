# Discord Squadleader Bot

A beginner-friendly Discord bot for organising squads. The bot can pick random squad leaders, create squads, and optionally display the current game map. All configuration is done via slash commands so no manual editing of the code is required.

## Features
- Slash commands to configure the text and voice channels
- `!squadlead` command to choose random squad leaders and split players
- Optional map display using a game server API
- Supports multiple languages (English, German, French, Spanish)
- Works on multiple servers with separate settings

## Requirements
- Python 3.8+
- A Discord bot token
- (Optional) API domain for map information

## Installation
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Squadlead-Bot
   ```
2. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Create a `.env` file**
   ```bash
   cp env.dist .env
   ```
   Edit `.env` and add your `DISCORD_BOT_TOKEN`.
4. **Start the bot**
   ```bash
   python bot.py
   ```

## Slash Commands
- `/set_text_channel` – set the text channel where the bot listens
- `/add_channel` – register a voice channel for squads
- `/remove_channel` – unregister a voice channel
- `/list_channels` – list all registered voice channels
- `/set_api_domain` – set the API domain for map data
- `/set_language` – choose the bot language (e.g. `en` or `de`)

## Text Command
- `!squadlead` – pick squad leaders and show the squads in the text channel

## Example Output
```
Squadleader and Squads

1 Squad(s) created for the channel 🎧│Seeding!

Current Map
Omaha Beach

Squad 1 (Leader: ⭐ Player1)
⭐ Player1
🪖 Player2
🪖 Player3
```

## Troubleshooting
- If the bot does not respond, make sure `/set_text_channel` was used and check the bot's permissions.
- If no map is displayed, verify the API domain set with `/set_api_domain` is reachable.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

This project is licensed under the MIT License.
