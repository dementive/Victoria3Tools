# Plugin Architecture

Victoria3Tools is a sublime text 4 plugin, it uses some of the newer [API features](https://www.sublimetext.com/docs/api_reference.html) so you'll need the latest stable release of sublime.

Almost all plugin features revolve around manipulation of GameObjects which are objects defined by mods or the game that are used in other scopes, effects, or triggers. For example a CharacterTrait game object defined in `common/traits` could be defined in vic3 script like this:
```
my_trait = {
	param1 = yes
	param2 = no
}
```
The plugin parses all game objects defined both in the game and a user's mods using [jomini.py](https://github.com/dementive/Victoria3Tools/blob/main/src/jomini.py), which isn't actually a real parser and is solely based on vibes but somehow works pretty well. For each GameObject the plugin needs to know the name, file it is found in, and line number it is defined on in order to provide autocomplete, goto definition, dynamically generated syntax definitions, and other features. The actual implementation of vic3's game objects is done in [v3_objects.py](https://github.com/dementive/Victoria3Tools/blob/main/src/v3_objects.py).

# Entry point

The whole plugin is imported by `imperator_plugin.py` as a module where all of the sublime text interfacing API classes need to be imported into [\_\_init\_\_.py](https://github.com/dementive/Victoria3Tools/blob/main/src/__init__.py)

# Event Listener
Most plugin features are initiated by the [event listener](https://www.sublimetext.com/docs/api_reference.html#sublime_plugin.EventListener) found in [event_listener.py](https://github.com/dementive/Victoria3Tools/blob/main/src/event_listener.py)

# Autocomplete

The "entry point" for autocomplete features is the `on_query_completions` function found in the main event listener. The autocompletion entries we show the user is very dependent on the context around the user's editing position, depending on what game subdirectory they are in, and what kind of block (effect, trigger, mtth, etc...) different completions will need to be shown. For example in `common/modifiers` only modifiers are valid to use so we only show modifier completions. [scope_match.py](https://github.com/dementive/Victoria3Tools/blob/main/src/scope_match.py) is used to let the main event listener known what kind of block the cursor is inside of so autocomplete is able to provide accurate completions depending on where the cursor is. There is lots of static data associated with autocomplete found at the bottom of game_data.py that will need to be updated when making changes to autocomplete as well.

Some completions are more complex to setup and because the parser for game objects is very simple by design they are done in a somewhat hacky way via syntax scopes, these complex completions are added by updating the `check_complex_completions` function in autocomplete.py as well as the syntax scopes in the script syntax file. There are 2 different kinds of "complex completions":

Blocks with a list of game objects seperated by a space:
```
taboos = {
	liquor wine
}
```
Blocks with a parameter that equals a game object:
```
add_modifier = {
	name = <modifier name>
	months = normal_modifier_time
}
```


# Hover

There are a ton of plugin features that trigger from the `on_hover` of the main event listener. These include video, texture, goto definition, and documentation for script, gui, and shaders. As far as maintenence goes hover is pretty easy as almost all of the data is generated automatically or dynamically. Some of the hover code is really jank but shouldn't need much adjustment as it works very well. Updating the `hover_objects` list in the main event listener will be necessary when adding new game objects though but that should be mostly it.

# Adding a new GameObject

1. Make a new GameObject class in v3_objects.py

2. Load the game object into the plugin by updating the create_game_objects function in [event_listener.py](https://github.com/dementive/Victoria3Tools/blob/main/src/event_listener.py)

3. In [game_object_manager.py](https://github.com/dementive/Victoria3Tools/blob/main/src/game_object_manager.py) create a new attribute in the GameObjectManager

4. Update the write_data_to_syntax function in [game_objects.py](https://github.com/dementive/Victoria3Tools/blob/main/src/game_objects.py)

5. Update the hover_objects list in [event_listener.py](https://github.com/dementive/Victoria3Tools/blob/main/src/event_listener.py)

6. If the game object needs autocomplete:
	1. Add it to the auto_complete_fields dict in [autocomplete.py](https://github.com/dementive/Victoria3Tools/blob/main/src/autocomplete.py). 
	2. Update the completion_flag_pairs and simple_completion_pattern_flag_pairs lists in [game_data.py](https://github.com/dementive/Victoria3Tools/blob/main/src/game_data.py)

7. If the game object is a scope update the simple_completion_scope_pattern_flag_pairs list in [game_data.py](https://github.com/dementive/Victoria3Tools/blob/main/src/game_data.py)

8. Uncomment the print_load_balanced_game_object_creation function in [event_listener.py](https://github.com/dementive/Victoria3Tools/blob/main/src/event_listener.py) and copy the output into the create_game_objects function. This automatically balances the load when loading all the game objects so the threading is as efficient as possible (you only need to do this step if several new objects were added).

Occasionally GameObject's get removed from the game so just do the opposite of this to completely remove one.

# Updating to a new Victoria 3 Version

With each Victoria 3 update several things will have to be updated to keep the plugin up to date with the latest game version. I have a procedure I go through for updates (that could probably be better) that includes:

1. Follow the instructions in [parse_docs.py](https://github.com/dementive/Victoria3Tools/blob/main/Utilities/CreateSublimeSyntaxFromDocs/parse_docs.py) and run it to automatically generate new syntax, autocomplete, and hover descriptions from the game's logs that are obtained by running the `script_docs` console command in game. This will output 3 different things that needed to be added to the plugin:
	
	1. A huge ugly block of text that needs to be replace the existing generate content at the bottom of the `auto-generated-content` block of the [vic 3 script syntax](https://github.com/dementive/Victoria3Tools/blob/main/Vic3%20Script/VictoriaScript.fake-sublime-syntax).
	2. A [sublime completions](https://github.com/dementive/Victoria3Tools/blob/main/VictoriaCompletions.sublime-completions) file that can be used to just override the existing one in the root of the repo. This has all scopes in it as scopes are valid to use in pretty much every scripting context (trigger, effect, mtth, etc...) so they can all have static completion entries.
	3. 4 different giant ugly dictionaries that hold the static descriptions for every modifier, effect, trigger, and scope in the [minihtml](https://www.sublimetext.com/docs/minihtml.html) format so they can be displayed directly in sublime popups. In [game_data.py](https://github.com/dementive/Victoria3Tools/blob/main/src/game_data.py) there is a gigantic disgusting class named GameData. In that class the ModifiersList, EffectsList, TriggersList, and ScopesList will all need to be updated with the new data generated by parse_docs.py.

2. Believe it or not that is the easy part of updating to a new version. Some of the more involved plugin features require combing through vic3 files to ensure everything is up to date which can be quite tedious. You'll need to go through all the directories in Vic3 and check to see if any new GameObjects have been added or removed and apply these changes to the plugin. There are also thousands of keywords in various files all over Vic3 as well currently I have to manually go through to find all these and assign them to the proper syntax scope, this sucks and there is definitely a better way to automate it...I'll likely look into making this process faster in the future so the plugin maintenance isn't so time consuming.


# Bugs

• goto definition popups wrongly show the definition of something as a reference if it is defined in the same file as the current token

## Todo

• Fix shader syntax so it correctly shows `//` comments when on Code[[ ]] blocks and `#` commments when not in Code blocks

• Add a new hover popup for usages of @words preprocessor statements. When hovering over the usages it will show a simple popup that shows what the value of the statement is. Should work for gui and script.

• Add ⨉ character to top corner of texture phantom popups to close them

• Special autocompletion triggers for event, decision, and journal files

• Custom parsers for different GameObjects that save more useful information that can be used in popups
