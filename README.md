# Victoria 3 Syntax for Sublime Text 4

## How to Install

Run the following script in the Sublime Text terminal ```(ctrl+` )``` which utilizes git clone for easy installation:
```
import os; path=sublime.packages_path(); (os.makedirs(path) if not os.path.exists(path) else None); window.run_command('exec', {'cmd': ['git', 'clone', 'https://github.com/dementive/Victoria3Tools', 'Victoria3Tools'], 'working_dir': path})
```
This will only work with git installed on your system.

Alternatively you can download the zip file from github and put the Victoria3Tools folder in the packages folder. This is not recommended because you will not receive updates unless you redownload it manually.
The packages folder can easily be found by going to ```preferences``` in the main menu and selecting ```Browse Packages```.
```
C:\Users\YOURUSERNAME\AppData\Roaming\Sublime Text 3\Packages\Victoria3Tools
```

Make sure the folder is named `Victoria3Tools` or there will be issues with the plugin.

## Features

#### All script (.txt) files have the following features:
- Context aware autocomplete for all scopes, effects, and triggers.
- Dynamically generated syntax that will automatically add any scripted effects, scripted triggers, or scripted values you make to the highlighting. To work properly your mods path needs to be added to the package settings.
- Snippets to generate common boiler plate text like country events, decisions, journals, and more.
- Documentation on hover for all terms in the log. Simply hovering over an effect/trigger/scope will show it's full documentation in a popup.
- Localize command that will automatically create localization entries from a script file. Accessed from the command palette, opened with `ctrl+shift+p` and then type in `Victoria 3`.
- Hovering over texture paths will show a popup to open it.
- Textures can be show in sublime either in a new tab or directly in script files. To show textures either hover over the path and show inline or use `ctrl+alt+t` to show all the textures in the current file.
- Goto Definition for all game objects, saved scopes, and saved variables
- Simple validator that will check for common easy to find errors and alert you when they happen when a script file is saved. These include: mismatched brackets, mismatched quotes, and encoding errors.
- Full syntax highlighting of all relevant terms you may come across in Vic3 modding.

![Script Screenshot](/images/script.png)
![Script Screenshot2](/images/textures.png)

#### Gui 
- Syntax highlighting for .gui files with a similar style to script
- Hovering over texture paths will show a popup to open it. Textures can be show in sublime.
- Goto definition for types and templates.

![Gui Screenshot](/images/gui.png)

#### For shaders (.fxh and .shader) there are multiple features that include:
- Open header files with a popup that shows up when hovering over an included files name.
- Documentation for common HLSL functions and links to MSDN documentation on hover.
- Ifdef block matching on hover that makes it easy to navigate big blocks.
- 100+ snippets that will fill out commonly used HLSL functions.
- Syntax highlighting for paradox shader files which is similar to HLSL in a lot of ways but has a lot of key differences.

![Shader Screenshot](/images/shader.png)

# vic3-tiger integration

[vic3-tiger](https://github.com/amtep/ck3-tiger) has been fully integrated into the plugin and provides validation for all of your mod files. The vic3-tiger binary comes with the plugin and it's usage within sublime can be configured with the plugin settings. The following settings can be adjusted to change the behavior of vic3-tiger:
- Vic3TigerModPath - The path to the mod you are currently working on that you want to be validated. If you do not put a valid path in this setting the plugin will not use vic3-tiger at all and validation will be ignored.
- Vic3TigerUseDefaultConfig - By default the plugin will call tiger with the default vic3-tiger.conf file which is located in your mod folder. If you set this setting to 'false' the plugin will instead use a common .conf file between all mods that can be edited with the `Victoria 3: Edit vic3-tiger.conf` command. For more information about the vic3-tiger.conf read [guide](https://github.com/amtep/ck3-tiger/blob/main/filter.md)
- Vic3TigerShowErrorsInline - When you open a new file that tiger has detected errors in a squiggly line will be drawn under all the errors in the file, you can hover over these to get more information about the error. If you want to disable this feature just set this setting to false.

When you have a valid path defined in the vic3TigerModPath setting the plugin will automatically call vic3-tiger when you open sublime if changes have been detected in any of the mods you are currently working on. The following commands can be used to directly interact with vic3-tiger:
- `Victoria 3: Reload plugin objects and regenerate syntax` - The vic3-tiger output will be regenerated automatically by the plugin at the same time the syntax definition is. This means changes will only occur when sublime is first opened or when this reload objects command is run. If you have made some changes and you want vic3-tiger to validate them you can run this command to check if you made any mistakes.
- `Victoria 3: Show Tiger Output` - You can view the results of the tiger validation directly in sublime in either a panel at the bottom of the screen or in a new tab. This will display the validator output in the same style as tiger which replicated the style of Rust compiler errors. For each error an annotation will be draw that you can click on to open the source of the error in a new tab.

## Settings

There are also multiple settings that can be accessed via the package settings menu to disable some features or change the style of popups. Settings can be accessed from `main menu -> Preferences -> Package Setting -> Victoria 3 Settings -> Settings`

When setting up the package make sure the file paths to your Victoria 3 game folder and your mod folders are in settings. This allows the plugin to find game data.

## How to Enable Syntax

The syntaxes can be activated by going to:
```
main menu -> view -> syntax -> Open All with current extention as... -> Victoria3Tools
```
With a Victoria 3 .txt file open in sublime 
Select ```Victoria Script``` as the default syntax for .txt.

With a Victoria 3 .gui file open
Select ```Jomini Gui``` as the default syntax for .gui.

For both .yml file types select ```Victoria Localization``` as the default syntax.

For both .log file types select ```Victoria Logs``` as the default syntax.

For both .asset file types select ```Victoria Asset``` as the default syntax.

For both .shader and .fxh file types select ```PdxShader``` as the default syntax.


## Contributing to Victoria3Tools

All contributions are appreciated, whether they're bug fixes, feature additions, or improvements to documentation. Here's how you can contribute:

#### Getting Started

- Check Existing Issues: Before starting, please check our existing issues to see if someone has already reported the problem or suggested the feature you're interested in. If not, feel free to open a new issue.

- Create a Fork: Fork the project on GitHub to start making your changes.

- Open a Pull Request: Open a pull request against the main branch of the original repository. Include a detailed description of your changes and why they should be merged.

#### Code Guidelines

Victoria3Tools is written in python 3.8 and runs in the [Sublime Text 4 API environment](https://www.sublimetext.com/docs/api_environments.html), which means external dependencies cannot be used and some standard library modules are missing.

I am currently using [ruff](https://github.com/astral-sh/ruff) for linting and formatting that I have setup to run on [pre-commit](https://pre-commit.com/) hooks as well as [pyright](https://github.com/microsoft/pyright) for type checking.


To setup the pre-commit hooks you'll first need to [install pre-commit](https://pre-commit.com/#install) then run `pre-commit install`. You can use `pre-commit run --all-files` to make sure ruff is being run.

For more information on contributing see [Contributing.md](https://github.com/dementive/Victoria3Tools/blob/main/Contributing.md)


## License

Victoria3Tools uses the MIT license.
