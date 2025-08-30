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
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const net = require("net");
const vscode_1 = require("vscode");
const node_1 = require("vscode-languageclient/node");
const cp = require("child_process");
let client;
const DEBUG_CLIENT = false;
function getClientOptions() {
    return {
        // Register the server for plain text documents
        documentSelector: [
            { scheme: "file", language: "medford" },
            { scheme: "untitled", language: "medford" },
        ],
        outputChannelName: "[pygls] MEDFORDLanguageServer",
        synchronize: {
            // Notify the server about file changes to '.clientrc files contain in the workspace
            fileEvents: vscode_1.workspace.createFileSystemWatcher("**/.clientrc"),
        },
    };
}
function installDependencies(pythonPath) {
    try {
        // check if mfdls is installed already
        cp.execSync(`${pythonPath} -c "import pygls"`);
    }
    catch (e) {
        vscode_1.window.showWarningMessage(`Could not find pygls in ${pythonPath}, attempting to install now`);
        try {
            // if not, try to install it.
            cp.execSync(`${pythonPath} -m pip install pygls`);
        }
        catch (e) {
            vscode_1.window.showErrorMessage("Could not install pygls");
            throw new Error("could not install pygls");
        }
        vscode_1.window.showInformationMessage("Successfully installed pygls");
    }
}
function connectToLangServerTCP(addr) {
    const serverOptions = () => {
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
    return new node_1.LanguageClient(`tcp lang server (port ${addr})`, serverOptions, getClientOptions());
}
function startLangServer(command, args, cwd) {
    const serverOptions = {
        args,
        command,
        options: { cwd },
    };
    return new node_1.LanguageClient(command, serverOptions, getClientOptions());
}
function activate(context) {
    if (context.extensionMode === vscode_1.ExtensionMode.Development && !DEBUG_CLIENT) {
        // Development - Run the server manually
        client = connectToLangServerTCP(2087);
    }
    else {
        // Production - Client is going to run the server (for use within `.vsix` package)
        /*const cwd = path.join(__dirname, "..", "..", "medford-language-server");
        /*const pythonPath = workspace
            .getConfiguration("python")
            .get<string>("pythonPath");

        if (!pythonPath) {
            throw new Error("python.pythonPath` is not set");
        }
        
        // Check that the mfdls server exists. If it doesn't, try to install it
        installDependencies(pythonPath);

        */
        const cwd = ".";
        const pythonPath = "python3";
        client = startLangServer(pythonPath, ["-m", "mfdls"], cwd);
    }
    context.subscriptions.push(client.start());
}
exports.activate = activate;
function deactivate() {
    return client ? client.stop() : Promise.resolve();
}
exports.deactivate = deactivate;
``;
//# sourceMappingURL=extension.js.map