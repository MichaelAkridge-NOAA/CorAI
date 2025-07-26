
import * as vscode from 'vscode';

function runCommand(command: string, cwd: string) {
    const terminal = vscode.window.createTerminal({
        name: 'Label Studio',
        cwd: cwd
    });
    terminal.show();
    terminal.sendText(command);
}

class LabelStudioSidebarProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'labelstudio.sidebar';
    private _view?: vscode.WebviewView;
    private _labelstudioPath: string;

    constructor(private readonly _extensionUri: vscode.Uri, labelstudioPath: string) {
        this._labelstudioPath = labelstudioPath;
    }

    resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;
        webviewView.webview.options = {
            enableScripts: true,
        };
        webviewView.webview.html = this.getHtmlForWebview(webviewView.webview);

        webviewView.webview.onDidReceiveMessage((message) => {
            switch (message.command) {
                case 'start':
                    runCommand('docker compose up', this._labelstudioPath);
                    break;
                case 'stop':
                    runCommand('docker compose down', this._labelstudioPath);
                    break;
                case 'status':
                    runCommand('docker compose ps', this._labelstudioPath);
                    break;
                case 'logs':
                    runCommand('docker compose logs -f', this._labelstudioPath);
                    break;
            }
        });
    }

    getHtmlForWebview(webview: vscode.Webview): string {
        return `
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Label Studio Manager</title>
                <style>
                    body { font-family: sans-serif; padding: 10px; }
                    button { margin: 5px 0; width: 100%; padding: 8px; font-size: 1em; }
                </style>
            </head>
            <body>
                <h2>Label Studio Manager</h2>
                <button onclick="vscode.postMessage({ command: 'start' })">Start Label Studio</button>
                <button onclick="vscode.postMessage({ command: 'stop' })">Stop Label Studio</button>
                <button onclick="vscode.postMessage({ command: 'status' })">Show Status</button>
                <button onclick="vscode.postMessage({ command: 'logs' })">View Logs</button>
                <script>
                    const vscode = acquireVsCodeApi();
                </script>
            </body>
            </html>
        `;
    }
}

export function activate(context: vscode.ExtensionContext) {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    const labelstudioPath = workspaceFolders ? `${workspaceFolders[0].uri.fsPath}/docker/labelstudio` : '';

    // Register commands for command palette
    context.subscriptions.push(
        vscode.commands.registerCommand('labelstudio.start', () => {
            runCommand('docker compose up', labelstudioPath);
        })
    );
    context.subscriptions.push(
        vscode.commands.registerCommand('labelstudio.stop', () => {
            runCommand('docker compose down', labelstudioPath);
        })
    );
    context.subscriptions.push(
        vscode.commands.registerCommand('labelstudio.status', () => {
            runCommand('docker compose ps', labelstudioPath);
        })
    );
    context.subscriptions.push(
        vscode.commands.registerCommand('labelstudio.logs', () => {
            runCommand('docker compose logs -f', labelstudioPath);
        })
    );

    // Register sidebar provider
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            LabelStudioSidebarProvider.viewType,
            new LabelStudioSidebarProvider(context.extensionUri, labelstudioPath)
        )
    );
}

export function deactivate() {}
