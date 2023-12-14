<h1 align="center">
<br>
<a name="top" href="https://marketplace.visualstudio.com/items?itemName=mstuttgart.odoo-scaffold">
<img src="https://raw.githubusercontent.com/mstuttgart/vscode-odoo-scaffold/develop/images/icon.png">
</a>
<br>
Visual Code Odoo Scaffold
<br>
</h1>

<h4 align="center">A Visual Code extension to create Odoo modules easily</h4>

<p align="center">

<a name="top" href="https://marketplace.visualstudio.com/items?itemName=mstuttgart.odoo-scaffold">
<img src="https://vsmarketplacebadge.apphb.com/version-short/mstuttgart.odoo-scaffold.svg?style=flat-square" alt="Version">
</a>
<a href="https://marketplace.visualstudio.com/items?itemName=mstuttgart.odoo-scaffold">
<img src="https://vsmarketplacebadge.apphb.com/installs/mstuttgart.odoo-scaffold.svg?style=flat-square" alt="Installs">
</a>
<a href="https://marketplace.visualstudio.com/items?itemName=mstuttgart.odoo-scaffold">
<img src="https://vsmarketplacebadge.apphb.com/rating/mstuttgart.odoo-scaffold.svg?style=flat-square" alt="Rating">
</a>

</p>
<p align="center">
<b><a href="#features">Features</a></b>
|
<b><a href="#requirements">Requirements</a></b>
|
<b><a href="#installation">Installation</a></b>
|
<b><a href="#settings">Settings</a></b>
|
<b><a href="#release-notes">Release Notes</a></b>
|
<b><a href="#credits">Credits</a></b>
</p>

## Features

This extension allow create Odoo modules from explorer windown in easy way.

### From window explorer

Right click on Explorer Window and click in `New Odoo Module`.

![feature X](https://raw.githubusercontent.com/mstuttgart/vscode-odoo-scaffold/develop/images/screenshot.png)

Confirme the selected path (press `Enter`) and type the new module name and press `Enter`.

![feature X](https://raw.githubusercontent.com/mstuttgart/vscode-odoo-scaffold/develop/images/screenshot_1.png)

### From command panel

Press `ctrl+shift+p` to open command panel and type `Python: New Odoo Module`. 

Type the path of where new module will be create:

![feature X](https://raw.githubusercontent.com/mstuttgart/vscode-odoo-scaffold/develop/images/screenshot2.png)

Type the name of new module:

![feature X](https://raw.githubusercontent.com/mstuttgart/vscode-odoo-scaffold/develop/images/screenshot_1.png)

## Requirements

Work with Odoo 10.0+ and need of `Python Path` configured.

This extension use Odoo  [scaffold](https://www.odoo.com/documentation/11.0/reference/cmdline.html#scaffolding) command to generate Odoo modules. To use it, you need to set [odoo-bin](https://github.com/odoo/odoo/blob/11.0/odoo-bin) executable path in settings of vscode.

## Installation

Launch *Quick Open*
  - <img src="https://www.kernel.org/theme/images/logos/favicon.png" width=16 height=16/> <a href="https://code.visualstudio.com/shortcuts/keyboard-shortcuts-linux.pdf">Linux</a> `Ctrl+P`
  - <img src="https://developer.apple.com/favicon.ico" width=16 height=16/> <a href="https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf">macOS</a> `⌘P`
  - <img src="https://www.microsoft.com/favicon.ico" width=16 height=16/> <a href="https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf">Windows</a> `Ctrl+P`

Paste the following command and press `Enter`:

```
ext install mstuttgart.odoo-scaffold
```

## Settings

By default the extension uses the configuration from [Python extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

To configure Python for your project see [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial).

You need to set `odoo-bin` path of you `workspace settings` to made this extension works.

```json
{
  "odooScaffold.odooBinPath": "absolute/path/to/odoo-bin",
  "pythonVirtualEnv": "absolute/path/to/virtualenv/bin/python",
  "odooTemplatePath": "absolute/path/to/moduletemplate" // optional
}
```

## Release Notes

See [changelog](CHANGELOG.md).

## Credits

Copyright (C) 2018-2021 by Michell Stuttgart
