import sublime
import sublime_plugin
import os
import sys
import subprocess
import re
import time
import struct
import threading
import Default.exec
import json
from .v3_objects import *
from webbrowser import open as openwebsite
from collections import deque
from .jomini import GameObjectBase, PdxScriptObject
from .jomini import dict_to_game_object as make_object
from .Utilities.game_data import GameData
from .Utilities.css import CSS
from .object_cache import GameObjectCache

# ----------------------------------
# -          Plugin Setup          -
# ----------------------------------
settings = sublime.Settings(888)
v3_files_path = ""
v3_mod_files = []
gui_files_path = ""
gui_mod_files = []
css = CSS()
GameData = GameData()
base_object = GameObjectBase()

# global dictionary of game objects used everywhere
game_objects = {
    "ai_strats": base_object,
    "bgs": base_object,
    "buildings": base_object,
    "char_traits": base_object,
    "cultures": base_object,
    "mods": base_object,
    "decrees": base_object,
    "diplo_actions": base_object,
    "diplo_plays": base_object,
    "game_rules": base_object,
    "goods": base_object,
    "gov_types": base_object,
    "ideologies": base_object,
    "institutions": base_object,
    "ig_traits": base_object,
    "igs": base_object,
    "jes": base_object,
    "law_groups": base_object,
    "laws": base_object,
    "parties": base_object,
    "pop_needs": base_object,
    "pop_types": base_object,
    "pm_groups": base_object,
    "pms": base_object,
    "religions": base_object,
    "state_traits": base_object,
    "strategic_regions": base_object,
    "subject_types": base_object,
    "technologies": base_object,
    "terrains": base_object,
    "state_regions": base_object,
    "script_values": base_object,
    "scripted_effects": base_object,
    "scripted_modifiers": base_object,
    "scripted_triggers": base_object,
    "countries": base_object,
    "country_ranks": base_object,
    "country_types": base_object,
    "named_colors": base_object,
    "battle_conditions": base_object,
    "commander_ranks": base_object,
    "culture_graphics": base_object,
    "proposal_types": base_object,
    "discrimination_traits": base_object,
    "gui_types": base_object,
    "gui_templates": base_object,
}


def check_mod_for_changes():
    """
    Check if any changes have been made to mod files
    if changes have been made new game objects need to be generated and cached
    """
    object_cache_path = sublime.packages_path() + f"/Victoria3Tools/object_cache.py"
    if os.stat(object_cache_path).st_size < 200:
        # If there are no objects in the cache, they need to be created
        return True
    mod_cache_path = sublime.packages_path() + f"/Victoria3Tools/mod_cache.txt"
    with open(mod_cache_path, "r") as f:
        # Save lines before writing
        mod_cache = "".join(f.readlines())
    with open(mod_cache_path, "w") as f:
        # Clear
        f.write("")

    for path in v3_mod_files:
        stats_dict = dict()
        mod_name = path.replace("\\", "/").rstrip("/").rpartition("/")[2]
        mod_class_name = mod_name.replace(" ", "")
        for dirpath, dirnames, filenames in os.walk(path):
            mod_files = [
                x for x in filenames if x.endswith(".txt") or x.endswith(".gui")
            ]
            if mod_files:
                for i, j in enumerate(mod_files):
                    full_path = dirpath + "/" + mod_files[i]
                    stats_dict[full_path] = os.stat(full_path).st_mtime

        with open(mod_cache_path, "a") as f:
            f.write("#")
            for i in stats_dict:
                key = re.sub(r"\W|^(?=\d)", "_", i.split(mod_name)[1])
                value = stats_dict[i]
                f.write(f"{key}{value} ")
            f.write("\n")

    with open(mod_cache_path, "r") as f:
        # Save written mod classes
        new_mod_cache = "".join(f.readlines())

    return True if mod_cache != new_mod_cache else False


def get_gui_objects_from_cache():
    global game_objects
    object_cache = GameObjectCache()

    game_objects["gui_types"] = make_object(object_cache.gui_types)
    game_objects["gui_templates"] = make_object(object_cache.gui_templates)


def get_objects_from_cache():
    global game_objects
    object_cache = GameObjectCache()

    for i in game_objects:
        game_objects[i] = make_object(getattr(object_cache, i))


def cache_all_objects():
    # Write all generated objects to cache
    path = sublime.packages_path() + f"/Victoria3Tools/object_cache.py"
    with open(path, "w") as f:
        f.write("class GameObjectCache:\n\tdef __init__(self):")
        for i in game_objects:
            f.write(f"\n\t\tself.{i} = {game_objects[i].to_json()}")


def create_game_objects():
    t0 = time.time()

    def load_first():
        global game_objects
        game_objects["ai_strats"] = V3AiStrategy()
        game_objects["bgs"] = V3BuildingGroup()
        game_objects["buildings"] = V3Building()
        game_objects["char_traits"] = V3CharacterTrait()
        game_objects["cultures"] = V3Culture()
        game_objects["decrees"] = V3Decree()
        game_objects["diplo_actions"] = V3DiplomaticAction()
        game_objects["diplo_plays"] = V3DiplomaticPlay()

    def load_second():
        global game_objects
        game_objects["mods"] = V3Modifier()
        game_objects["game_rules"] = V3GameRules()
        game_objects["goods"] = V3Goods()
        game_objects["gov_types"] = V3GovernmentType()
        game_objects["ideologies"] = V3Ideology()
        game_objects["institutions"] = V3Institutions()
        game_objects["ig_traits"] = V3InterestGroupTrait()
        game_objects["igs"] = V3InterestGroup()

    def load_third():
        global game_objects
        game_objects["jes"] = V3JournalEntry()
        game_objects["law_groups"] = V3LawGroup()
        game_objects["laws"] = V3Law()
        game_objects["parties"] = V3Party()
        game_objects["pop_needs"] = V3PopNeed()
        game_objects["pop_types"] = V3PopType()
        game_objects["pm_groups"] = V3ProductionMethodGroup()

    def load_fourth():
        global game_objects
        game_objects["pms"] = V3ProductionMethod()
        game_objects["religions"] = V3Religion()
        game_objects["script_values"] = V3ScriptValue()
        game_objects["scripted_effects"] = V3ScriptedEffect()
        game_objects["scripted_modifiers"] = V3ScriptedModifier()
        game_objects["scripted_triggers"] = V3ScriptedTrigger()
        game_objects["proposal_types"] = V3ProposalType()
        game_objects["discrimination_traits"] = V3DiscriminationTrait()

    def load_fifth():
        global game_objects
        game_objects["strategic_regions"] = V3StrategicRegion()
        game_objects["subject_types"] = V3SubjectType()
        game_objects["technologies"] = V3Technology()
        game_objects["terrains"] = V3Terrain()
        game_objects["state_regions"] = V3StateRegion()
        game_objects["countries"] = V3Country()
        game_objects["countries"].remove("NOR")

    def load_sixth():
        global game_objects
        game_objects["country_ranks"] = V3CountryRank()
        game_objects["country_types"] = V3CountryType()
        game_objects["culture_graphics"] = V3CultureGraphics()
        game_objects["named_colors"] = V3NamedColor()
        game_objects["battle_conditions"] = V3BattleCondition()
        game_objects["commander_ranks"] = V3CommanderRank()
        game_objects["state_traits"] = V3StateTrait()

    thread1 = threading.Thread(target=load_first)
    thread2 = threading.Thread(target=load_second)
    thread3 = threading.Thread(target=load_third)
    thread4 = threading.Thread(target=load_fourth)
    thread5 = threading.Thread(target=load_fifth)
    thread6 = threading.Thread(target=load_sixth)
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()

    # Write syntax data after creating objects so they actually exist when writing
    sublime.set_timeout_async(lambda: write_data_to_syntax(), 0)

    # Load gui objects after script objects
    sublime.set_timeout_async(lambda: load_gui_objects(), 0)

    t1 = time.time()
    print("Time taken to create Victoria 3 objects: {:.3f} seconds".format(t1 - t0))


def load_gui_objects():
    global game_objects
    game_objects["gui_types"] = GuiType()
    game_objects["gui_templates"] = GuiTemplate()
    game_objects["gui_templates"].remove("inside")
    game_objects["gui_templates"].remove("you")
    game_objects["gui_templates"].remove("can")
    game_objects["gui_templates"].remove("but")
    game_objects["gui_templates"].remove("on")
    game_objects["gui_templates"].remove("within")
    game_objects["gui_templates"].remove("names")

    # Cache created objects
    sublime.set_timeout_async(lambda: cache_all_objects(), 0)


def plugin_loaded():
    global settings, v3_files_path, v3_mod_files, gui_files_path, gui_mod_files
    settings = sublime.load_settings("Victoria Syntax.sublime-settings")
    v3_files_path = settings.get("Victoria3FilesPath")
    v3_mod_files = settings.get("PathsToModFiles")
    gui_files_path = settings.get("GuiBaseGamePath")
    gui_mod_files = settings.get("PathsToGuiModFiles")
    script_enabled = settings.get("EnableVictoriaScriptingFeatures")
    if check_mod_for_changes():
        # Create new objects
        if script_enabled:
            sublime.set_timeout_async(lambda: create_game_objects(), 0)
        else:
            sublime.set_timeout_async(lambda: load_gui_objects(), 0)
    elif not script_enabled:
        get_gui_objects_from_cache()
    else:
        # Load cached objects
        get_objects_from_cache()
    cache_size_limit = settings.get("MaxImageCacheSize")
    cache = sublime.packages_path() + "/Victoria3Tools/Convert DDS/cache/"
    cache_files = [x for x in os.listdir(cache) if x.endswith(".png")]
    if len(cache_files) > cache_size_limit:
        for i in cache_files:
            os.remove(os.path.join(cache, i))
        sublime.status_message("Cleared Image Cache")
    add_color_scheme_scopes()


def add_color_scheme_scopes():
    # Add scopes for yml text formatting to color scheme
    DEFAULT_CS = "Packages/Color Scheme - Default/Monokai.sublime-color-scheme"
    prefs = sublime.load_settings("Preferences.sublime-settings")
    cs = prefs.get("color_scheme", DEFAULT_CS)
    scheme_cache_path = os.path.join(
        sublime.packages_path(), "User", "PdxTools", cs
    ).replace("tmTheme", "sublime-color-scheme")
    if not os.path.exists(scheme_cache_path):
        os.makedirs(os.path.dirname(scheme_cache_path), exist_ok=True)
        rules = """{"variables": {}, "globals": {},"rules": [{"scope": "text.format.white.yml","foreground": "rgb(250, 250, 250)",},{"scope": "text.format.grey.yml","foreground": "rgb(173, 165, 160)",},{"scope": "text.format.red.yml","foreground": "rgb(210, 40, 40)",},{"scope": "text.format.green.yml","foreground": "rgb(40, 210, 40)",},{"scope": "text.format.yellow.yml","foreground": "rgb(255, 255, 0)",},{"scope": "text.format.blue.yml","foreground": "rgb(51, 214, 255)",},{"scope": "text.format.gold.yml","foreground": "#ffb027",},{"scope": "text.format.bold.yml","font_style": "bold"},{"scope": "text.format.italic.yml","font_style": "italic"}]}"""
        with open(scheme_cache_path, "w") as f:
            f.write(rules)


def write_data_to_syntax():
    fake_syntax_path = (
        sublime.packages_path()
        + "/Victoria3Tools/Vic3 Script/VictoriaScript.fake-sublime-syntax"
    )
    real_syntax_path = (
        sublime.packages_path()
        + "/Victoria3Tools/Vic3 Script/VictoriaScript.sublime-syntax"
    )
    with open(fake_syntax_path, "r") as file:
        lines = file.read()

    # Append all other matches to auto-generated-content section
    lines += write_syntax(
        game_objects["scripted_triggers"].keys(),
        "Scripted Triggers",
        "string.scripted.trigger",
    )
    lines += write_syntax(
        game_objects["scripted_effects"].keys(),
        "Scripted Effects",
        "keyword.scripted.effect",
    )
    lines += write_syntax(
        game_objects["script_values"].keys(),
        "Scripted Values",
        "storage.type.script.value",
    )

    # All GameObjects get entity.name scope
    lines += write_syntax(
        game_objects["ai_strats"].keys(), "Ai Strategies", "entity.name.ai.strat"
    )
    lines += write_syntax(
        game_objects["bgs"].keys(), "Building Groups", "entity.name.bg"
    )
    lines += write_syntax(
        game_objects["buildings"].keys(), "Buildings", "entity.name.building"
    )
    lines += write_syntax(
        game_objects["char_traits"].keys(),
        "Character Traits",
        "entity.name.character.trait",
    )
    lines += write_syntax(
        game_objects["cultures"].keys(), "Cultures", "entity.name.culture"
    )
    lines += write_syntax(
        game_objects["mods"].keys(), "Modifiers", "entity.name.modifier"
    )
    lines += write_syntax(
        game_objects["decrees"].keys(), "Decrees", "entity.name.decree"
    )
    lines += write_syntax(
        game_objects["diplo_actions"].keys(),
        "Diplomatic Actions",
        "entity.name.diplo.action",
    )
    lines += write_syntax(
        game_objects["diplo_plays"].keys(), "Diplomatic Plays", "entity.name.diplo.play"
    )
    lines += write_syntax(
        game_objects["game_rules"].keys(), "Game Rules", "entity.name.game.rule"
    )
    lines += write_syntax(
        game_objects["goods"].keys(), "Trade Goods", "entity.name.trade.good"
    )
    lines += write_syntax(
        game_objects["gov_types"].keys(), "Gov Types", "entity.name.gov.type"
    )
    lines += write_syntax(
        game_objects["ideologies"].keys(), "Ideologies", "entity.name.ideology"
    )
    lines += write_syntax(
        game_objects["institutions"].keys(), "Institutions", "entity.name.institution"
    )
    lines += write_syntax(
        game_objects["ig_traits"].keys(), "Ig Traits", "entity.name.ig.trait"
    )
    lines += write_syntax(
        game_objects["igs"].keys(), "Interest Groups", "entity.name.interest.group"
    )
    lines += write_syntax(
        game_objects["jes"].keys(), "Journal Entries", "entity.name.journal.entry"
    )
    lines += write_syntax(
        game_objects["law_groups"].keys(), "Law Groups", "entity.name.law.group"
    )
    lines += write_syntax(game_objects["laws"].keys(), "Laws", "entity.name.law")
    lines += write_syntax(
        game_objects["parties"].keys(), "Parties", "entity.name.party"
    )
    lines += write_syntax(
        game_objects["pop_needs"].keys(), "Pop Needs", "entity.name.pop.need"
    )
    lines += write_syntax(
        game_objects["pop_types"].keys(), "Pop Types", "entity.name.pop.type"
    )
    lines += write_syntax(
        game_objects["pm_groups"].keys(),
        "Production Method Groups",
        "entity.name.pm.groups",
    )
    lines += write_syntax(
        game_objects["pms"].keys(), "Production Methods", "entity.name.pm"
    )
    lines += write_syntax(
        game_objects["religions"].keys(), "Religions", "entity.name.religion"
    )
    lines += write_syntax(
        game_objects["state_traits"].keys(), "State Traits", "entity.name.state.trait"
    )
    lines += write_syntax(
        game_objects["strategic_regions"].keys(),
        "Strategic Regions",
        "entity.name.strategic.region",
    )
    lines += write_syntax(
        game_objects["subject_types"].keys(),
        "Subject Types",
        "entity.name.subject.type",
    )
    lines += write_syntax(
        game_objects["technologies"].keys(), "Technologies", "entity.name.tech"
    )
    lines += write_syntax(
        game_objects["terrains"].keys(), "Terrains", "entity.name.terrain"
    )
    lines += write_syntax(
        game_objects["state_regions"].keys(),
        "State Regions",
        "entity.name.state.region",
    )
    lines += write_syntax(
        game_objects["countries"].keys(), "Countries", "entity.name.countries"
    )
    lines += write_syntax(
        game_objects["country_ranks"].keys(),
        "Country Ranks",
        "entity.name.country.ranks",
    )
    lines += write_syntax(
        game_objects["country_types"].keys(),
        "Country Types",
        "entity.name.country.types",
    )
    lines += write_syntax(
        game_objects["culture_graphics"].keys(),
        "Culture Graphics",
        "entity.name.culture.graphics",
    )
    lines += write_syntax(
        game_objects["named_colors"].keys(), "Named Colors", "entity.name.named.colors"
    )
    lines += write_syntax(
        game_objects["battle_conditions"].keys(),
        "Battle Conditions",
        "entity.name.battle.conditions",
    )
    lines += write_syntax(
        game_objects["commander_ranks"].keys(),
        "Commander Ranks",
        "entity.name.commander.ranks",
    )
    lines += write_syntax(
        game_objects["proposal_types"].keys(),
        "Proposal Types",
        "entity.name.proposal.type",
    )
    lines += write_syntax(
        game_objects["discrimination_traits"].keys(),
        "Discrimination Traits",
        "entity.name.discrimination.trait",
    )

    # Dynamic modifiers
    country_modifs = list()
    state_modifs = list()
    ig_modifs = list()
    bg_modifs = list()
    building_modifs = list()
    character_modifs = list()
    goods_modifs = list()

    # interest_group_(IG)_pol_str_mult
    # interest_group_(IG)_approval_add
    # interest_group_(IG)_pop_attraction_mult
    for i in game_objects["igs"].keys():
        ig_modifs.append(f"interest_group_{i}_pol_str_mult")
        ig_modifs.append(f"interest_group_{i}_approval_add")
        ig_modifs.append(f"interest_group_{i}_pop_attraction_mult")

    # building_group_(BG)_(POP_TYPE)_fertility_mult
    # building_group_(BG)_(POP_TYPE)_mortality_mult
    # building_group_(BG)_(POP_TYPE)_standard_of_living_add
    # building_group_(BG)_tax_mult
    # building_group_(BG)_employee_mult
    # country_subsidies_(BG)
    for i in game_objects["bgs"].keys():
        bg_modifs.append(f"building_group_{i}_tax_mult")
        bg_modifs.append(f"building_group_{i}_employee_mult")
        bg_modifs.append(f"building_group_{i}_throughput_mult")
        country_modifs.append(f"country_subsidies_{i}")
        for j in game_objects["pop_types"].keys():
            bg_modifs.append(f"building_group_{i}_{j}_fertility_mult")
            bg_modifs.append(f"building_group_{i}_{j}_mortality_mult")
            bg_modifs.append(f"building_group_{i}_{j}_standard_of_living_add")

    # building_output_(TRADE_GOOD)_add
    # building_input_(TRADE_GOOD)_add
    # building_output_(TRADE_GOOD)_mult
    for i in game_objects["goods"].keys():
        building_modifs.append(f"building_output_{i}_add")
        building_modifs.append(f"building_input_{i}_add")
        building_modifs.append(f"building_output_{i}_mult")
        goods_modifs.append(f"goods_input_{i}_add")
        goods_modifs.append(f"goods_output_{i}_add")

    # building_(BUILDING)_throughput_mult
    for i in game_objects["buildings"].keys():
        building_modifs.append(f"{i}_throughput_mult")

    # character_(BATTLE_CONDITION)_mult
    for i in game_objects["battle_conditions"].keys():
        character_modifs.append(f"character_{i}_mult")

    # state_(RELIGION)_standard_of_living_add
    for i in game_objects["religions"].keys():
        state_modifs.append(f"state_{i}_standard_of_living_add")

    # country_(INSTITUTION)_max_investment_add
    for i in game_objects["institutions"].keys():
        state_modifs.append(f"country_{i}_max_investment_add")

    for i in game_objects["pop_types"].keys():
        country_modifs.append(f"country_{i}_pol_str_mult")
        country_modifs.append(f"country_{i}_voting_power_add")
        state_modifs.append(f"state_{i}_mortality_mult")
        state_modifs.append(f"state_{i}_dependent_wage_mult")
        building_modifs.append(f"building_employment_{i}_add")
        building_modifs.append(f"building_employment_{i}_mult")
        building_modifs.append(f"{i}_fertility_mult")
        building_modifs.append(f"{i}_mortality_mult")
        state_modifs.append(f"state_{i}_investment_pool_contribution_add")
        state_modifs.append(f"state_{i}_investment_pool_efficiency_mult")
        building_modifs.append(f"{i}_shares_add")
        building_modifs.append(f"{i}_shares_mult")

    for i in game_objects["laws"].keys():
        state_modifs.append(f"state_pop_support_{i}_add")
        state_modifs.append(f"state_pop_support_{i}_add")
        state_modifs.append(f"state_pop_support_{i}_mult")

    lines += write_syntax(
        country_modifs,
        "Country Modifier Types",
        "string.modifier.type",
    )
    lines += write_syntax(
        state_modifs,
        "State Modifier Types",
        "string.modifier.type",
    )
    lines += write_syntax(
        ig_modifs,
        "Interest Group Modifier Types",
        "string.modifier.type",
    )
    lines += write_syntax(
        bg_modifs,
        "Building Group Modifier Types",
        "string.modifier.type",
    )
    lines += write_syntax(
        building_modifs,
        "Building Modifier Types",
        "string.modifier.type",
    )
    lines += write_syntax(
        character_modifs,
        "Character Modifier Types",
        "string.modifier.type",
    )
    lines += write_syntax(
        goods_modifs,
        "Trade Good Modifier Types",
        "string.trade.good.type",
    )

    with open(real_syntax_path, "r") as file:
        real_lines = file.read()

    if real_lines != lines:
        with open(real_syntax_path, "w", encoding="utf-8") as file:
            file.write(lines)


def write_syntax(li, header, scope):
    count = 0
    string = f"\n    # Generated {header}\n    - match: \\b("
    for i in li:
        count += 1
        # Count is needed to split because columns are waaay too long for syntax regex
        if count == 0:
            string = f")\\b\n      scope: {scope}\n"
            string += f"    # Generated {header}\n    - match: \\b({i}|"
        elif count == 75:
            string += f")\\b\n      scope: {scope}\n"
            string += f"    # Generated {header}\n    - match: \\b({i}|"
            count = 1
        else:
            string += f"{i}|"
    string += f")\\b\n      scope: {scope}"
    return string


class V3CompletionsEventListener(sublime_plugin.EventListener):
    def __init__(self):
        self.fields = {
            # Note: these need to have the same names as they do in the game_objects dict
            "trigger_field": [],
            "effect_field": [],
            "modifier_field": [],
            "mtth_field": [],
            "ai_strats": [],
            "buildings": [],
            "bgs": [],
            "char_traits": [],
            "cultures": [],
            "decrees": [],
            "diplo_actions": [],
            "diplo_plays": [],
            "game_rules": [],
            "goods": [],
            "gov_types": [],
            "ideologies": [],
            "igs": [],
            "institutions": [],
            "jes": [],
            "law_groups": [],
            "laws": [],
            "mods": [],
            "parties": [],
            "pop_types": [],
            "pms": [],
            "religions": [],
            "state_traits": [],
            "strategic_regions": [],
            "subject_types": [],
            "technologies": [],
            "terrains": [],
            "state_regions": [],
            "countries": [],
            "country_ranks": [],
            "country_types": [],
            "culture_graphics": [],
            "named_colors": [],
            "battle_conditions": [],
            "commander_ranks": [],
            "proposal_types": [],
            "discrimination_traits": [],
        }
        for field in self.fields.keys():
            setattr(self, field, False)

    def on_deactivated_async(self, view):
        """
        Remove field states when view loses focus
        if cursor was in a field in the old view but not the new view the completions will still be accurate
        save the id of the view so it can be readded when it regains focus
        """

        if not settings.get("EnableVictoriaScriptingFeatures"):
            return

        vid = view.id()
        for field, views in self.fields.items():
            if getattr(self, field):
                setattr(self, field, False)
                views.append(vid)

    def on_activated_async(self, view):
        if not settings.get("EnableVictoriaScriptingFeatures"):
            return

        vid = view.id()
        for field, views in self.fields.items():
            if vid in views:
                setattr(self, field, True)
                views.remove(vid)

    def create_completion_list(self, flag_name, completion_kind):
        if not getattr(self, flag_name, False):
            return None

        completions = game_objects[flag_name].keys()
        completions = sorted(completions)
        return sublime.CompletionList(
            [
                sublime.CompletionItem(
                    trigger=key,
                    completion_format=sublime.COMPLETION_FORMAT_TEXT,
                    kind=completion_kind,
                    details=" ",
                )
                # Calling sorted() twice makes it so completions are ordered by
                # 1. the number of times they appear in the current buffer
                # 2. if they dont appear they show up alphabetically
                for key in sorted(completions)
            ],
            flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
            | sublime.INHIBIT_WORD_COMPLETIONS,
        )

    def on_query_completions(self, view, prefix, locations):
        if not view:
            return None

        try:
            if (
                view.syntax().name != "Victoria Script"
                and view.syntax().name != "PdxPython"
            ):
                return None
        except AttributeError:
            return None

        if not settings.get("EnableVictoriaScriptingFeatures"):
            return

        fname = view.file_name()

        completion_flag_pairs = [
            ("ai_strats", (sublime.KIND_ID_MARKUP, "A", "Ai Strategy")),
            ("buildings", (sublime.KIND_ID_VARIABLE, "B", "Building")),
            ("bgs", (sublime.KIND_ID_VARIABLE, "B", "Building Group")),
            ("char_traits", (sublime.KIND_ID_VARIABLE, "C", "Character Trait")),
            ("cultures", (sublime.KIND_ID_NAMESPACE, "C", "Culture")),
            ("decrees", (sublime.KIND_ID_MARKUP, "D", "Decree")),
            ("diplo_actions", (sublime.KIND_ID_SNIPPET, "D", "Diplomatic Action")),
            ("diplo_plays", (sublime.KIND_ID_SNIPPET, "D", "Diplomatic Play")),
            ("game_rules", (sublime.KIND_ID_FUNCTION, "G", "Game Rule")),
            ("goods", (sublime.KIND_ID_NAMESPACE, "G", "Trade Good")),
            ("gov_types", (sublime.KIND_ID_SNIPPET, "G", "Government Type")),
            ("ideologies", (sublime.KIND_ID_NAVIGATION, "I", "Ideology")),
            ("institutions", (sublime.KIND_ID_NAVIGATION, "I", "Institution")),
            ("igs", (sublime.KIND_ID_MARKUP, "I", "Interest Group")),
            ("jes", (sublime.KIND_ID_TYPE, "J", "Journal Entry")),
            ("law_groups", (sublime.KIND_ID_VARIABLE, "L", "Law Group")),
            ("laws", (sublime.KIND_ID_VARIABLE, "L", "Law")),
            ("mods", (sublime.KIND_ID_SNIPPET, "M", "Modifier")),
            ("parties", (sublime.KIND_ID_TYPE, "P", "Political Party")),
            ("pop_types", (sublime.KIND_ID_VARIABLE, "P", "Pop Type")),
            ("pms", (sublime.KIND_ID_NAVIGATION, "P", "Production Method")),
            ("religions", (sublime.KIND_ID_NAMESPACE, "R", "Religion")),
            ("state_traits", (sublime.KIND_ID_VARIABLE, "S", "State Trait")),
            ("strategic_regions", (sublime.KIND_ID_SNIPPET, "S", "Strategic Region")),
            ("subject_types", (sublime.KIND_ID_TYPE, "S", "Subject Type")),
            ("technologies", (sublime.KIND_ID_VARIABLE, "T", "Technology")),
            ("terrains", (sublime.KIND_ID_NAVIGATION, "T", "Terrain")),
            ("state_regions", (sublime.KIND_ID_NAMESPACE, "S", "State Region")),
            ("countries", (sublime.KIND_ID_NAMESPACE, "C", "Country")),
            ("country_ranks", (sublime.KIND_ID_NAMESPACE, "C", "Country Ranks")),
            ("country_types", (sublime.KIND_ID_NAMESPACE, "C", "Country Types")),
            ("culture_graphics", (sublime.KIND_ID_NAMESPACE, "C", "Country Types")),
            ("named_colors", (sublime.KIND_ID_VARIABLE, "C", "Named Color")),
            ("battle_conditions", (sublime.KIND_ID_VARIABLE, "B", "Battle Condition")),
            ("commander_ranks", (sublime.KIND_ID_VARIABLE, "C", "Commander Rank")),
            ("proposal_types", (sublime.KIND_ID_VARIABLE, "P", "Proposal Types")),
            (
                "discrimination_traits",
                (sublime.KIND_ID_VARIABLE, "D", "Discrimination Traits"),
            ),
        ]

        for flag, completion in completion_flag_pairs:
            completion_list = self.create_completion_list(flag, completion)
            if completion_list is not None:
                return completion_list

        # Special completions
        if "script_values" in fname or "scripted_modifiers" in fname:
            e_list = []
            for i in GameData.EffectsList:
                e_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
                        details=GameData.EffectsList[i].split("<br>")[0],
                    )
                )
            t_list = []
            for i in GameData.TriggersList:
                t_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
                        details=GameData.TriggersList[i].split("<br>")[0],
                    )
                )
            return sublime.CompletionList(e_list + t_list)
        if self.trigger_field or "scripted_triggers" in fname:
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
                        details=GameData.TriggersList[key].split("<br>")[0],
                    )
                    for key in sorted(GameData.TriggersList)
                ]
            )
        if self.mtth_field:
            x = dict(sorted(GameData.ValueFieldCompletionList.items()))
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "V", "Value"),
                        details=GameData.ValueFieldCompletionList[key],
                    )
                    for key in x
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS
                | sublime.INHIBIT_REORDER,
            )
        if (
            self.effect_field
            or "scripted_effects" in fname
            or "common/history" in fname
        ):
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
                        details=GameData.EffectsList[key].split("<br>")[0],
                    )
                    for key in sorted(GameData.EffectsList)
                ]
            )
        if self.modifier_field or re.search("modifiers", fname):
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_MARKUP, "M", "Modifier"),
                        details=GameData.ModifiersList[key],
                        annotation=GameData.ModifiersList[key].replace(
                            "Category: ", ""
                        ),
                    )
                    for key in sorted(GameData.ModifiersList)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        return None

    # Get the index of a closing bracket in a string given the starting brackets index
    def getIndex(self, string, index):
        if string[index] != "{":
            return -1
        d = deque()
        for k in range(index, len(string)):
            if string[k] == "}":
                d.popleft()
            elif string[k] == "{":
                d.append(string[index])
            if not d:
                return k + 1
        return -1

    def get_regions(self, view, selector, view_str):
        start_brackets = view.find_by_selector(selector)
        return [
            sublime.Region(br.a, self.getIndex(view_str, br.a)) for br in start_brackets
        ]

    def simple_scope_match(self, view):
        selection = view.sel()
        if not selection[0].empty():
            return

        view_str = view.substr(sublime.Region(0, view.size()))

        # Get the starting bracket index from the syntax scopes
        trigger_regions = self.get_regions(view, "meta.trigger.bracket", view_str)
        effect_regions = self.get_regions(view, "meta.effect.bracket", view_str)
        value_regions = self.get_regions(view, "meta.value.bracket", view_str)
        modifier_regions = self.get_regions(view, "meta.modifier.bracket", view_str)

        self.show_status(selection[0].a, trigger_regions, "trigger", view)

        # Have to account for trigger fields inside of effect fields, definetly a better way to do this.
        for block in effect_regions:
            if block.a <= selection[0].a <= block.b:
                view.set_status("effect", "Effect Field")
                self.effect_field = True
                for block in trigger_regions:
                    if block.a <= selection[0].a <= block.b:
                        view.erase_status("effect")
                        self.effect_field = False
                        view.set_status("trigger", "Trigger Field")
                        self.trigger_field = True
                        break
                    else:
                        view.erase_status("trigger")
                        self.trigger_field = False
                break
            else:
                view.erase_status("effect")
                self.effect_field = False

        self.show_status(selection[0].a, modifier_regions, "modifier", view)

        self.show_status(selection[0].a, value_regions, "value", view)

        # For actual mtth fields that have a modifier = {} block inside of them, remove the modifier status
        if self.mtth_field and self.modifier_field:
            view.erase_status("modifier")

    def show_status(self, selection, regions, status, view):
        for block in regions:
            if block.a <= selection <= block.b:
                view.set_status(status, status.title() + " Field")
                if status == "trigger":
                    self.trigger_field = True
                elif status == "effect":
                    self.effect_field = True
                elif status == "modifier":
                    self.modifier_field = True
                elif status == "value":
                    self.mtth_field = True
                break
            else:
                view.erase_status(status)
                if status == "trigger":
                    self.trigger_field = False
                elif status == "effect":
                    self.effect_field = False
                elif status == "modifier":
                    self.modifier_field = False
                elif status == "value":
                    self.mtth_field = False

    def reset_shown(self):
        excluded_fields = (
            "trigger_field",
            "effect_field",
            "modifier_field",
            "mtth_field",
        )
        for i in self.fields.keys():
            if i not in excluded_fields:
                setattr(self, i, False)

    def check_for_patterns_and_set_flag(
        self, patterns_list, flag_name, view, line, point
    ):
        for pattern in patterns_list:
            r = re.search(f'{pattern}\s?=\s?(")?', line)
            if r:
                y = 0
                idx = line.index(pattern) + view.line(point).a + len(pattern) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    setattr(self, flag_name, True)
                    view.run_command("auto_complete")
                    return True
        return False

    def check_pattern_and_set_flag(self, pattern, flag_name, view, line, point):
        if pattern in line:
            idx = line.index(pattern) + view.line(point).a + len(pattern)
            if idx == point:
                setattr(self, flag_name, True)
                view.run_command("auto_complete")

    def check_for_simple_completions(self, view, point):
        """
        Check if the current cursor position should trigger a autocompletion item
        this is for simple declarations like: remove_building = CursorHere
        """
        self.reset_shown()

        if view.substr(point) == "=":
            return

        line = view.substr(view.line(point))

        ai_list = ["has_strategy", "set_strategy"]
        b_list = [
            "start_building_construction",
            "remove_building",
            "start_building_construction",
            "activate_building",
            "deactivate_building",
            "start_privately_funded_building_construction",
            "building",
            "building_type",
            "has_building",
            "is_building_type",
            "pop_employment_building",
            "has_active_building",
            "set_available_for_autonomous_investment",
            "unset_available_for_autonomous_investment",
            "start_privately_funded_building_construction",
        ]
        bg_list = [
            "force_resource_depletion",
            "force_resource_discovery",
            "pop_employment_building_group",
            "is_building_group",
            "has_potential_resource",
            "building_group",
        ]
        char_traits_list = ["add_trait", "remove_trait", "has_trait"]
        culture_list = [
            "has_culture_graphics",
            "country_has_primary_culture",
            "has_pop_culture",
            "is_homeland",
            "add_homeland",
            "remove_homeland",
            "culture",
        ]
        decree_list = ["has_decree"]
        diplo_action_list = ["is_diplomatic_action_type"]
        diplo_play_list = ["is_diplomatic_play_type"]
        game_rules_list = ["has_game_rule"]
        trade_goods_list = [
            "add_cultural_obsession",
            "remove_cultural_obsession",
            "is_taxing_goods",
            "has_cultural_obsession",
            "is_banning_goods",
        ]
        gov_types_list = ["has_government_type"]
        ideologies_list = [
            # "has_ideology", # these 2 take ideology:x
            # "set_ideology",
            "add_ideology",
            "remove_ideology",
            "ideology",
        ]
        institutions_list = ["expanding_institution", "has_institution", "institution"]
        ig_list = [
            "has_ruling_interest_group",
            "is_interest_group_type",
            "law_approved_by",
            "interest_group",
        ]
        journal_list = ["has_journal_entry"]
        modifier_list = ["has_modifier", "remove_modifier"]
        party_list = ["is_party_type"]
        pops_list = ["is_pop_type", "pop_type"]
        pms_list = ["has_active_production_method", "production_method"]
        religions_list = ["has_pop_religion", "religion"]
        state_trait_list = ["has_state_trait"]
        strategic_regions_list = [
            "add_declared_interest",
            "has_interest_marker_in_region",
            "hq",
        ]
        subject_type_list = ["is_subject_type", "change_subject_type"]
        tech_list = [
            "technology",
            "add_technology_researched",
            "can_research",
            "has_technology_progress",
            "has_technology_researched",
            "is_researching_technology",
            "is_researching_technology_category",
        ]
        terrain_list = ["has_terrain"]
        state_regions_list = [
            "set_capital",
            "set_market_capital",
            "country_or_subject_owns_entire_state_region",
            "has_state_in_state_region",
            "owns_entire_state_region",
            "owns_treaty_port_in",
        ]

        country_types = ["is_country_type", "country_type"]
        culture_graphics = ["has_culture_graphics", "graphics"]
        named_colors = ["color", "color1", "color2", "color3", "color4", "color5"]
        commander_ranks = ["commander_rank"]
        battle_conditions = ["has_battle_condition"]

        proposal_types_list = ["post_proposal"]
        discrimination_traits_list = ["has_discrimination_trait"]

        # Define the lists of patterns and corresponding flags
        pattern_flag_pairs = [
            (ai_list, "ai_strats"),
            (b_list, "buildings"),
            (bg_list, "bgs"),
            (char_traits_list, "char_traits"),
            (culture_list, "cultures"),
            (decree_list, "decrees"),
            (diplo_action_list, "diplo_actions"),
            (diplo_play_list, "diplo_plays"),
            (game_rules_list, "game_rules"),
            (trade_goods_list, "goods"),
            (gov_types_list, "gov_types"),
            (ideologies_list, "ideologies"),
            (institutions_list, "institutions"),
            (ig_list, "igs"),
            (journal_list, "jes"),
            (modifier_list, "mods"),
            (party_list, "parties"),
            (pops_list, "pop_types"),
            (pms_list, "pms"),
            (religions_list, "religions"),
            (state_trait_list, "state_traits"),
            (strategic_regions_list, "strategic_regions"),
            (subject_type_list, "subject_types"),
            (tech_list, "technologies"),
            (terrain_list, "terrains"),
            (state_regions_list, "state_regions"),
            (country_types, "country_types"),
            (culture_graphics, "culture_graphics"),
            (named_colors, "named_colors"),
            (battle_conditions, "battle_conditions"),
            (commander_ranks, "commander_ranks"),
            (proposal_types_list, "proposal_types"),
            (discrimination_traits_list, "discrimination_traits"),
        ]

        # Define the list of scope patterns and corresponding flags
        scope_pattern_flag_pairs = [
            ("b:", "buildings"),
            ("cu:", "cultures"),
            ("decree_cost:", "decrees"),
            ("goods:", "goods"),
            ("g:", "goods"),
            ("institution:", "institutions"),
            ("ig:", "igs"),
            ("interest_group:", "igs"),
            ("je:", "jes"),
            ("active_law:", "law_groups"),
            ("law_type:", "laws"),
            ("py:", "parties"),
            ("party:", "parties"),
            ("pop_type:", "pop_types"),
            ("rel:", "religions"),
            ("religion:", "religions"),
            ("sr:", "strategic_regions"),
            ("s:", "state_regions"),
            ("c:", "countries"),
            ("rank_value:", "country_ranks"),
        ]

        for patterns, flag in pattern_flag_pairs:
            if self.check_for_patterns_and_set_flag(patterns, flag, view, line, point):
                return

        for pattern, flag in scope_pattern_flag_pairs:
            self.check_pattern_and_set_flag(pattern, flag, view, line, point)

    def check_region_and_set_flag(
        self, selector, flag_name, view, view_str, point, string_check_and_move=None
    ):
        for br in view.find_by_selector(selector):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            s = view.substr(i)
            if string_check_and_move and string_check_and_move[0] in s:
                fpoint = (
                    s.index(string_check_and_move[0]) + string_check_and_move[1]
                ) + i.a
                if fpoint == point:
                    setattr(self, flag_name, True)
                    view.run_command("auto_complete")
            elif i.contains(point):
                setattr(self, flag_name, True)
                view.run_command("auto_complete")

    def check_complex_completions(self, view, point):
        view_str = view.substr(sublime.Region(0, view.size()))

        # Define the list of selectors and corresponding flags
        selector_flag_pairs = [
            ("meta.ig.bracket", "igs"),
            ("meta.goods.simple.bracket", "goods"),
            ("meta.ideology.bracket", "ideologies"),
            ("meta.law.bracket", "laws"),
            ("meta.tech.bracket", "technologies"),
            ("meta.bg.bracket", "bgs", ("type = ", 7)),
            ("meta.da.bracket", "diplo_actions", ("type = ", 7)),
            ("meta.dp.bracket", "diplo_plays", ("type = ", 7)),
            ("meta.je.bracket", "jes", ("type = ", 7)),
            ("meta.mods.bracket", "mods", ("name = ", 7)),
            ("meta.subjects.bracket", "subject_types", ("type = ", 7)),
        ]

        for pair in selector_flag_pairs:
            if len(pair) == 3:
                selector, flag, string_check_and_move = pair
                self.check_region_and_set_flag(
                    selector, flag, view, view_str, point, string_check_and_move
                )
            else:
                selector, flag = pair
                self.check_region_and_set_flag(selector, flag, view, view_str, point)

    def on_selection_modified(self, view):
        if not view:
            return

        try:
            if (
                view.syntax().name != "Victoria Script"
                and view.syntax().name != "PdxPython"
            ):
                return
        except AttributeError:
            return

        if not settings.get("EnableVictoriaScriptingFeatures"):
            return

        self.simple_scope_match(view)
        # Only do when there is 1 selection, doens't make sense with multiple selections
        if len(view.sel()) == 1:
            self.check_for_simple_completions(view, view.sel()[0].a)
            self.check_complex_completions(view, view.sel()[0].a)


# ----------------------------------
# -     Text & Window Commands     -
# ----------------------------------


class LocalizeCurrentFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window = sublime.active_window()
        view = window.active_view()
        view_region = sublime.Region(0, view.size())
        view_str = view.substr(view_region)
        loc_list = self.localize_tokens(view_str)

        # Insert into new view
        window.run_command("new_file")
        loc_view = window.active_view()
        loc_view.set_name("Localization")
        for i in loc_list:
            loc_view.insert(edit, len(loc_view), i)

    def localize_tokens(self, file_contents):
        out_list = []
        file_contents = file_contents.replace("desc = {", "").replace(
            "custom_tooltip = {", ""
        )
        out = re.sub("(#).*", "", file_contents)
        out = out.replace(" ", "")
        out = re.findall(
            r"(title|desc|name|custom_tooltip|text|flavor)\s?=\s?(.+)", out
        )

        for i in out:
            key = i[1].replace('"', "")
            # Exclude modifiers and variables
            if (
                key.endswith("_mod")
                or key.endswith("_var")
                or key.endswith("_cooldown")
            ):
                pass
            else:
                if (
                    not key.endswith("tt")
                    and not key.endswith("ttt")
                    and key.endswith(".t")
                    or key.endswith("title")
                ):
                    loced = key.replace("_", " ")
                    key = "\n" + key + ':0 "' + loced + '"'
                else:
                    loced = key.replace("_", " ")
                    key = "\n" + key + ':0 "' + loced + '"'
                    key = key.replace("\t", "")
                out_list.append(key)

        return out_list


class FolderHandler(sublime_plugin.TextCommand):
    def input_description(self):
        return "Fold Level"

    def input(self, args):
        if "level" not in args:
            return FoldingInputHandler()

    def run(self, edit, level):
        if level != "Unfold All":
            self.view.run_command("fold_by_level", {"level": int(level)})
        else:
            self.view.run_command("unfold_all")


class FoldingInputHandler(sublime_plugin.ListInputHandler):
    def name(self):
        return "level"

    def list_items(self):
        keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "Unfold All"]
        return keys


# ----------------------------------
# -            Validator           -
# ----------------------------------


class ValidatorOnSaveListener(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        if view is None:
            return
        try:
            if view.syntax().name != "Victoria Script":
                return
        except AttributeError:
            return
        if settings.get("ScriptValidator") is False:
            return

        if not settings.get("EnableVictoriaScriptingFeatures"):
            return

        self.view = view
        self.view_str = view.substr(sublime.Region(0, view.size()))

        in_mod_dir = any(
            [
                x
                for x in v3_mod_files
                if self.is_file_in_mod_directory(self.view.file_name(), x)
            ]
        )

        if in_mod_dir:
            self.encoding_check()

    def encoding_check(self):
        # Check that the current filepath is in a folder that should use UTF-8 with BOM
        # If it should be UTF-8 with BOM and it is not create error panel
        path = self.view.file_name()
        # Coat of arms is the only files that are only UTF-8 not UTF-8 with BOM
        utf8_paths = re.search(r"(common/coat_of_arms)", path)
        bom_paths = re.search(r"(events|common|music|localization)", path)
        with open(path, "r+b") as fp:
            old_encoding = self.view.encoding()
            if not old_encoding == "UTF-8 with BOM":
                if bom_paths is not None and utf8_paths is None:
                    # is not bom and should be
                    self.view.set_encoding("UTF-8 with BOM")
                    error_message = f"EncodingError: Encoding is {old_encoding}, files in {bom_paths.group()} should be UTF-8 with BOM, resave to fix."

                    panel = self.create_error_panel()
                    panel.set_read_only(False)
                    panel.run_command("append", {"characters": error_message})
                    panel.add_regions(
                        "bad_encoding",
                        [sublime.Region(27, 27 + len(old_encoding))],
                        "underline.bad",
                        flags=(
                            sublime.DRAW_SOLID_UNDERLINE
                            | sublime.DRAW_NO_FILL
                            | sublime.DRAW_NO_OUTLINE
                        ),
                    )
                    panel.add_regions(
                        "encoding",
                        [sublime.Region(len(panel) - 30, len(panel) - 16)],
                        "underline.good",
                        flags=(
                            sublime.DRAW_SOLID_UNDERLINE
                            | sublime.DRAW_NO_FILL
                            | sublime.DRAW_NO_OUTLINE
                        ),
                    )
                    panel.set_read_only(True)

                if utf8_paths is not None and not old_encoding == "UTF-8":
                    # is not utf-8 and should be
                    self.view.set_encoding("UTF-8")
                    error_message = f"EncodingError: Encoding is {old_encoding}, files in {utf8_paths.group()} should be UTF-8, resave to fix."

                    panel = self.create_error_panel()
                    panel.set_read_only(False)
                    panel.run_command("append", {"characters": error_message})
                    # bad encoding
                    panel.add_regions(
                        "bad_encoding",
                        [sublime.Region(27, 27 + len(old_encoding))],
                        "underline.bad",
                        flags=(
                            sublime.DRAW_SOLID_UNDERLINE
                            | sublime.DRAW_NO_FILL
                            | sublime.DRAW_NO_OUTLINE
                        ),
                    )
                    # new good encoding
                    panel.add_regions(
                        "encoding",
                        [sublime.Region(len(panel) - 21, len(panel) - 16)],
                        "underline.good",
                        flags=(
                            sublime.DRAW_SOLID_UNDERLINE
                            | sublime.DRAW_NO_FILL
                            | sublime.DRAW_NO_OUTLINE
                        ),
                    )
                    panel.set_read_only(True)

    def create_error_panel(self):
        window = sublime.active_window()
        panel = window.create_output_panel("error", unlisted=True)
        panel.assign_syntax("scope:text.error")
        panel.settings().set("color_scheme", "ErrorPanel.hidden-color-scheme")
        panel.settings().set("gutter", False)
        window.run_command("show_panel", {"panel": "output.error"})
        window.focus_view(panel)
        return panel

    def is_file_in_mod_directory(self, file_path, directory_path):
        if not os.path.exists(file_path):
            return False

        if not os.path.exists(directory_path):
            return False

        absolute_file_path = os.path.abspath(file_path)
        absolute_directory_path = os.path.abspath(directory_path)

        common_path = os.path.commonpath([absolute_file_path, absolute_directory_path])

        return common_path == absolute_directory_path


# ----------------------------------
# -     Shader Intrinsic Hover     -
# ----------------------------------


def OpenMSDNLink(text):
    openStyle = 2
    openStyleSetting = settings.get("IntrinsicHoverLinkOpenStyle", "new_tab")
    if openStyleSetting == "same_window":
        openStyle = 0
    elif openStyleSetting == "new_window":
        openStyle = 1

    openwebsite(text, openStyle)


class IntrinsicHoverListener(sublime_plugin.EventListener):
    def on_hover(self, view, point, hover_zone):
        if settings.get("IntrinsicHoverEnabled", True) is False:
            return
        if not view:
            return
        try:
            if view.syntax().name != "PdxShader":
                return
        except AttributeError:
            return

        scopesStr = view.scope_name(point)
        scopeList = scopesStr.split(" ")
        for scope in scopeList:
            if scope == "keyword.function.intrinsic.hlsl":
                posWord = view.word(point)
                intrinsicWord = view.substr(posWord)
                if intrinsicWord in GameData.IntrinsicList:
                    url, desc = GameData.IntrinsicList[intrinsicWord]
                    hoverBody = """
                        <body id=show-intrinsic>
                            <style>
                                %s
                            </style>
                            <p>%s</p>
                            <br>
                            <a href="%s">MSDN Link</a>
                        </body>
                    """ % (
                        css.default,
                        desc,
                        url,
                    )

                    view.show_popup(
                        hoverBody,
                        flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                        location=point,
                        max_width=1024,
                        on_navigate=lambda x: OpenMSDNLink(x),
                    )
                    return


# ----------------------------------
# -           Hover Docs           -
# ----------------------------------


def show_hover_docs(view, point, scope, collection):
    style = settings.get("DocsPopupStyle")
    if style == "dark":
        style = css.dark
    elif style == "none":
        style = css.default
    elif style == "dynamic":
        if scope == "keyword.effect":
            style = css.effect
        elif scope == "string.trigger":
            style = css.trigger
        elif scope == "storage.type.scope":
            style = css.scope
    item = view.substr(view.word(point))
    if item in collection:
        desc = collection[item]
        hoverBody = """
            <body id="vic-body">
                <style>%s</style>
                <p>%s</p>
            </body>
        """ % (
            style,
            desc,
        )

        view.show_popup(
            hoverBody,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=1024,
        )
        return


def show_gui_docs_popup(view, point, item):
    data = GameData.GuiContent[item]
    color = data[0]
    desc = data[1]
    example = data[2]
    if example:
        example = f'<div class="box-for-codebox"><div class="codebox"><code>{example}</code></div></div>'
    if item in example:
        if color == "green":
            example = example.replace(item, f'<code class="green-text">{item}</code>')
        if color == "red":
            example = example.replace(item, f'<code class="red-text">{item}</code>')
        if color == "yellow":
            example = example.replace(item, f'<code class="yellow-text">{item}</code>')
        if color == "blue":
            example = example.replace(item, f'<code class="blue-text">{item}</code>')
        if color == "purple":
            example = example.replace(item, f'<code class="purple-text">{item}</code>')
        if color == "orange":
            example = example.replace(item, f'<code class="orange-text">{item}</code>')

    if item == "template" or item == "using":
        template_example = f'<div class="box-for-codebox"><div class="codebox code">template example_name {{<br>&nbsp;&nbsp;&nbsp;&nbsp;size = {{ 50 50 }}<br>}}<br></div></div>'
        template_example = template_example.replace(
            "template", f'<code class="purple-text">template</code>'
        )
        template_example_text = (
            '<p class="code-header">Example template definition:</p>'
        )
        template_example_text2 = (
            '<br><br><br><p class="code-header">Example template usage:</p>'
        )
        example = example.replace("using", f'<code class="green-text">using</code>')
        example = (
            template_example_text + template_example + template_example_text2 + example
        )

    if item == "block" or item == "blockoverride":
        block_example = f'<div class="box-for-codebox"><div class="codebox code">block "example_name" {{<br>&nbsp;&nbsp;&nbsp;&nbsp;visible = no<br>}}<br></div></div>'
        block_example = block_example.replace(
            "block", f'<code class="red-text">block</code>'
        )
        block_example_text = '<p class="code-header">Example block definition:</p>'
        block_example_text2 = (
            '<br><br><br><p class="code-header">Example blockoverride:</p>'
        )
        example = f'<div class="box-for-codebox"><div class="codebox code">blockoverride "example_name" {{<br>&nbsp;&nbsp;&nbsp;&nbsp;visible = yes<br>}}<br></div></div>'
        example = example.replace(
            "blockoverride", f'<code class="red-text">blockoverride</code>'
        )
        example = block_example_text + block_example + block_example_text2 + example

    if item == "type" or item == "types":
        example = f'<div class="box-for-codebox"><div class="codebox code">types My_Types<br>{{<br>&nbsp;&nbsp;&nbsp;&nbsp;type widget_with_size = widget {{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;size = {{ 50 50 }}<br>&nbsp;&nbsp;&nbsp;&nbsp;}}<br>}}<br></div></div>'
        example = example.replace("types", f'<code class="purple-text">types</code>')
        example = example.replace("type", f'<code class="purple-text">type</code>')
        type_example_text = '<p class="code-header">Example type definition:</p>'
        example = type_example_text + example

    hoverBody = """
        <body id="vic-body">
            <style>%s</style>
            <p class=\"codedesc\">%s</p>
            %s
        </body>
    """ % (
        css.default,
        desc,
        example,
    )

    view.show_popup(
        hoverBody,
        flags=(
            sublime.HIDE_ON_MOUSE_MOVE_AWAY
            | sublime.COOPERATE_WITH_AUTO_COMPLETE
            | sublime.HIDE_ON_CHARACTER_EVENT
        ),
        location=point,
        max_width=1024,
    )


class ScriptHoverListener(sublime_plugin.EventListener):
    def on_hover(self, view, point, hover_zone):
        if not view:
            return

        try:
            if view.syntax().name not in (
                "Victoria Script",
                "PdxPython",
                "Victoria Gui",
            ):
                return
        except AttributeError:
            return

        if view.match_selector(point, "comment.line"):
            return

        if view.syntax().name == "Victoria Gui":
            sublime.set_timeout_async(lambda: self.do_gui_hover_async(view, point), 0)
            item = view.substr(view.word(point))
            if (
                settings.get("GuiDocsHoverEnabled") is True
                and item in GameData.GuiContent
            ):
                sublime.set_timeout_async(
                    lambda: show_gui_docs_popup(view, point, item), 0
                )

        if (
            view.syntax().name == "Victoria Script"
            or view.syntax().name == "PdxPython"
            and not settings.get("EnableVictoriaScriptingFeatures")
        ):
            if settings.get("DocsHoverEnabled") is True:
                if view.match_selector(point, "keyword.effect"):
                    show_hover_docs(view, point, "keyword.effect", GameData.EffectsList)

                if view.match_selector(point, "string.trigger"):
                    GameData.TriggersList.update(GameData.CustomTriggersList)
                    show_hover_docs(
                        view, point, "string.trigger", GameData.TriggersList
                    )

                if view.match_selector(point, "storage.type.scope"):
                    GameData.ScopesList.update(GameData.CustomScopesList)
                    show_hover_docs(
                        view, point, "storage.type.scope", GameData.ScopesList
                    )

                # Do everything that requires fetching GameObjects in non-blocking thread
                sublime.set_timeout_async(lambda: self.do_hover_async(view, point), 0)

            # Event Videos
            if settings.get("BinkVideoHover") is True:
                posLine = view.line(point)
                posa = posLine.a + 1
                posb = posLine.b - 1
                video_raw_start = view.find("video = ", posLine.a)
                word_position_b = posLine.b - 6
                video_region = sublime.Region(video_raw_start.b, posb)
                video_file = (
                    view.substr(video_region)
                    .replace('"', "")
                    .replace("video = ", "")
                    .replace(" ", "")
                    .replace("\t", "")
                )
                global video_point, video_file_path
                if video_file in GameData.EventVideos:
                    video_file_path = v3_files_path + "/" + video_file
                    if not os.path.exists(video_file_path):
                        # Check mod paths if it's not vanilla
                        for mod in v3_mod_files:
                            mod_path = mod + "/" + video_file
                            if os.path.exists(mod_path):
                                video_file_path = mod_path
                    video_name = view.substr(view.word(word_position_b))
                    video_point = point
                    if video_region.__contains__(point):
                        self.show_video_hover_popup(view, point, video_name)
                else:
                    video_point = None

            # Event Sound
            if settings.get("EventSoundPopup") is True:
                posLine = view.line(point)
                if "event:/SFX/Events" in view.substr(posLine):
                    sound_raw_start = view.find("event:", posLine.a)
                    global sound_region
                    sound_region = sublime.Region(sound_raw_start.a, posLine.b - 1)
                    sound_string = view.substr(sound_region).replace('"', "")
                    if (
                        sound_string in GameData.EventSoundsList
                        and sound_region.__contains__(point)
                    ):
                        self.show_event_sound_hover_popup(view, point)
                else:
                    global show_sound_menu
                    show_sound_menu = False

        # Texture popups can happen for both script and gui files
        if (
            view.syntax().name == "Victoria Script"
            or view.syntax().name == "Victoria Gui"
            or view.syntax().name == "PdxPython"
        ):
            if settings.get("TextureOpenPopup") is True:
                posLine = view.line(point)
                linestr = view.substr(posLine)
                if ".dds" in linestr or ".tga" in linestr:
                    if "common/coat_of_arms" in view.file_name():
                        if "pattern" in linestr:
                            raw_start = view.find("pattern", posLine.a)
                            raw_end = (
                                view.find(".dds", posLine.a)
                                if ".dds" in linestr
                                else view.find(".tga", posLine.a)
                            )
                            raw_region = sublime.Region(raw_start.a + 10, raw_end.b)
                            raw_path = view.substr(raw_region).replace('"', "")
                            full_texture_path = (
                                v3_files_path + "/gfx/coat_of_arms/patterns/" + raw_path
                            )
                            full_texture_path = full_texture_path
                            if raw_region.__contains__(point) and os.path.exists(
                                full_texture_path
                            ):
                                texture_name = view.substr(view.word(raw_end.a - 1))
                                self.show_texture_hover_popup(
                                    view, point, texture_name, full_texture_path
                                )
                                return
                        if "texture" in linestr:
                            raw_start = view.find("texture", posLine.a)
                            raw_end = (
                                view.find(".dds", posLine.a)
                                if ".dds" in linestr
                                else view.find(".tga", posLine.a)
                            )
                            raw_region = sublime.Region(raw_start.a + 10, raw_end.b)
                            raw_path = view.substr(raw_region).replace('"', "")
                            full_texture_path = (
                                v3_files_path
                                + "/gfx/coat_of_arms/colored_emblems/"
                                + raw_path
                            )
                            if not os.path.exists(full_texture_path):
                                full_texture_path = (
                                    v3_files_path
                                    + "/gfx/coat_of_arms/textured_emblems/"
                                    + raw_path
                                )
                            if raw_region.__contains__(point) and os.path.exists(
                                full_texture_path
                            ):
                                texture_name = view.substr(view.word(raw_end.a - 1))
                                self.show_texture_hover_popup(
                                    view, point, texture_name, full_texture_path
                                )
                                return

                    texture_raw_start = view.find("gfx", posLine.a)
                    texture_raw_end = (
                        view.find(".dds", posLine.a)
                        if ".dds" in linestr
                        else view.find(".tga", posLine.a)
                    )
                    texture_raw_region = sublime.Region(
                        texture_raw_start.a, texture_raw_end.b
                    )
                    texture_raw_path = view.substr(texture_raw_region)
                    if view.syntax().name == "Victoria Gui":
                        full_texture_path = gui_files_path + "/" + texture_raw_path
                    else:
                        full_texture_path = v3_files_path + "/" + texture_raw_path
                    if not os.path.exists(full_texture_path):
                        # Check mod paths if it's not vanilla
                        for mod in [m for m in v3_mod_files if os.path.exists(m)]:
                            if mod.endswith("mod"):
                                # if it is the path to the mod directory, get all directories in it
                                for directory in [
                                    f.path for f in os.scandir(mod) if f.is_dir()
                                ]:
                                    mod_path = directory + "/" + texture_raw_path
                                    if os.path.exists(mod_path):
                                        full_texture_path = mod_path
                            else:
                                mod_path = mod + "/" + texture_raw_path
                                if os.path.exists(mod_path):
                                    full_texture_path = mod_path

                        if view.syntax().name == "Victoria Gui" and not os.path.exists(
                            mod_path
                        ):
                            for mod in [m for m in gui_mod_files if os.path.exists(m)]:
                                if mod.endswith("mod"):
                                    # if it is the path to the mod directory, get all directories in it
                                    for directory in [
                                        f.path for f in os.scandir(mod) if f.is_dir()
                                    ]:
                                        mod_path = directory + "/" + texture_raw_path
                                        if os.path.exists(mod_path):
                                            full_texture_path = mod_path
                                else:
                                    mod_path = mod + "/" + texture_raw_path
                                    if os.path.exists(mod_path):
                                        full_texture_path = mod_path

                    # The path exists and the point in the view is inside of the path
                    if texture_raw_region.__contains__(point) and os.path.exists(
                        full_texture_path
                    ):
                        texture_name = view.substr(view.word(texture_raw_end.a - 1))
                        self.show_texture_hover_popup(
                            view, point, texture_name, full_texture_path
                        )

    def do_gui_hover_async(self, view, point):
        word = view.substr(view.word(point))

        if view.match_selector(point, "comment.line"):
            return

        if game_objects["gui_templates"].contains(word):
            self.show_gui_popup(
                view,
                point,
                word,
                game_objects["gui_templates"].access(word),
                "Gui Template",
            )

        if game_objects["gui_types"].contains(word):
            self.show_gui_popup(
                view, point, word, game_objects["gui_types"].access(word), "Gui Type"
            )

    def do_hover_async(self, view, point):
        word_region = view.word(point)
        word = view.substr(word_region)
        fname = view.file_name()
        current_line_num = view.rowcol(point)[0] + 1

        if view.match_selector(point, "comment.line"):
            return

        if view.match_selector(point, "entity.name.function.scope.declaration"):
            self.show_popup_default(
                view,
                point,
                word,
                PdxScriptObject(word, fname, current_line_num),
                "Scope Declaration",
            )

        if view.match_selector(point, "entity.name.function.var.declaration"):
            self.show_popup_default(
                view,
                point,
                word,
                PdxScriptObject(word, fname, current_line_num),
                "Variable Declaration",
            )

        if (
            view.match_selector(point, "variable.parameter.scope.usage")
            or view.match_selector(point, "variable.parameter.remove.var")
            or view.match_selector(point, "variable.parameter.trigger.usage")
            or view.match_selector(point, "variable.parameter.variable.usage")
        ):
            if view.match_selector(point, "variable.parameter.scope.usage"):
                self.show_popup_default(
                    view,
                    point,
                    word,
                    PdxScriptObject(word, fname, current_line_num),
                    "Saved Scope",
                )
            else:
                self.show_popup_default(
                    view,
                    point,
                    word,
                    PdxScriptObject(word, fname, current_line_num),
                    "Saved Variable",
                )

        hover_objects = [
            ("ai_strats", "Ai Strategies"),
            ("bgs", "Building Group"),
            ("buildings", "Building"),
            ("char_traits", "Character Trait"),
            ("cultures", "Culture"),
            ("decrees", "Decree"),
            ("diplo_actions", "Diplomatic Action"),
            ("diplo_plays", "Diplomatic Play"),
            ("game_rules", "Game Rule"),
            ("goods", "Trade Good"),
            ("gov_types", "Government Type"),
            ("ideologies", "Ideology"),
            ("institutions", "Institution"),
            ("ig_traits", "Group Traits"),
            ("igs", "Interest Group"),
            ("jes", "Journal Entry"),
            ("law_groups", "Law Group"),
            ("laws", "Law"),
            ("mods", "Modifier"),
            ("parties", "Party"),
            ("pop_needs", "Pop Need"),
            ("pop_types", "Pop Type"),
            ("pm_groups", "Method Group"),
            ("pms", "Production Method"),
            ("religions", "Religion"),
            ("script_values", "Script Value"),
            ("scripted_effects", "Scripted Effect"),
            ("scripted_modifiers", "Scripted Modifer"),
            ("scripted_triggers", "Scripted Trigger"),
            ("state_traits", "State Trait"),
            ("strategic_regions", "Strategic Region"),
            ("subject_types", "Subject Types"),
            ("technologies", "Technology"),
            ("terrains", "Terrain"),
            ("state_regions", "State Region"),
            ("countries", "Country"),
            ("country_ranks", "Country Rank"),
            ("country_types", "Country Type"),
            ("culture_graphics", "Culture Graphic"),
            ("named_colors", "Named Color"),
            ("battle_conditions", "Battle Condition"),
            ("commander_ranks", "Commander Rank"),
            ("proposal_types", "Proposal Type"),
            ("discrimination_traits", "Discrimination Trait"),
        ]

        # Iterate over the list and call show_popup_default for each game object
        for hover_object, name in hover_objects:
            if game_objects[hover_object].contains(word):
                self.show_popup_default(
                    view, point, word, game_objects[hover_object].access(word), name
                )

    def show_gui_popup(self, view, point, word, PdxObject, header):
        word_line_num = view.rowcol(point)[0] + 1
        word_file = view.file_name().replace("\\", "/").rstrip("/").rpartition("/")[2]
        definition = ""

        if word_line_num != PdxObject.line:
            definition = f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            goto_args = {"path": PdxObject.path, "line": PdxObject.line}
            goto_url = sublime.command_url("goto_script_object_definition", goto_args)
            definition += (
                """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;"""
                % (
                    goto_url,
                    PdxObject.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    PdxObject.line,
                    PdxObject.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    PdxObject.line,
                )
            )
            goto_right_args = {"path": PdxObject.path, "line": PdxObject.line}
            goto_right_url = sublime.command_url(
                "goto_script_object_definition_right", goto_right_args
            )
            definition += (
                """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                % (goto_right_url)
            )

        references = []
        ref = ""
        for win in sublime.windows():
            for i in [v for v in win.views() if v and v.file_name()]:
                if i.file_name().endswith(".gui"):
                    view_region = sublime.Region(0, i.size())
                    view_str = i.substr(view_region)
                    for j, line in enumerate(view_str.splitlines()):
                        definition_found = False
                        if PdxObject.key in line:
                            filename = (
                                i.file_name()
                                .replace("\\", "/")
                                .rstrip("/")
                                .rpartition("/")[2]
                            )
                            line_num = j + 1
                            if word_line_num == line_num and word_file == filename:
                                # Don't do current word
                                continue
                            elif (
                                line_num == PdxObject.line
                                and i.file_name() == PdxObject.path
                            ):
                                # Don't do definition
                                continue
                            if not definition_found:
                                references.append(f"{i.file_name()}|{line_num}")

        if references:
            ref = f'<p><b>References to&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            for j, i in enumerate(references):
                if j > 10:
                    break
                fname = i.split("|")[0]
                shortname = fname.replace("\\", "/").rstrip("/").rpartition("/")[2]
                line = i.split("|")[1]
                goto_args = {"path": fname, "line": line}
                goto_url = sublime.command_url(
                    "goto_script_object_definition", goto_args
                )
                ref += (
                    """<a href="%s" title="Open %s and goto line %s">%s:%s</a>&nbsp;"""
                    % (
                        goto_url,
                        shortname,
                        line,
                        shortname,
                        line,
                    )
                )
                goto_right_args = {"path": fname, "line": line}
                goto_right_url = sublime.command_url(
                    "goto_script_object_definition_right", goto_right_args
                )
                ref += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )

        link = definition + ref
        if link:
            hoverBody = """
                <body id="vic-body">
                    <style>%s</style>
                    <h1>%s</h1>
                    %s
                </body>
            """ % (
                css.default,
                header,
                link,
            )

            view.show_popup(
                hoverBody,
                flags=(
                    sublime.HIDE_ON_MOUSE_MOVE_AWAY
                    | sublime.COOPERATE_WITH_AUTO_COMPLETE
                    | sublime.HIDE_ON_CHARACTER_EVENT
                ),
                location=point,
                max_width=1024,
            )

    def get_definitions_for_popup(self, view, point, PdxObject, header, def_value=""):
        word_line_num = view.rowcol(point)[0] + 1
        word_file = view.file_name().replace("\\", "/").rstrip("/").rpartition("/")[2]
        definition = ""
        definitions = []
        if header == "Saved Scope" or header == "Saved Variable":
            for win in sublime.windows():
                for i in [v for v in win.views() if v and v.file_name()]:
                    if i.file_name().endswith(".txt") or i.file_name().endswith(".py"):
                        variables = [
                            x
                            for x in i.find_by_selector(
                                "entity.name.function.var.declaration"
                            )
                            if i.substr(x) == PdxObject.key
                        ]
                        variables.extend(
                            [
                                x
                                for x in i.find_by_selector(
                                    "entity.name.function.scope.declaration"
                                )
                                if i.substr(x) == PdxObject.key
                            ]
                        )
                        for r in variables:
                            line = i.rowcol(r.a)[0] + 1
                            path = i.file_name()
                            if line == word_line_num and path == PdxObject.path:
                                continue
                            else:
                                definitions.append(
                                    PdxScriptObject(PdxObject.key, path, line)
                                )

            if len(definitions) == 1:
                if def_value:
                    definition = f"<br>{def_value}<br><br>"
                    definition += f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                else:
                    definition = f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            elif len(definitions) > 1:
                if def_value:
                    definition = f"<br>{def_value}<br><br>"
                    definition += f'<p><b>Definitions of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                else:
                    definition = f'<p><b>Definitions of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            for obj in definitions:
                goto_args = {"path": obj.path, "line": obj.line}
                goto_url = sublime.command_url(
                    "goto_script_object_definition", goto_args
                )
                definition += (
                    """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;"""
                    % (
                        goto_url,
                        obj.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                        obj.line,
                        obj.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                        obj.line,
                    )
                )
                goto_right_args = {"path": obj.path, "line": obj.line}
                goto_right_url = sublime.command_url(
                    "goto_script_object_definition_right", goto_right_args
                )
                definition += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )
        else:
            if word_line_num != PdxObject.line and view.file_name() != PdxObject.path:
                if def_value:
                    definition = f"<br>{def_value}<br><br>"
                    definition += f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                else:
                    definition = f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                goto_args = {"path": PdxObject.path, "line": PdxObject.line}
                goto_url = sublime.command_url(
                    "goto_script_object_definition", goto_args
                )
                definition += (
                    """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;"""
                    % (
                        goto_url,
                        PdxObject.path.replace("\\", "/")
                        .rstrip("/")
                        .rpartition("/")[2],
                        PdxObject.line,
                        PdxObject.path.replace("\\", "/")
                        .rstrip("/")
                        .rpartition("/")[2],
                        PdxObject.line,
                    )
                )
                goto_right_args = {"path": PdxObject.path, "line": PdxObject.line}
                goto_right_url = sublime.command_url(
                    "goto_script_object_definition_right", goto_right_args
                )
                definition += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )

        return definition

    def get_references_for_popup(self, view, point, PdxObject, header):
        word_line_num = view.rowcol(point)[0] + 1
        word_file = view.file_name().replace("\\", "/").rstrip("/").rpartition("/")[2]
        references = []
        ref = ""
        for win in sublime.windows():
            for i in [v for v in win.views() if v and v.file_name()]:
                if i.file_name().endswith(".txt"):
                    view_region = sublime.Region(0, i.size())
                    view_str = i.substr(view_region)
                    for j, line in enumerate(view_str.splitlines()):
                        if re.search(r"\b" + re.escape(PdxObject.key) + r"\b", line):
                            filename = (
                                i.file_name()
                                .replace("\\", "/")
                                .rstrip("/")
                                .rpartition("/")[2]
                            )
                            line_num = j + 1
                            if word_line_num == line_num and word_file == filename:
                                # Don't do current word
                                continue
                            elif (
                                line_num == PdxObject.line
                                and i.file_name() == PdxObject.path
                            ):
                                # Don't do definition
                                continue
                            else:
                                references.append(f"{i.file_name()}|{line_num}")
        if references:
            ref = f'<p><b>References to&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            for i in references:
                fname = i.split("|")[0]
                shortname = fname.replace("\\", "/").rstrip("/").rpartition("/")[2]
                line = i.split("|")[1]
                goto_args = {"path": fname, "line": line}
                goto_url = sublime.command_url(
                    "goto_script_object_definition", goto_args
                )
                ref += (
                    """<a href="%s" title="Open %s and goto line %s">%s:%s</a>&nbsp;"""
                    % (
                        goto_url,
                        shortname,
                        line,
                        shortname,
                        line,
                    )
                )
                goto_right_args = {"path": fname, "line": line}
                goto_right_url = sublime.command_url(
                    "goto_script_object_definition_right", goto_right_args
                )
                ref += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )

        return ref

    def show_popup_default(self, view, point, word, PdxObject, header):
        if view.file_name() is None:
            return

        link = self.get_definitions_for_popup(
            view, point, PdxObject, header
        ) + self.get_references_for_popup(view, point, PdxObject, header)
        if link:
            hoverBody = """
                <body id="vic-body">
                    <style>%s</style>
                    <h1>%s</h1>
                    %s
                </body>
            """ % (
                css.default,
                header,
                link,
            )

            view.show_popup(
                hoverBody,
                flags=(
                    sublime.HIDE_ON_MOUSE_MOVE_AWAY
                    | sublime.COOPERATE_WITH_AUTO_COMPLETE
                    | sublime.HIDE_ON_CHARACTER_EVENT
                ),
                location=point,
                max_width=1024,
            )

    def show_popup_named_color(self, view, point, word, PdxObject, header):
        if view.file_name() is None:
            return

        object_color = PdxObject.color
        css_color = PdxObject.rgb_color
        r = css_color[0]
        g = css_color[1]
        b = css_color[2]
        icon_color = f"rgb({r},{g},{b})"
        color = f'<a class="icon"style="color:{icon_color}">■</a>\t\t\t<code>{object_color}</code>'

        link = self.get_definitions_for_popup(view, point, PdxObject, header, color)
        if link:
            hoverBody = """
                <body id="vic-body">
                    <style>%s</style>
                    <h1>%s</h1>
                    %s
                </body>
            """ % (
                css.default,
                header,
                link,
            )

            view.show_popup(
                hoverBody,
                flags=(
                    sublime.HIDE_ON_MOUSE_MOVE_AWAY
                    | sublime.COOPERATE_WITH_AUTO_COMPLETE
                    | sublime.HIDE_ON_CHARACTER_EVENT
                ),
                location=point,
                max_width=1024,
            )

    def show_texture_hover_popup(self, view, point, texture_name, full_texture_path):
        args = {"path": full_texture_path}
        open_texture_url = sublime.command_url("open_victoria_texture ", args)
        folder_args = {"path": full_texture_path, "folder": True}
        open_folder_url = sublime.command_url("open_victoria_texture ", folder_args)
        in_sublime_args = {"path": full_texture_path, "mode": "in_sublime"}
        inline_args = {"path": full_texture_path, "point": point}
        open_in_sublime_url = sublime.command_url(
            "open_victoria_texture ", in_sublime_args
        )
        open_inline_url = sublime.command_url("v3_show_texture ", inline_args)
        hoverBody = """
            <body id=\"vic-body\">
                <style>%s</style>
                <h1>Open Texture</h1>
                <div></div>
                <a href="%s" title="Open folder containing the texture.">Open Folder</a>
                <br>
                <a href="%s" title="Open %s in the default program">Open in default program</a>
                <br>
                <a href="%s" title="Open %s in sublime">Open in sublime</a>
                <br>
                <a href="%s" title="Show %s at current selection">Show Inline</a>
            </body>
        """ % (
            css.default,
            open_folder_url,
            open_texture_url,
            texture_name,
            open_in_sublime_url,
            texture_name,
            open_inline_url,
            texture_name,
        )

        view.show_popup(
            hoverBody,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=802,
        )

    def show_event_sound_hover_popup(self, view, point):
        global show_sound_menu
        show_sound_menu = True
        browse_url = sublime.command_url("browse_event_sound")
        hoverBody = """
            <body id=\"vic-body\">
                <style>%s</style>
                <h1>Event Sound</h1>
                <div></div>
                <a href="%s" title="Replace current event sound with a new one...">Browse event audio</a>
            </body>
        """ % (
            css.default,
            browse_url,
        )

        view.show_popup(
            hoverBody,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=802,
        )

    def show_video_hover_popup(self, view, point, word):
        args = {"play": True}
        browse_and_play_url = sublime.command_url("browse_bink_videos", args)
        hoverBody = """
            <body id=\"vic-body\">
                <style>%s</style>
                <h1>Bink Video</h1>
                <span>•</span><a href="subl:play_bink_video" title="Note: Rad Game Tools Bink video player required.">Play %s.bk2</a>
                <br><div></div>
                <span>•</span><a href="subl:browse_bink_videos" title="Browse videos for a video to replace current video path.">Browse and Replace</a>&nbsp;
                <br>
                <span>•</span><a href="%s" title="Browse videos for a video to replace current video path and then play the new video.">Browse, Replace, and Play</a>&nbsp;
            </body>
        """ % (
            css.default,
            word,
            browse_and_play_url,
        )

        view.show_popup(
            hoverBody,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=802,
        )


# Global so I don't have to deal with passing through the hrefs, should probably just pass them as args.
video_file_path = False
video_point = None
edit_obj = None  # Used to pass edit object to on_done
show_sound_menu = False
sound_region = False


class GotoScriptObjectDefinitionCommand(sublime_plugin.WindowCommand):
    def run(self, path, line):
        if os.path.exists(path):
            file_path = "{}:{}:{}".format(path, line, 0)
            self.open_location(self.window, file_path)

    def open_location(self, window, location):
        flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP
        view = window.open_file(location, flags)


class GotoScriptObjectDefinitionRightCommand(sublime_plugin.WindowCommand):
    def run(self, path, line):
        if os.path.exists(path):
            file_path = "{}:{}:{}".format(path, line, 0)
            self.open_location(
                self.window, file_path, side_by_side=True, clear_to_right=True
            )

    def open_location(
        self, window, location, side_by_side=False, replace=False, clear_to_right=False
    ):
        flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP

        if side_by_side:
            flags |= sublime.ADD_TO_SELECTION | sublime.SEMI_TRANSIENT
            if clear_to_right:
                flags |= sublime.CLEAR_TO_RIGHT

        elif replace:
            flags |= sublime.REPLACE_MRU | sublime.SEMI_TRANSIENT
        view = window.open_file(location, flags)


class OpenVictoriaTextureCommand(sublime_plugin.WindowCommand):
    def run(self, path, folder=False, mode="default_program"):
        if folder:
            path = path.replace("\\", "/")
            end = path.rfind("/")
            path = path[0:end:]
            OpenVictoriaTextureCommand.open_path(path)
        else:
            if mode == "default_program":
                OpenVictoriaTextureCommand.open_path(path)
            elif mode == "in_sublime":
                simple_path = (
                    path.replace("\\", "/")
                    .rstrip("/")
                    .rpartition("/")[2]
                    .replace(".dds", ".png")
                    if ".dds" in path
                    else path.replace("\\", "/")
                    .rstrip("/")
                    .rpartition("/")[2]
                    .replace(".tga", ".png")
                )
                output_file = (
                    sublime.packages_path()
                    + "/Victoria3Tools/Convert DDS/cache/"
                    + simple_path
                )
                exe_path = (
                    sublime.packages_path()
                    + "/Victoria3Tools/Convert DDS/src/ConvertDDS.exe"
                )

                if not os.path.exists(output_file):
                    # Run dds to png converter
                    self.window.run_command(
                        "quiet_execute", {"cmd": [exe_path, path, output_file]}
                    )
                    sublime.active_window().open_file(output_file)
                else:
                    # File is already in cache, don't need to convert
                    sublime.active_window().open_file(output_file)

    @staticmethod
    def open_path(path):
        system = sys.platform
        if system == "Darwin":  # macOS
            subprocess.call(("open", path))
        elif system == "Windows" or system == "win32" or system == "win":  # Windows
            os.startfile(path)
        else:  # Linux and other Unix-like systems
            subprocess.call(("xdg-open", path))


class QuietExecuteCommand(sublime_plugin.WindowCommand):
    """
    Simple version of Default.exec.py that only runs the process and shows no panel or messages
    """

    def __init__(self, window):
        super().__init__(window)
        self.proc = None

    def run(
        self,
        cmd=None,
        shell_cmd=None,
        working_dir="",
        encoding="utf-8",
        env={},
        **kwargs,
    ):
        self.encoding = encoding
        merged_env = env.copy()
        if self.window.active_view():
            user_env = self.window.active_view().settings().get("build_env")
            if user_env:
                merged_env.update(user_env)

        if working_dir != "":
            os.chdir(working_dir)

        try:
            # Run process
            self.proc = Default.exec.AsyncProcess(
                cmd, shell_cmd, merged_env, self, **kwargs
            )
            self.proc.start()
        except Exception:
            sublime.status_message("Build error")

    def on_data(self, proc, data):
        return

    def on_finished(self, proc):
        return


class V3ClearImageCacheCommand(sublime_plugin.WindowCommand):
    def run(self):
        dir_name = sublime.packages_path() + "/Victoria3Tools/Convert DDS/cache/"
        ld = os.listdir(dir_name)
        for item in ld:
            if item.endswith(".png"):
                os.remove(os.path.join(dir_name, item))
        sublime.status_message("Cleared Image Cache")


class V3TextureFileLoadEventListener(sublime_plugin.EventListener):
    def on_load_async(self, view):
        if not view:
            return None

        try:
            if (
                view.syntax().name != "Victoria Script"
                and view.syntax().name != "PdxPython"
                and view.syntax().name != "Victoria Gui"
            ):
                return None
        except AttributeError:
            return None

        if settings.get("ShowInlineTexturesOnLoad"):
            sublime.active_window().run_command("v3_show_all_textures")


class V3TextureEventListener(sublime_plugin.EventListener):
    def on_post_text_command(self, view, command_name, args):
        if command_name in ("left_delete", "insert"):
            if (
                view.file_name()
                and view.syntax().name == "Victoria Script"
                or view.syntax().name == "PdxPython"
                or view.syntax().name == "Victoria Gui"
            ):
                x = [v for v in views_with_shown_textures if v.id() == view.id()]
                if x:
                    x[0].update_line_count(view.rowcol(view.size())[0] + 1)


views_with_shown_textures = set()


class V3ViewTextures(sublime.View):
    def __init__(self, id):
        super(V3ViewTextures, self).__init__(id)
        self.textures = []
        self.line_count = self.rowcol(self.size())[0] + 1

    def update_line_count(self, new_count):
        diff = new_count - self.line_count
        self.line_count += diff
        to_update = []
        for i, tex in enumerate(self.textures):
            tex = tex.split("|")
            key = tex[0]
            line = int(tex[1])
            point = self.text_point(line, 1)
            if self.find(key, point):
                # Texture is still on the same line, dont need to update
                return
            else:
                current_selection_line = self.rowcol(self.sel()[0].a)[0] + 1
                if current_selection_line < line:
                    line += diff
                    out = key + "|" + str(line)
                    to_update.append((i, out))
        for i in to_update:
            index = i[0]
            replacement = i[1]
            views_with_shown_textures.discard(self)
            self.textures[index] = replacement
            views_with_shown_textures.add(self)


class ShowTextureBase:
    conversion_iterations = 0

    def show_texture(self, path, point):
        window = sublime.active_window()
        simple_path = (
            path.replace("\\", "/")
            .rstrip("/")
            .rpartition("/")[2]
            .replace(".dds", ".png")
            if ".dds" in path
            else path.replace("\\", "/")
            .rstrip("/")
            .rpartition("/")[2]
            .replace(".tga", ".png")
        )
        output_file = (
            sublime.packages_path() + "/Victoria3Tools/Convert DDS/cache/" + simple_path
        )
        exe_path = (
            sublime.packages_path() + "/Victoria3Tools/Convert DDS/src/ConvertDDS.exe"
        )
        if not os.path.exists(output_file):
            window.run_command("quiet_execute", {"cmd": [exe_path, path, output_file]})
            # Wait 100ms for conversion to finish
            sublime.set_timeout_async(
                lambda: self.toggle_async(
                    output_file, simple_path, point, window, path
                ),
                100,
            )
        else:
            self.toggle_async(output_file, simple_path, point, window, path)

    def toggle_async(self, output_file, simple_path, point, window, original_path):
        # Try to convert for 500ms
        if not os.path.exists(output_file) and self.conversion_iterations < 6:
            self.conversion_iterations += 1
            self.show_texture(original_path, point)
        elif os.path.exists(output_file):
            self.conversion_iterations = 0
            image = f"file://{output_file}"
            dimensions = self.get_png_dimensions(output_file)
            width = dimensions[0]
            height = dimensions[1]
            html = f'<img src="{image}" width="{width}" height="{height}">'
            view = window.active_view()
            if os.path.exists(output_file):
                self.toggle(simple_path, view, html, point)

    def toggle(self, key, view, html, point):
        pid = key + "|" + str(view.rowcol(point)[0] + 1)
        x = V3ViewTextures(view.id())
        views_with_shown_textures.add(x)
        x = [v for v in views_with_shown_textures if v.id() == view.id()]
        if not x:
            return
        current_view = x[0]
        if pid in current_view.textures:
            current_view.textures.remove(pid)
            view.erase_phantoms(key)
        else:
            current_view.textures.append(pid)
            line_region = view.line(point)
            # Find region of texture path declaration
            # Ex: [start]texture = "gfx/interface/icons/goods_icons/meat.dds"[end]
            start = view.find(
                r'[A-Za-z_][A-Za-z_0-9]*\s?=\s?"?/?(gfx)?', line_region.a
            ).a
            end = view.find('"|\n', start).a
            phantom_region = sublime.Region(start, end)
            view.add_phantom(key, phantom_region, html, sublime.LAYOUT_BELOW)

    def get_png_dimensions(self, path):
        height = 150
        width = 150
        file = open(path, "rb")
        try:
            head = file.read(31)
            size = len(head)
            if (
                size >= 24
                and head.startswith(b"\211PNG\r\n\032\n")
                and head[12:16] == b"IHDR"
            ):
                try:
                    width, height = struct.unpack(">LL", head[16:24])
                except struct.error:
                    pass
            elif size >= 16 and head.startswith(b"\211PNG\r\n\032\n"):
                try:
                    width, height = struct.unpack(">LL", head[8:16])
                except struct.error:
                    pass
        finally:
            file.close()

        # Scale down so image doens't take up entire viewport
        if width > 150 and height > 150:
            width /= 1.75
            height /= 1.75
        return int(width), int(height)


class V3ShowTextureCommand(sublime_plugin.ApplicationCommand, ShowTextureBase):
    def run(self, path, point):
        self.show_texture(path, point)


class V3ToggleAllTexturesCommand(sublime_plugin.ApplicationCommand):
    def __init__(self):
        self.shown = False

    def run(self):
        window = sublime.active_window()
        view = window.active_view()
        if not view:
            return None

        try:
            if (
                view.syntax().name != "Victoria Script"
                and view.syntax().name != "PdxPython"
                and view.syntax().name != "Victoria Gui"
            ):
                return None
        except AttributeError:
            return None

        if self.shown or len(views_with_shown_textures) > 0:
            self.shown = False
            window.run_command("v3_clear_all_textures")
        else:
            self.shown = True
            window.run_command("v3_show_all_textures")


class V3ClearAllTexturesCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        keys = []
        for view in views_with_shown_textures:
            for i in view.textures:
                tex = i.split("|")
                key = tex[0]
                keys.append(key)
        for view in sublime.active_window().views():
            for i in keys:
                view.erase_phantoms(i)
        views_with_shown_textures.clear()


class V3ShowAllTexturesCommand(sublime_plugin.WindowCommand, ShowTextureBase):
    def run(self):
        view = self.window.active_view()
        texture_list = [
            x
            for x in view.lines(sublime.Region(0, view.size()))
            if ".dds" in view.substr(x)
        ]
        for line, i in zip(texture_list, range(settings.get("MaxToggleTextures"))):
            texture_raw_start = view.find("gfx", line.a)
            texture_raw_end = view.find(".dds", line.a)
            texture_raw_region = sublime.Region(texture_raw_start.a, texture_raw_end.b)
            texture_raw_path = view.substr(texture_raw_region)
            full_texture_path = v3_files_path + "/" + texture_raw_path
            self.show_texture(full_texture_path, texture_raw_start.a)


class PlayBinkVideoCommand(sublime_plugin.WindowCommand):
    def run(self):
        global video_file_path
        if video_file_path:
            OpenVictoriaTextureCommand.open_path(video_file_path)


class BrowseEventSoundCommand(sublime_plugin.TextCommand):
    def input_description(self):
        return "Select Sound"

    def input(self, args):
        if "sound" not in args:
            return SoundInputHandler()

    def run(self, edit, sound):
        global sound_region
        sound = "event:/SFX/Events/" + sound
        self.view.replace(edit, sound_region, sound)

    def is_visible(self):
        # Won't show in the command pallete normally but will still be avilable for commands
        global show_sound_menu
        if show_sound_menu:
            return True
        else:
            return False


class BrowseBinkVideosCommand(sublime_plugin.TextCommand):
    def run(self, edit, video, play=False):
        global edit_obj
        edit_obj = edit
        if video:
            if play:
                self.on_done(video, play=True)
            else:
                self.on_done(video)

    def input_description(self):
        return "Select Video"

    def input(self, args):
        if "video" not in args:
            return VideoInputHandler()

    def on_done(self, video, play=False):
        global video_point, edit_obj
        video = "gfx/event_pictures/" + video
        video_path = v3_files_path + "/" + video
        if not os.path.exists(video_path):
            # Check mod paths if it's not vanilla
            for mod in v3_mod_files:
                mod_path = mod + "/" + video
                if os.path.exists(mod_path):
                    video_path = mod_path

        # If opened with command pallete it will just show the video, not try to replace text.
        if video_point is None:
            OpenVictoriaTextureCommand.open_path(video_path)
            return
        view = self.view
        posLine = view.line(video_point)
        posa = posLine.a + 1
        posb = posLine.b - 1
        video_file = (
            view.substr(sublime.Region(posa, posb))
            .replace('"', "")
            .replace("video = ", "")
            .replace(" ", "")
            .replace("\t", "")
        )
        actual_video_region = view.find(video_file, posa)
        view.replace(edit_obj, actual_video_region, video)
        video_point = None
        edit_obj = None
        if play:
            OpenVictoriaTextureCommand.open_path(video_path)


class VideoInputHandler(sublime_plugin.ListInputHandler):
    def name(self):
        return "video"

    def list_items(self):
        keys = []
        for x in GameData.EventVideos:
            keys.append(x.replace("gfx/event_pictures/", ""))
        return keys


class SoundInputHandler(sublime_plugin.ListInputHandler):
    def name(self):
        return "sound"

    def list_items(self):
        keys = []
        for x in GameData.EventSoundsList:
            keys.append(x.replace("event:/SFX/Events/", ""))
        return sorted(keys)


class V3ReloadPluginCommand(sublime_plugin.WindowCommand):
    def run(self):
        plugin_loaded()


# class RunVic3TigerCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         print("running tiger...")
#         mod_path = ""
#         exe_path = (
#             sublime.packages_path()
#             + "/Victoria3Tools/Vic3 Tiger/vic3-tiger-linux/vic3-tiger"
#         )
#         sublime.set_timeout_async(lambda: self.run_tiger(exe_path, mod_path), 0)

#     def run_tiger(self, exe_path, path):
#         result = subprocess.run(
#             [exe_path, path, "--json"], capture_output=True, text=True
#         )
#         output = result.stdout
#         output = "[" + output.split("[", 1)[1]

#         # Load the JSON data
#         data = json.loads(output)

#         # Filter the objects with a severity of "error"
#         error_objects = [obj for obj in data if obj["severity"] == "error"]

#         # Print the error objects
#         for obj in error_objects:
#             key = obj["key"]
#             locations = obj["locations"][0]
#             path = locations["fullpath"]
#             linenum = locations["linenr"]
#             line = locations["line"]
#             length = locations["length"]
#             column = locations["column"]
#             message = obj["message"]
#             if os.path.exists(path):
#                 location = "{}:{}:{}".format(path, linenum, column)
#                 flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP
#                 view = self.window.open_file(location, flags)

#                 point = view.text_point(linenum, column) - len(line) - 2
#                 error_region = sublime.Region(
#                     point,
#                     point + length,
#                 )
#                 view.add_regions(
#                     view.substr(error_region),
#                     [error_region],
#                     "invalid",
#                     "",
#                     sublime.PERSISTENT
#                     | sublime.DRAW_NO_OUTLINE
#                     | sublime.DRAW_SQUIGGLY_UNDERLINE
#                     | sublime.DRAW_NO_FILL,
#                 )

# break

# print(f"Error: {key}   Path: {path}    Line: {line}\n\t{message}")

# output_path = (
#     sublime.packages_path() + "/Victoria3Tools/Vic3 Tiger/tiger_output.json"
# )
# with open(output_path, "w") as file:
#     file.write(output)
