/* extension.ts
 * 
 * By: Liam Strand
 * On: Summer 2022
 * 
 * Provides a shim connecting the language server to VS Code. Handles making
 * requests to the language server and reporting responses.
 * 
 * Also handles most dependency management.
 * 
 */

"use strict";

import * as net from "net";
import * as path from "path";
import { ExtensionContext, ExtensionMode, workspace, window} from "vscode";
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
} from "vscode-languageclient/node";
import * as cp from "child_process";

let client: LanguageClient;

const DEBUG_CLIENT = false;

function getClientOptions(): LanguageClientOptions {
    return {
        // Register the server for plain text documents
        documentSelector: [
            { scheme: "file", language: "medford" },
            { scheme: "untitled", language: "medford" },
        ],
        outputChannelName: "[pygls] MEDFORDLanguageServer",
        synchronize: {
            // Notify the server about file changes to '.clientrc files contain in the workspace
            fileEvents: workspace.createFileSystemWatcher("**/.clientrc"),
        },
    };
}

function installDependencies(pythonPath: string): void {
    try {
        // check if mfdls is installed already
        cp.execSync(`${pythonPath} -c "import pygls"`);
    } catch (e) {
        window.showWarningMessage(`Could not find pygls in ${pythonPath}, attempting to install now`);
        try {
            // if not, try to install it.
            cp.execSync(`${pythonPath} -m pip install pygls`);
        } catch (e) {
            window.showErrorMessage("Could not install pygls");
            throw new Error("could not install pygls")
        }
        window.showInformationMessage("Successfully installed pygls");
    }
}

function connectToLangServerTCP(addr: number): LanguageClient {
    const serverOptions: ServerOptions = () => {
        return new Promise((resolve /* , reject */) => {
            const clientSocket = new net.Socket();
            clientSocket.connect(addr, "127.0.0.1", () => {
                resolve({
                    reader: clientSocket,
                    writer: clientSocket,
                });
            });
        });
    };

    return new LanguageClient(
        `tcp lang server (port ${addr})`,
        serverOptions,
        getClientOptions()
    );
}

function startLangServer(
    command: string,
    args: string[],
    cwd: string
): LanguageClient {
    const serverOptions: ServerOptions = {
        args,
        command,
        options: { cwd },
    };

    return new LanguageClient(command, serverOptions, getClientOptions());
}

export function activate(context: ExtensionContext): void {
    if (context.extensionMode === ExtensionMode.Development && !DEBUG_CLIENT) {
        // Development - Run the server manually
        client = connectToLangServerTCP(2087);
    } else {
        // Production - Client is going to run the server (for use within `.vsix` package)
        const cwd = path.join(__dirname, "..", "..", "medford-language-server");
        const pythonPath = workspace
            .getConfiguration("python")
            .get<string>("pythonPath");

        if (!pythonPath) {
            throw new Error("python.pythonPath` is not set");
        }
        
        // Check that the mfdls server exists. If it doesn't, try to install it
        installDependencies(pythonPath);


        client = startLangServer(pythonPath, ["-m", "mfdls"], cwd);

    }

    context.subscriptions.push(client.start());

}

export function deactivate(): Thenable<void> {
    return client ? client.stop() : Promise.resolve();
}
``
