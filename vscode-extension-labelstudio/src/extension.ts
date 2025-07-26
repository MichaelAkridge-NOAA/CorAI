import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';

class LabelStudioItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    public readonly command?: vscode.Command
  ) {
    super(label);
    this.tooltip = label;
    this.description = '';
  }
}

class LabelStudioProvider implements vscode.TreeDataProvider<LabelStudioItem> {
  private _onDidChangeTreeData: vscode.EventEmitter<LabelStudioItem | undefined | void> = new vscode.EventEmitter<LabelStudioItem | undefined | void>();
  readonly onDidChangeTreeData: vscode.Event<LabelStudioItem | undefined | void> = this._onDidChangeTreeData.event;

  getTreeItem(element: LabelStudioItem): vscode.TreeItem {
    return element;
  }

  getChildren(): Thenable<LabelStudioItem[]> {
    return Promise.resolve([
      new LabelStudioItem("Start Label Studio", {
        command: 'labelstudio.start',
        title: 'Start Label Studio'
      }),
      new LabelStudioItem("Stop Label Studio", {
        command: 'labelstudio.stop',
        title: 'Stop Label Studio'
      }),
      new LabelStudioItem("Check Status", {
        command: 'labelstudio.status',
        title: 'Check Status'
      }),
      new LabelStudioItem("View Logs", {
        command: 'labelstudio.logs',
        title: 'View Logs'
      }),
    ]);
  }
}

function runDockerCommand(command: string, label: string, cwd: string) {
  vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: label,
      cancellable: false
    },
    async () =>
      new Promise<void>((resolve) => {
        exec(command, { cwd }, (error: Error | null, stdout: string, stderr: string) => {
          if (error) {
            vscode.window.showErrorMessage(`${label} failed: ${stderr || error.message}`);
          } else {
            vscode.window.showInformationMessage(`${label} succeeded:\n${stdout}`);
          }
          resolve();
        });
      })
  );
}

export function activate(context: vscode.ExtensionContext) {
  const provider = new LabelStudioProvider();
  vscode.window.registerTreeDataProvider('labelstudio.sidebar', provider);

  const workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '';

  context.subscriptions.push(
    vscode.commands.registerCommand('labelstudio.start', () => {
      runDockerCommand('docker compose up -d', 'Starting Label Studio', workspacePath);
    }),

    vscode.commands.registerCommand('labelstudio.stop', () => {
      runDockerCommand('docker compose down', 'Stopping Label Studio', workspacePath);
    }),

    vscode.commands.registerCommand('labelstudio.status', () => {
      runDockerCommand('docker compose ps', 'Label Studio Status', workspacePath);
    }),

    vscode.commands.registerCommand('labelstudio.logs', () => {
      runDockerCommand('docker compose logs --tail=20', 'Label Studio Logs', workspacePath);
    })
  );
}

export function deactivate() {}