# How To Update to new Vic3 Version

1. Run parse_docs.py and follow it's instructions

2. Add the generated data to the bottom of the auto-generated-content section in VictoriaScript.fake-sublime-syntax

3. Go to PluginData.py and run the get_game_data function.

4. With the printed output, replace the proper lists in PluginData.py


# Bugs

• goto definition popups wrongly show the definition of something as a reference if it is defined in the same file as the current token

## Todo

• Fix shader syntax so it correctly shows `//` comments when on Code[[ ]] blocks and `#` commments when not in Code blocks

• Add a new hover popup for usages of @words preprocessor statements. When hovering over the usages it will show a simple popup that shows what the value of the statement is. Should work for gui and script.

• Add ⨉ character to top corner of texture phantom popups to close them

• Write parser for Data system functions in data types log.

• Special autocompletion triggers for event, decision, and journal files

• Custom parsers for different GameObjects that save more useful information that can be used in popups
