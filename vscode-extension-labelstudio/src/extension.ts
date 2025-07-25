import * as vscode from 'vscode';
import { exec } from 'child_process';

function runCommand(command: string, cwd: string) {
    const terminal = vscode.window.createTerminal('Label Studio');
    terminal.show();
    terminal.sendText(`cd "${cwd}" && ${command}`);
}

export function activate(context: vscode.ExtensionContext) {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    const labelstudioPath = workspaceFolders ? `${workspaceFolders[0].uri.fsPath}/docker/labelstudio` : '';

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
}

export function deactivate() {}
