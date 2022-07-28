# medford-vscode

An implementation of the Language Server Protocol to provide editor support for the MEDFORD metadata markup language. The server will be started automatically when a MEDFORD document (ending in `.mfd`) is opened.

## Features:

- Syntactic validation
- Semantic validation
- Autocomplete for major tokens and expected minor tokens
- Autocomplete for preveiously defined macros
- Syntax highlighting

## Requirements:

Python (3.8 or newer) must be installed on your system and VS Code must have access to the Python interpreter.

Python dependencies should be automatically installed. If there are issues,
try installing [pygls](https://github.com/openlawlibrary/pygls) manually on the configured python environment using `pip install pygls`.

The [language server](https://github.com/liam-strand/medford-language-server) and [medford parser](https://github.com/TuftsBCB/medford) are bundled with this extension and do not need to be installed seperately.

## Extension Settings:

There are no user-configurable settings at this time. If you'd like one added, please let us know.

## Issues:

This software is in ***beta***! If you run into an issue with the user-interface, please open an issue in the [extension repository](https://github.com/liam-strand/medford-vscode). If you run into an issue with error messages or autocomplete, please open an issue in the [language server repository](https://github.com/liam-strand/medford-language-server). Also, feel free to email us if you have any questions or concerns!

## Contributors:
- [Liam Strand](https://github.com/liam-strand)
- [Andrew Powers](https://github.com/andrew-powers)

<!-- 
## Python Dependencies:
* [pygls](https://pypi.org/project/pygls/)
* [medford](https://pypi.org/project/medford/)

## TypeScript Dependencies:
* `npm` should take care of this for you
* but you have to [have `npm` installed](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

## To Run:
* Install the dependencies
* `git clone` this repository, you must use the `--recurse-submodules` flag
* Open the root directory in VS Code
* `npm install && cd client && npm install && cd ..` to install TypeScript dependencies
* Go to "Run and Debug" view and select "Launch Client"
* There is a sample MEDFORD file at `testfiles/example.mfd`, open it up to try it out!

## Features

Describe specific features of your extension including screenshots of your extension in action. Image paths are relative to this README file.

For example if there is an image subfolder under your extension project workspace:

\!\[feature X\]\(images/feature-x.png\)

> Tip: Many popular extensions utilize animations. This is an excellent way to show off your extension! We recommend short, focused animations that are easy to follow.

## Requirements

If you have any requirements or dependencies, add a section describing those and how to install and configure them.

## Extension Settings

Include if your extension adds any VS Code settings through the `contributes.configuration` extension point.

For example:

This extension contributes the following settings:

* `myExtension.enable`: enable/disable this extension
* `myExtension.thing`: set to `blah` to do something

## Known Issues

Calling out known issues can help limit users opening duplicate issues against your extension.

## Release Notes

Users appreciate release notes as you update your extension.

### 1.0.0

Initial release of ...

### 1.0.1

Fixed issue #.

### 1.1.0

Added features X, Y, and Z.

-----------------------------------------------------------------------------------------------------------

## Working with Markdown

**Note:** You can author your README using Visual Studio Code.  Here are some useful editor keyboard shortcuts:

* Split the editor (`Cmd+\` on macOS or `Ctrl+\` on Windows and Linux)
* Toggle preview (`Shift+CMD+V` on macOS or `Shift+Ctrl+V` on Windows and Linux)
* Press `Ctrl+Space` (Windows, Linux) or `Cmd+Space` (macOS) to see a list of Markdown snippets

### For more information

* [Visual Studio Code's Markdown Support](http://code.visualstudio.com/docs/languages/markdown)
* [Markdown Syntax Reference](https://help.github.com/articles/markdown-basics/)

**Enjoy!**
 -->
