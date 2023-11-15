import os
import re

"""
	Creates lists from paradox game logs

	How to use:
	1. Take trigger, on_action, modifier, effect, and event_targets logs from documents folder and put them all in the "docs" folder
	2. Remove the first set of first header from each of the logs
	3. Remove all the stray words from the bottom of the event_targets
	4. Make sure all the logs look like this (make sure there is a "- " before the description starts for triggers, effects, and scopes) 
		```
		### attacker_side
		- Scope from a battle to the BattleSide corresponding to the attacker
		Input Scopes: battle
		Output Scopes: battle_side
		### defender_side
		- Scope from a battle to the BattleSide corresponding to the defender
		Input Scopes: battle
		Output Scopes: battle_side
		### diplomatic_pact_other_country
		- Scope to the other country of the diplomatic pact in scope
		Requires Data: yes
		Input Scopes: diplomatic_pact
		Output Scopes: country
		```
	5. Run the script
"""


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def parse_logs(file, mode):
    file = open(file, "r")
    contents = file.read()
    file.close()
    # The first identifier must be removed from the input file for it to read properly.
    if mode == "on_action":
        split = contents.split("--------------------")
    elif file == "docs/event_targets.log":
        split = contents.split("###")
    elif mode == "normal" or "descriptions":
        split = contents.split("##")
    elif mode == "mods":
        split = contents.replace(",", "").replace("\n", "").split("Tag: ")

    parsed_list = []

    for i in range(len(split)):
        node = split[i].strip()
        if not node:
            continue
        if mode == "normal":
            stripped = node.split("-", 1)[0].replace("\n", "").replace(" ", "")
            parsed_list.append(stripped)
        elif mode == "mods":
            parsed_list.append(node)
        elif mode == "on_action":
            from_code = "From Code: Yes" in node
            if from_code:
                stripped = node.split(":", 1)[0].replace("\n", "").replace(" ", "")
                parsed_list.append(stripped)
        elif mode == "descriptions":
            desc_pos = node.find("Supported S")
            if desc_pos != -1:
                node_end = node.find("\n\n")
                description = node[desc_pos : len(node)]
                description = description.replace("\n", "")
                split_pos = description.find("Supported Targets")
                if split_pos != -1:
                    description = (
                        description[:split_pos] + " -> " + description[split_pos:]
                    )
                    parsed_list.append(description)
                else:
                    parsed_list.append(description)
        elif mode == "scope_descriptions":
            description = find_between(node, "- ", "\n")
            parsed_list.append(description)
        elif mode == "full_descs":
            full_descs = node.split("- ", 1)
            # Make minihtml compatible
            full_descs[1] = (
                full_descs[1]
                .replace("\n", "<br>")
                .replace(
                    "Traits: <, <=, =, !=, >, >=",
                    "Traits: &lt;, &le;, =, !=, &gt;, &ge;",
                )
                .replace("<triggers>", "triggers")
                .replace("<effects>", "effects")
            )
            # remove trailing br tags
            if full_descs[1].endswith("<br><br>"):
                full_descs[1] = full_descs[1].replace("<br><br>", "")
            if full_descs[1].endswith("<br>"):
                full_descs[1] = full_descs[1].rstrip()[:-4]

            # fix quotes so they can go into python
            full_descs[1] = full_descs[1].replace('"', '\\"')

            parsed_list.append(full_descs[1])

    return parsed_list


def create_sublime_completions(
    game, syntax_scope, effects, triggers, scopes, modifiers
):
    file = open(f"output/{game}Completions.sublime-completions", "w")
    file.write(f'{{\n\t"scope": "{syntax_scope}",\n\t"completions":\n\t[')

    effects_desc = parse_logs("docs/effects.log", "descriptions")
    triggers_desc = parse_logs("docs/triggers.log", "descriptions")
    scopes_desc = parse_logs("docs/event_targets.log", "scope_descriptions")

    # These use the normal Trigger and Effect lists
    # for i, ed in zip(effects, effects_desc):
    # 	file.write(f"""
    # 	{{
    # 		\"trigger\": \"{i}\",
    # 		\"contents\": \"{i}\",
    # 		\"details\": \"{ed}\",
    # 		\"kind\": [\"function\", \"E\", \"Effect\"]
    # 	}},""")

    # for i, td in zip(triggers, triggers_desc):
    # 	file.write(f"""
    # 	{{
    # 		\"trigger\": \"{i}\",
    # 		\"contents\": \"{i}\",
    # 		\"details\": \"{td}\",
    # 		\"kind\": [\"navigation\", \"T\", \"Trigger\"]
    # 	}},""")

    for i, sd in zip(scopes, scopes_desc):
        file.write(
            f"""
		{{
			\"trigger\": \"{i}\",
			\"contents\": \"{i}\",
			\"details\": \"{sd}\",
			\"kind\": [\"namespace\", \"S\", \"Scope\"]
		}},"""
        )

    # file.write("ModifersList = {")
    # for i in modifiers:
    #     regex = re.search(r"[^C]*$", i)
    #     cat_out = regex[0].replace("ategories", "Category")
    #     mod_out = i.split("C", 1)[0].replace(" ", "")
    #     file.write(f"\"{mod_out}\": \"{cat_out}\",\n")

    file.write("}")
    file.write("\n\t]\n}")
    file.close()
    full_path = os.path.realpath(f"{game}Completions.sublime-completions")
    file_path = os.path.dirname(full_path) + "\\output"


def write_syntax(iterator, header, scheme_scope, file):
    if header == "Scopes":
        # Scopes can be case insensitive, everything else is not for performance.
        file.write(f"    # {header}\n    - match: \\b(?i)(")
        for i in iterator:
            file.write(f"{i}|")
        file.write(f")(?-i)\\b\n      scope: {scheme_scope}\n")
    else:
        file.write(f"    # {header}\n    - match: \\b(")
        for i in iterator:
            file.write(f"{i}|")
        file.write(f")\\b\n      scope: {scheme_scope}\n")


def split_write_syntax(iterator, header, scheme_scope, file):
    file.write(f"    # {header}\n    - match: \\b(")
    half = int(len(iterator)) / 2
    count = 0  # count for modifiers split
    for index, content in enumerate(iterator):
        if header != "Modifiers":
            if index < int(half):
                file.write(f"{content}|")
            elif index == int(half):
                file.write(f")\\b\n      scope: {scheme_scope}\n")
                file.write(f"    # {header} part 2\n    - match: \\b({content}|")
            else:
                file.write(f"{content}|")
        else:
            count += 1
            if count == 0:
                file.write(f")\\b\n      scope: {scheme_scope}\n")
                file.write(f"    # {header}\n    - match: \\b({content}|")
            elif count == 75:
                file.write(f")\\b\n      scope: {scheme_scope}\n")
                file.write(f"    # {header}\n    - match: \\b({content}|")
                count = 1
            else:
                file.write(f"{content}|")

    file.write(f")\\b\n      scope: {scheme_scope}\n")


def write_extra(file):
    file.write(
        "\n    # --------------------------------\n    # -     Manually Added Terms     -\n    # --------------------------------\n\n"
    )
    file.write(
        f"    # Essential Scipt Functions\n    - match: \\b(texture|icon)\\b\n      scope: constant.numeric\n"
    )
    file.write(
        f"    # Math/Sound\n    - match: \\b(add)\\b\n      scope: variable.language\n"
    )
    file.write(
        f"    # Gui Defaults\n    - match: \\b(textbox)\\b\n      scope: keyword.onaction\n"
    )


def create_sublime_syntax(
    game, syntax_scope, effects, triggers, scopes, modifiers, on_actions
):
    file = open(f"output/{game}Syntax.sublime-syntax", "w")
    file.write(
        f"%YAML 1.2\n---\nname: {game} Scripting\nfile_extensions: [txt]\nscope: {syntax_scope}\n\ncontexts:\n  main:\n    # Comments\n    - match: (#).*$\\n?\n      scope: comment\n"
    )

    write_syntax(scopes, "Scopes", "storage.type.scope", file)
    write_syntax(on_actions, "On Actions From Code", "keyword.onaction", file)
    split_write_syntax(effects, "Effects", "keyword.effect", file)
    split_write_syntax(triggers, "Triggers", "string.trigger", file)
    mod_list_out = []
    for i in modifiers:
        regex = re.search(r"[^C]*$", i)
        mod_out = i.split("C", 1)[0].replace(" ", "")
        mod_list_out.append(mod_out)

    try:
        mod_list_out.remove("")
    except ValueError:
        pass
    split_write_syntax(mod_list_out, "Modifiers", "string.modifier", file)
    write_extra(file)


def write_full_descriptions(list1, fd):
    descs = parse_logs(f"docs/{fd}.log", "full_descs")
    file = open(f"output_lists/{fd}_dict.txt", "w")

    file.write(f"{fd.capitalize()}List = {{\n")
    count = 0
    for i in descs:
        file.write(f'\t"{list1[count]}": "{i}",\n')
        count += 1
    file.write("}")
    file.close()


def write_log(**kwargs):
    file = open("output_lists/logs.txt", "a")
    for key, value in kwargs.items():
        file.write(key.upper() + ":")
        for i in value:
            file.write(i + "|")
        file.write("\n")
    file.close()


def write_mods_to_log(modifiers):
    file = open("output_lists/logs.txt", "w")
    file.write("MODIFIERS:")
    count = 0
    for i in modifiers:
        regex = re.search(r"[^C]*$", i)
        mod_out = i.split("C", 1)[0].replace(" ", "")
        file.write(mod_out + "|")
        count += 1
        if count == 450:
            file.write("\n")
        if count == 900:
            file.write("\n")
    file.close()


if __name__ == "__main__":
    syntax_scope = "text.vic"
    game = "Victoria"

    effects = parse_logs("docs/effects.log", "normal")
    triggers = parse_logs("docs/triggers.log", "normal")
    scopes = parse_logs("docs/event_targets.log", "normal")
    # modifiers = parse_logs("docs/modifiers.log", "mods")
    on_actions = parse_logs("docs/on_actions.log", "on_action")
    modifiers = []

    # Extract full descriptions for hover docs (with br tags instead of newlines)

    write_full_descriptions(effects, "effects")
    write_full_descriptions(triggers, "triggers")
    write_full_descriptions(scopes, "event_targets")

    # Write to log for debugging syntax
    # write_mods_to_log(modifiers)
    write_log(effects=effects, triggers=triggers, scopes=scopes, on_actions=on_actions)

    # Create syntax
    create_sublime_completions(game, syntax_scope, effects, triggers, scopes, modifiers)
    create_sublime_syntax(
        game, syntax_scope, effects, triggers, scopes, modifiers, on_actions
    )
