# Label Studio Manager VS Code Extension

This extension lets you setup, start, stop, and manage Label Studio via Docker Compose directly from VS Code.

## Features
- Start Label Studio (`docker compose up`)
- Stop Label Studio (`docker compose down`)
- Show status (`docker compose ps`)
- View logs (`docker compose logs -f`)



## Setup
1. Open a terminal in this folder (`vscode-extension-labelstudio`).
2. Run:
   ```sh
   npm install
   npm run compile
   ```
   This installs dependencies and builds the extension.

## Packaging and Installing
To package the extension as a VSIX file for easy installation:
```sh
npx vsce package
```
This will create a `.vsix` file you can install in VS Code via "Extensions: Install from VSIX" in the Command Palette.

## Important
- Make sure you open your CorAI workspace folder in VS Code (e.g., `/home/user/CorAI`).
- The extension looks for the `docker/labelstudio` folder inside your workspace. If you open the wrong folder, the commands may use an incorrect path (e.g., `/home/user/docker/labelstudio` instead of `/home/user/CorAI/docker/labelstudio`).

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
