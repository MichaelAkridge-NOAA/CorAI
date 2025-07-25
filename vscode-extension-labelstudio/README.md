# Label Studio Manager VS Code Extension

This extension lets you setup, start, stop, and manage Label Studio via Docker Compose directly from VS Code.

## Features
- Start Label Studio (`docker compose up`)
- Stop Label Studio (`docker compose down`)
- Show status (`docker compose ps`)
- View logs (`docker compose logs -f`)

## Usage
1. Open your CorAI workspace in VS Code.
2. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`).
3. Type `Label Studio:` and select an action (Start, Stop, Status, Logs).

## Requirements
- Docker must be installed and running.
- Your workspace must contain the `docker/labelstudio` folder.

## Development
- Run `npm install` to install dependencies.
- Run `npm run compile` to build the extension.
- Press `F5` to launch a new Extension Development Host.
