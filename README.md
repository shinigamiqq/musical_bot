# Music Bot

This Discord bot allows users to play music from various sources such as YouTube, Twitch, etc., and interact with an AI chat model for natural language processing.

## Features

- Play Music: Play music tracks from YouTube, Twitch, etc., in a voice channel using the !play <url> command.
- Search Video: Search for videos on YouTube and play them in a voice channel using the !search <name> command.
- Pause and Resume: Pause and resume music playback in a voice channel using the !pause and !resume commands.
- Stop Playback: Stop music playback and disconnect the bot from the voice channel using the !stop command.
- AI Chat: Engage in conversation with an AI chat model using the !chat <message> command.
- Image Search: Search for images using the !image <query> command.

## Usage

1. Invite the bot to your Discord server.
2. Join a voice channel in the server.
3. Use the commands to play music, pause/resume playback, search for videos, chat with AI, and search for images.

## Requirements

- Python 3.7 or higher
- discord.py library
- youtube-dl library
- yt-dlp library
- OpenAI API key

## Setup

1. Clone this repository.
2. Install the required Python packages using pip install -r requirements.txt.
3. Obtain an OpenAI API key and set it in the openai.api_key variable in the code.
4. Same thing with discord API key
5. Run the bot using python senbonzakura_kageyoshi.py.

## Commands

- !play <url>: Play music from the specified URL.
- !search <name>: Search for videos on YouTube and play them.
- !pause: Pause music playback.
- !resume: Resume music playback.
- !stop: Stop music playback and disconnect from the voice channel.
- !chat <message>: Chat with an AI model.
- !image <query>: Search for images based on the query.
- !help: information about commands

## Credits

This bot is created by shinigamiqq.
