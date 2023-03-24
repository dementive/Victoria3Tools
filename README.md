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

## Features

#### All script (.txt) files have the following features:
- Autocomplete for all terms that are in triggers.log, effects.log, event_targets.log, and modifiers.log. All autocomplete items have a short description showing what input/output scope the term supports.
- Dynamically generated syntax that will automatically add any scripted effects, scripted triggers, or scripted values you make to the highlighting. To work properly your mods path needs to be added to the package settings.
- Snippets to generate common boiler plate text like country events, decisions, journals, and more.
- Documentation on hover for all terms in the log. Simply hovering over an effect/trigger/scope will show it's full documentation in a popup.
- Status Bar automatically updates to show when cursor is inside a Trigger or Effect block.
- Localize command that will automatically create localization entries from a script file. Accessed from the command palette, opened with `ctrl+shift+p` and then type in `Victoria 3`.
- Browse Video command that will allow you to play .bk2 videos directly from the command palette. Also shows a popup when hovering over a video file in an event that will let you play the video, replace the video with a new one, or replace and play the new video. Note that the [Rad Game Tools Bink Player](http://www.radgametools.com/bnkdown.htm) is required to play the games .bk2 files.
- Hovering over texture paths will show a popup to open it.
- Hovering over event sounds will show a popup that allows you to quickly browse and replace event sounds with the command palette.
- Goto Definition for all game objects, saved scopes, and saved variables
- Simple validator that will check for common easy to find errors and alert you when they happen when a script file is saved. These include: mismatched brackets, mismatched quotes, and encoding errors.
- Full syntax highlighting of all relevant terms you may come across in Vic3 modding.
	- Effects = red
	- Triggers = yellow
	- Scopes = blue
	- Math/Sound = orange
	- on_actions from code = green
	- Essential Scipt/Textures = purple

![Script Screenshot](/images/script.png)

#### All GUI (.gui) files have syntax highlighting with a similar style to script
- Effects = red
- Triggers = yellow
- Parameters = blue
- Textures = purple
- Gui Defaults = green
- Sound/Animations = orange
- Hovering over texture paths will show a popup to open it.
- Goto definition for types and templates.

![Gui Screenshot](/images/gui.png)

#### For shaders (.fxh and .shader) there are multiple IDE like features these include:
- Open header files with a popup that shows up when hovering over an included files name.
- Documentation for common HLSL functions and links to MSDN documentation on hover.
- Ifdef block matching on hover that makes it easy to navigate big blocks.
- 100+ snippets that will fill out commonly used HLSL functions.
- Syntax highlighting for paradox shader files which is similar to HLSL in a lot of ways but has a lot of key differences.

![Shader Screenshot](/images/shader.png)

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
Select ```Victoria Gui``` as the default syntax for .gui.

For both .shader and .fxh file types select ```PdxShader``` as the default syntax.
