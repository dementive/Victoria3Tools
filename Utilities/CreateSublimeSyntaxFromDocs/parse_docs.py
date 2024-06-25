import re
from typing import Dict

def parse_markdown_logs(log_content, header_length="##"):
    # Requirements: 
    # 1. Make sure there are 2 \n characters before the first log entry
    # 2. Remove all the extra stuff like headers and footers
    parsed_string = re.sub(r"\*\*(.*?)\*\*", "<b>\\1</b>", log_content.replace(f"\n\n{header_length} ", "ฌ").replace("\n", "<br>").replace("Traits: <, <=, =, !=, >, >=","Traits: &lt;, &le;, =, !=, &gt;, &ge;").replace("<triggers>", "triggers").replace("<effects>", "effects"))
    parsed_string = parsed_string.split("ฌ")

    parsed_dict = dict()
    for i in [x for x in parsed_string if x]:
        split_by = i.index("<br>")
        key = i[:split_by]
        value = i[split_by:]
        value = value[4:] # split off <br>
        parsed_dict[key] = value
    return parsed_dict

def get_markdown_log_data(filename) -> Dict[str, str]:
    parsed_logs = dict()

    with open(filename, "r") as file:
        content = "".join(file.readlines())

    if "event_targets" in filename:
        parsed_logs = parse_markdown_logs(content, "###")
    else:
        parsed_logs = parse_markdown_logs(content)

    return parsed_logs

def get_on_actions(log_file="docs/on_actions.log"):
    with open(log_file, "r") as file:
        content = "".join(file.readlines())
        content = content.split("--------------------\n\n")

    on_actions = set()
    for i in [x for x in content if "From Code: Yes" in x]:
        on_actions.add(i[:i.index(":")])

    return on_actions

class ModifData:
    def __init__(self, key, mask, name="", description=""):
        self.key = key
        self.mask = mask
        self.name = name
        self.description = description

def get_modifiers(input_string):
    # Input string must have a space at the bottom
    input_string = input_string.replace(":\n  ", "ฌ")
    input_string = re.sub(r"(\w+)(ฌ)", r"\2\n\1\n  ", input_string).replace("  ", "")
    input_string = input_string.split("ฌ\n")
    parsed_data = list()
    for i in [x for x in input_string if x != "\n"]:
        i = i[:-1].replace("Mask: ", "").replace("Name: ", "").replace("Description: ", "")
        i = re.sub(r"\w+!", "", i).replace("  ", " ")
        i = i.split("\n")
        if len(i) == 4:
            parsed_data.append(ModifData(i[0], i[1], i[2], i[3]))
        elif len(i) == 3:
            parsed_data.append(ModifData(i[0], i[1], i[2]))
        elif len(i) == 2:
            parsed_data.append(ModifData(i[0], i[1]))

    out_dict = dict()
    for i in parsed_data:
        if i.description:
            out_dict[i.key] = i.description

    return out_dict

def write_full_descriptions(desc_dict: dict, fd: str):
    file = open(f"output_lists/{fd}_dict.txt", "w")

    file.write(f"{fd} = {{\n")
    for i in desc_dict:
        file.write(f'\t"{i}": "{desc_dict[i].replace("\"", "'")}",\n')
    file.write("}")
    file.close()

def create_sublime_completions(
    game, syntax_scope, scopes
):
    file = open(f"output/{game}Completions.sublime-completions", "w")
    file.write(f'{{\n\t"scope": "{syntax_scope}",\n\t"completions":\n\t[')

    for i in scopes:
        file.write(
            f"""
        {{
            \"trigger\": \"{i}\",
            \"contents\": \"{i}\",
            \"details\": \"{scopes[i].replace("\t", "  ")}\",
            \"kind\": [\"namespace\", \"S\", \"Scope\"]
        }},"""
        )

    file.write("\n\t]\n}")
    file.close()

def write_extra(file):
    file.write(
        "\n    # --------------------------------\n    # -     Manually Added Terms     -\n    # --------------------------------\n\n"
    )
    file.write(
        "    # Essential Scipt Functions\n    - match: \\b(texture|icon)\\b\n      scope: constant.numeric\n"
    )
    file.write(
        "    # Math/Sound\n    - match: \\b(add)\\b\n      scope: variable.language\n"
    )

def write_syntax(iterator, header, scheme_scope, file):
    file.write(f"    # {header}\n    - match: \\b(")
    for i in iterator:
        file.write(f"{i}|")
    file.write(f")\\b\n      scope: {scheme_scope}\n")

def split_write_syntax(iterator, header, scheme_scope, file):
    file.write(f"    # {header}\n    - match: \\b(")
    for index, content in enumerate(iterator):
        if index == 0:
            file.write(f")\\b\n      scope: {scheme_scope}\n")
            file.write(f"    # {header}\n    - match: \\b({content}|")
        elif (index / 75).is_integer():
            file.write(f")\\b\n      scope: {scheme_scope}\n")
            file.write(f"    # {header}\n    - match: \\b({content}|")
        else:
            file.write(f"{content}|")

    file.write(f")\\b\n      scope: {scheme_scope}\n")

def create_sublime_syntax(
    game, syntax_scope, effects, triggers, scopes, modifiers, on_actions
):
    file = open(f"output/{game}Syntax.sublime-syntax", "w")
    file.write(
        f"%YAML 1.2\n---\nname: {game} Scripting\nfile_extensions: [txt]\nscope: {syntax_scope}\n\ncontexts:\n  main:\n    # Comments\n    - match: (#).*$\\n?\n      scope: comment\n"
    )

    write_syntax(on_actions, "On Actions From Code", "keyword.onaction", file)
    split_write_syntax(scopes, "Scopes", "storage.type.scope", file)
    split_write_syntax(effects, "Effects", "keyword.effect", file)
    split_write_syntax(triggers, "Triggers", "string.trigger", file)
    mod_list_out = []
    for i in modifiers:
        mod_out = i.split("C", 1)[0].replace(" ", "")
        mod_list_out.append(mod_out)

    try:
        mod_list_out.remove("")
    except ValueError:
        pass
    split_write_syntax(mod_list_out, "Modifiers", "string.modifier.type", file)
    write_extra(file)
    file.close()

if __name__ == "__main__":
    effects_log = "docs/effects.log"
    triggers_log = "docs/triggers.log"
    event_targets_log = "docs/event_targets.log"

    effects_log_data = get_markdown_log_data(effects_log)    
    write_full_descriptions(effects_log_data, effects_log.replace("docs/", "").replace(".log", ""))

    trigger_log_data = get_markdown_log_data(triggers_log)    
    write_full_descriptions(trigger_log_data, triggers_log.replace("docs/", "").replace(".log", ""))

    scope_log_data = get_markdown_log_data(event_targets_log)    
    write_full_descriptions(scope_log_data, event_targets_log.replace("docs/", "").replace(".log", ""))
    create_sublime_completions("Victoria", "text.vic.script", scope_log_data)

    with open("docs/modifiers.log", "r") as file:
        modifier_text = "".join(file.readlines())
    modifiers = get_modifiers(modifier_text)
    write_full_descriptions(modifiers, "modifiers")

    on_actions = get_on_actions()
    with open("output_lists/on_actions.txt", "w") as file:
        file.write(f"{"\n".join(on_actions)}")

    syntax_scope = "text.vic.script"
    game = "Victoria"

    create_sublime_syntax(
        game, syntax_scope, effects_log_data, trigger_log_data, scope_log_data, modifiers, on_actions
    )
