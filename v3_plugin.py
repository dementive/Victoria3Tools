import sublime
import sublime_plugin
import os
import sys
import subprocess
import re
import threading
import time
import struct
import Default.exec
from colorsys import hsv_to_rgb
from webbrowser import open as openwebsite
from collections import deque
from .jomini import GameObjectBase, PdxScriptObjectType, PdxScriptObject
from .jomini import dict_to_game_object as make_object
from .Utilities.game_data import GameData
from .Utilities.css import CSS
from .object_cache import GameObjectCache
from .mod_cache import remake_cache


# ----------------------------------
# -          Plugin Setup          -
# ----------------------------------
settings = None
v3_files_path = ""
v3_mod_files = []
gui_files_path = ""
gui_mod_files = []
css = CSS()
GameData = GameData()


# Gui Class implementations
class GuiType(GameObjectBase):
    def __init__(self):
        super().__init__(gui_mod_files, settings.get("GuiBaseGamePath"))
        self.get_data("gui")

    def get_pdx_object_list(self, path: str) -> PdxScriptObjectType:
        obj_list = list()
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in [f for f in filenames if f.endswith(".gui")]:
                if filename in self.ignored_files:
                    continue
                file_path = os.path.join(dirpath, filename)
                if self.included_files:
                    if filename not in self.included_files:
                        continue
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    for i, line in enumerate(file):
                        if self.should_read(line):
                            found_item = re.search(
                                "type\s([A-Za-z_][A-Za-z_0-9]*)\s?=", line
                            )
                            if found_item and found_item.groups()[0]:
                                found_item = found_item.groups()[0]
                                obj_list.append(
                                    PdxScriptObject(found_item, file_path, i + 1)
                                )
        return PdxScriptObjectType(obj_list)

    def should_read(self, x: str) -> bool:
        # Check if a line should be read
        return re.search("type\s[A-Za-z_][A-Za-z_0-9]*\s?=", x)


class GuiTemplate(GameObjectBase):
    def __init__(self):
        super().__init__(
            settings.get("PathsToGuiModFiles"), settings.get("GuiBaseGamePath")
        )
        self.get_data("gui")

    def get_pdx_object_list(self, path: str) -> PdxScriptObjectType:
        obj_list = list()
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in [f for f in filenames if f.endswith(".gui")]:
                if filename in self.ignored_files:
                    continue
                file_path = os.path.join(dirpath, filename)
                if self.included_files:
                    if filename not in self.included_files:
                        continue
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    for i, line in enumerate(file):
                        if self.should_read(line):
                            found_item = re.search(
                                "template\s([A-Za-z_][A-Za-z_0-9]*)", line
                            )
                            if found_item and found_item.groups()[0]:
                                found_item = found_item.groups()[0]
                                obj_list.append(
                                    PdxScriptObject(found_item, file_path, i + 1)
                                )
        return PdxScriptObjectType(obj_list)

    def should_read(self, x: str) -> bool:
        # Check if a line should be read
        return re.search("template\s[A-Za-z_][A-Za-z_0-9]*", x)


# Victoria 3 Game Object Class implementations
class V3AiStrategy(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\ai_strategies")


class V3BuildingGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\building_groups")


class V3Building(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\buildings")


class V3CharacterTrait(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\character_traits")


class V3Culture(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\cultures")


class V3Decree(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\decrees")


class V3DiplomaticAction(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\diplomatic_actions")


class V3DiplomaticPlay(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\diplomatic_plays")


class V3GameRules(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\game_rules")


class V3Goods(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\goods")


class V3GovernmentType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\government_types")


class V3Institutions(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\institutions")


class V3Ideology(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\ideologies")


class V3InterestGroupTrait(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\interest_group_traits")


class V3InterestGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\interest_groups")


class V3JournalEntry(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\journal_entries")


class V3LawGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\law_groups")


class V3Law(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\laws")


class V3Modifier(GameObjectBase):
    def __init__(self):
        super().__init__(
            v3_mod_files, v3_files_path, ignored_files=["00_static_modifiers.txt"]
        )
        self.get_data("common\\modifiers")


class V3Party(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\parties")


class V3PopNeed(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\pop_needs")


class V3PopType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\pop_types")


class V3ProductionMethodGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\production_method_groups")


class V3ProductionMethod(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\production_methods")


class V3Religion(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\religions")


class V3ScriptValue(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\script_values")


class V3ScriptedEffect(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\scripted_effects")


class V3ScriptedModifier(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\scripted_modifiers")


class V3ScriptedTrigger(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\scripted_triggers")


class V3StateTrait(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\state_traits")


class V3StrategicRegion(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\strategic_regions")


class V3SubjectType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\subject_types")


class V3Technology(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\technology")


class V3Terrain(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\terrain")


class V3StateRegion(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("map_data\\state_regions")


class V3Country(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\country_definitions")


class V3CountryRank(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\country_ranks")


class V3CountryType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\country_types")


class PdxColorObject(PdxScriptObject):
    def __init__(self, key, path, line, color):
        super().__init__(key, path, line)
        self.color = color
        self.rgb_color = self.get_rgb_color()

    def get_rgb_color(self):
        """
        Color Formats:
                color1 = hsv { 1.0 1.0 1.0 }
                color2 = hsv360 { 360 100 100 }
                color3 = { 255 255 255 }
                color4 = rgb { 255 255 255 }
                color5 = hex { aabbccdd }
        This function merges all of these formats into one and returns (r, g, b) tuple
        """
        object_color = self.color
        r = 255
        g = 255
        b = 0
        if object_color.startswith("rgb") or object_color.startswith("{"):
            split_color = object_color.split("{")[1].replace(" }", "")
            split_color = split_color.split(" ")
            r = float(split_color[1]) * 255
            g = float(split_color[2]) * 255
            b = float(split_color[3]) * 255
        if re.search(r"\bhsv\b", object_color):
            split_color = object_color.split("{")[1].replace(" }", "")
            split_color = object_color.split(" ")
            h = float(split_color[2])
            s = float(split_color[3])
            v = float(split_color[4])
            rgb = self.hsv2rgb(h, s, v)
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
        if re.search(r"\bhsv360\b", object_color):
            split_color = object_color.split("{")[1].replace(" }", "")
            split_color = object_color.split(" ")
            h = float(split_color[2]) / 360
            s = float(split_color[3]) / 100
            v = float(split_color[4]) / 100
            rgb = self.hsv2rgb(h, s, v)
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
            if (
                split_color[2] == "187"
                and split_color[3] == "83"
                and split_color[4] == "146"
            ):
                r = 230
                g = 0
                b = 230
        if re.search(r"\bhex\b", object_color):
            split_color = object_color.split("{")[1].replace(" }", "")
            split_color = split_color.split("#").replace(" ", "")
            return tuple(int(split_color[i : i + 2], 16) for i in (0, 2, 4))

        return (r, g, b)

    def hsv2rgb(self, h, s, v):
        return tuple(round(i * 255) for i in hsv_to_rgb(h, s, v))

    def __eq__(self, other):
        if isinstance(other, V3NamedColor):
            return self.key == other.key
        elif isinstance(other, str):
            return self.key == other
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, V3NamedColor):
            return self.key < other.key
        elif isinstance(other, str):
            return self.key < other
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, V3NamedColor):
            return self.key > other.key
        elif isinstance(other, str):
            return self.key > other
        else:
            return False


def make_named_color_object(objects: dict) -> GameObjectBase:
    obj_list = list()
    for i in objects:
        obj_list.append(PdxColorObject(i, objects[i][0], objects[i][1], objects[i][2]))
    game_object = GameObjectBase()
    game_object.main = PdxScriptObjectType(obj_list)
    return game_object


class V3NamedColor(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path, level=1)
        self.get_data("common\\named_colors")

    def to_dict(self) -> dict:
        d = dict()
        for i in self.main.objects:
            d[i.key] = [i.path, i.line, i.color]
        return d

    def get_pdx_object_list(self, path: str) -> PdxScriptObjectType:
        obj_list = list()
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in [f for f in filenames if f.endswith(".txt")]:
                if filename in self.ignored_files:
                    continue
                file_path = os.path.join(dirpath, filename)
                if self.included_files:
                    if filename not in self.included_files:
                        continue
                with open(file_path, "r", encoding="utf-8-sig") as file:
                    for i, line in enumerate(file):
                        if self.should_read(line):
                            found_item = re.search(
                                r"([A-Za-z_][A-Za-z_0-9]*)\s*=(.*)", line
                            )
                            if found_item and found_item.groups()[0]:
                                item_color = found_item.groups()[1]
                                found_item = found_item.groups()[0]
                                item_color = item_color.strip().split("#")[0]
                                item_color = item_color.rpartition("}")[0]
                                if not item_color:
                                    continue
                                else:
                                    item_color = item_color.replace("\t", " ") + " }"
                                    item_color = re.sub(r"\s+", " ", item_color)
                                    obj_list.append(
                                        PdxColorObject(
                                            found_item, file_path, i + 1, item_color
                                        )
                                    )
        return PdxScriptObjectType(obj_list)

    def should_read(self, x: str) -> bool:
        # Check if a line should be read
        return re.search(r"([A-Za-z_][A-Za-z_0-9]*)\s*=", x)


class V3BattleCondition(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\battle_conditions")


class V3CommanderRank(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\commander_ranks")


class V3CultureGraphics(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\culture_graphics")


class V3ProposalType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\proposal_types")


class V3DiscriminationTrait(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\discrimination_traits")


base_object = GameObjectBase()
# Gui globals

gui_types = gui_templates = base_object

# Global Object Variables that get set on plugin_loaded
ai_strats = (
    bgs
) = (
    buildings
) = char_traits = cultures = mods = decrees = diplo_actions = diplo_plays = base_object
game_rules = (
    goods
) = (
    gov_types
) = ideologies = institutions = ig_traits = igs = jes = law_groups = laws = base_object
parties = (
    pop_needs
) = (
    pop_types
) = pm_groups = pms = religions = state_traits = strategic_regions = base_object
subject_types = technologies = terrains = state_regions = base_object
script_values = scripted_effects = scripted_modifiers = scripted_triggers = base_object
countries = (
    country_ranks
) = (
    country_types
) = named_colors = battle_conditions = commander_ranks = culture_graphics = base_object
proposal_types = discrimination_traits = base_object
# Function to fill all global game objects that get set in non-blocking async function on plugin_loaded
# Setting all the objects can be slow and doing it on every hover (when they are actually used) is even slower,
# so loading it all in on plugin init makes popups actually responsive


def check_mod_for_changes():
    """
    Check if any changes have been made to mod files
    if changes have been made new game objects need to be generated and cached
    """
    object_cache_path = sublime.packages_path() + f"/Victoria3Tools/object_cache.py"
    if os.stat(object_cache_path).st_size < 200:
        # If there are no objects in the cache, they need to be created
        return True
    mod_cache_path = sublime.packages_path() + f"/Victoria3Tools/mod_cache.py"
    with open(mod_cache_path, "r") as f:
        # Save lines without remake_cache function
        mod_cache = f.readlines()
        mod_cache = "".join(mod_cache[0 : len(mod_cache) - 2])
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
                key = re.sub("\W|^(?=\d)", "_", i.split(mod_name)[1])
                value = stats_dict[i]
                f.write(f"{key}{value} ")
            f.write("\n")

    with open(mod_cache_path, "r") as f:
        # Save written mod classes
        new_mod_cache = "".join(f.readlines())
    with open(mod_cache_path, "a") as f:
        # Write remake_cache function that indicates if new game objects need to be made
        f.write(
            f"def remake_cache():\n\treturn {True if mod_cache != new_mod_cache else False}"
        )
    return remake_cache()


def get_gui_objects_from_cache():
    global gui_types, gui_templates
    object_cache = GameObjectCache()

    gui_types = make_object(object_cache.gui_types)
    gui_templates = make_object(object_cache.gui_templates)


def get_objects_from_cache():
    global igs, ai_strats, bgs, buildings, char_traits, cultures, mods, decrees, diplo_actions, diplo_plays, game_rules, goods
    global gov_types, ideologies, institutions, ig_traits, igs, jes, law_groups, laws, parties, pop_needs, pop_types, pm_groups
    global pms, religions, state_traits, strategic_regions, subject_types, technologies, terrains, state_regions, script_values, scripted_effects, scripted_modifiers, scripted_triggers
    global gui_types, gui_templates
    global countries, country_ranks, country_types, culture_graphics, named_colors, battle_conditions, commander_ranks, proposal_types, discrimination_traits
    object_cache = GameObjectCache()

    countries = make_object(object_cache.countries)
    country_ranks = make_object(object_cache.country_ranks)
    country_types = make_object(object_cache.country_types)
    culture_graphics = make_object(object_cache.culture_graphics)
    named_colors = make_named_color_object(object_cache.named_colors)
    battle_conditions = make_object(object_cache.battle_conditions)
    commander_ranks = make_object(object_cache.commander_ranks)
    ai_strats = make_object(object_cache.ai_strats)
    bgs = make_object(object_cache.bgs)
    buildings = make_object(object_cache.buildings)
    char_traits = make_object(object_cache.char_traits)
    cultures = make_object(object_cache.cultures)
    mods = make_object(object_cache.mods)
    decrees = make_object(object_cache.decrees)
    diplo_actions = make_object(object_cache.diplo_actions)
    diplo_plays = make_object(object_cache.diplo_plays)
    game_rules = make_object(object_cache.game_rules)
    goods = make_object(object_cache.goods)
    gov_types = make_object(object_cache.gov_types)
    ideologies = make_object(object_cache.ideologies)
    institutions = make_object(object_cache.institutions)
    ig_traits = make_object(object_cache.ig_traits)
    igs = make_object(object_cache.igs)
    jes = make_object(object_cache.jes)
    law_groups = make_object(object_cache.law_groups)
    laws = make_object(object_cache.laws)
    parties = make_object(object_cache.parties)
    pop_needs = make_object(object_cache.pop_needs)
    pop_types = make_object(object_cache.pop_types)
    pm_groups = make_object(object_cache.pm_groups)
    pms = make_object(object_cache.pms)
    religions = make_object(object_cache.religions)
    state_traits = make_object(object_cache.state_traits)
    strategic_regions = make_object(object_cache.strategic_regions)
    subject_types = make_object(object_cache.subject_types)
    technologies = make_object(object_cache.technologies)
    terrains = make_object(object_cache.terrains)
    state_regions = make_object(object_cache.state_regions)
    script_values = make_object(object_cache.script_values)
    scripted_effects = make_object(object_cache.scripted_effects)
    scripted_modifiers = make_object(object_cache.scripted_modifiers)
    scripted_triggers = make_object(object_cache.scripted_triggers)
    gui_types = make_object(object_cache.gui_types)
    gui_templates = make_object(object_cache.gui_templates)
    proposal_types = make_object(object_cache.proposal_types)
    discrimination_traits = make_object(object_cache.discrimination_traits)


def cache_all_objects():
    # Write all generated objects to cache
    path = sublime.packages_path() + f"/Victoria3Tools/object_cache.py"
    with open(path, "w") as f:
        f.write("class GameObjectCache:\n\tdef __init__(self):")
        f.write(f"\n\t\tself.ai_strats = {ai_strats.to_json()}")
        f.write(f"\n\t\tself.bgs = {bgs.to_json()}")
        f.write(f"\n\t\tself.buildings = {buildings.to_json()}")
        f.write(f"\n\t\tself.char_traits = {char_traits.to_json()}")
        f.write(f"\n\t\tself.cultures = {cultures.to_json()}")
        f.write(f"\n\t\tself.mods = {mods.to_json()}")
        f.write(f"\n\t\tself.decrees = {decrees.to_json()}")
        f.write(f"\n\t\tself.diplo_actions = {diplo_actions.to_json()}")
        f.write(f"\n\t\tself.diplo_plays = {diplo_plays.to_json()}")
        f.write(f"\n\t\tself.game_rules = {game_rules.to_json()}")
        f.write(f"\n\t\tself.goods = {goods.to_json()}")
        f.write(f"\n\t\tself.gov_types = {gov_types.to_json()}")
        f.write(f"\n\t\tself.ideologies = {ideologies.to_json()}")
        f.write(f"\n\t\tself.institutions = {institutions.to_json()}")
        f.write(f"\n\t\tself.ig_traits = {ig_traits.to_json()}")
        f.write(f"\n\t\tself.igs = {igs.to_json()}")
        f.write(f"\n\t\tself.jes = {jes.to_json()}")
        f.write(f"\n\t\tself.law_groups = {law_groups.to_json()}")
        f.write(f"\n\t\tself.laws = {laws.to_json()}")
        f.write(f"\n\t\tself.parties = {parties.to_json()}")
        f.write(f"\n\t\tself.pop_needs = {pop_needs.to_json()}")
        f.write(f"\n\t\tself.pop_types = {pop_types.to_json()}")
        f.write(f"\n\t\tself.pm_groups = {pm_groups.to_json()}")
        f.write(f"\n\t\tself.pms = {pms.to_json()}")
        f.write(f"\n\t\tself.religions = {religions.to_json()}")
        f.write(f"\n\t\tself.state_traits = {state_traits.to_json()}")
        f.write(f"\n\t\tself.strategic_regions = {strategic_regions.to_json()}")
        f.write(f"\n\t\tself.subject_types = {subject_types.to_json()}")
        f.write(f"\n\t\tself.technologies = {technologies.to_json()}")
        f.write(f"\n\t\tself.terrains = {terrains.to_json()}")
        f.write(f"\n\t\tself.state_regions = {state_regions.to_json()}")
        f.write(f"\n\t\tself.script_values = {script_values.to_json()}")
        f.write(f"\n\t\tself.scripted_effects = {scripted_effects.to_json()}")
        f.write(f"\n\t\tself.scripted_modifiers = {scripted_modifiers.to_json()}")
        f.write(f"\n\t\tself.scripted_triggers = {scripted_triggers.to_json()}")
        f.write(f"\n\t\tself.gui_types = {gui_types.to_json()}")
        f.write(f"\n\t\tself.gui_templates = {gui_templates.to_json()}")
        f.write(f"\n\t\tself.countries = {countries.to_json()}")
        f.write(f"\n\t\tself.country_ranks = {country_ranks.to_json()}")
        f.write(f"\n\t\tself.country_types = {country_types.to_json()}")
        f.write(f"\n\t\tself.culture_graphics = {culture_graphics.to_json()}")
        f.write(f"\n\t\tself.battle_conditions = {battle_conditions.to_json()}")
        f.write(f"\n\t\tself.commander_ranks = {commander_ranks.to_json()}")
        f.write(f"\n\t\tself.proposal_types = {proposal_types.to_json()}")
        f.write(f"\n\t\tself.discrimination_traits = {discrimination_traits.to_json()}")
        f.write(f"\n\t\tself.named_colors = {named_colors.to_json()}")


def create_game_objects():
    t0 = time.time()

    def load_first():
        global ai_strats, bgs, buildings, char_traits, cultures, decrees, diplo_actions, diplo_plays
        ai_strats = V3AiStrategy()
        bgs = V3BuildingGroup()
        buildings = V3Building()
        char_traits = V3CharacterTrait()
        cultures = V3Culture()
        decrees = V3Decree()
        diplo_actions = V3DiplomaticAction()
        diplo_plays = V3DiplomaticPlay()

    def load_second():
        global mods, game_rules, goods, gov_types, ideologies, institutions, ig_traits, igs
        mods = V3Modifier()
        game_rules = V3GameRules()
        goods = V3Goods()
        gov_types = V3GovernmentType()
        ideologies = V3Ideology()
        institutions = V3Institutions()
        ig_traits = V3InterestGroupTrait()
        igs = V3InterestGroup()

    def load_third():
        global jes, law_groups, laws, parties, pop_needs, pop_types, pm_groups
        jes = V3JournalEntry()
        law_groups = V3LawGroup()
        laws = V3Law()
        parties = V3Party()
        pop_needs = V3PopNeed()
        pop_types = V3PopType()
        pm_groups = V3ProductionMethodGroup()

    def load_fourth():
        global pms, religions, script_values, scripted_effects, scripted_modifiers, scripted_triggers, proposal_types, discrimination_traits
        pms = V3ProductionMethod()
        religions = V3Religion()
        script_values = V3ScriptValue()
        scripted_effects = V3ScriptedEffect()
        scripted_modifiers = V3ScriptedModifier()
        scripted_triggers = V3ScriptedTrigger()
        proposal_types = V3ProposalType()
        discrimination_traits = V3DiscriminationTrait()

    def load_fifth():
        global state_traits, strategic_regions, subject_types, technologies, terrains, state_regions, countries
        state_traits = V3StateTrait()
        strategic_regions = V3StrategicRegion()
        subject_types = V3SubjectType()
        technologies = V3Technology()
        terrains = V3Terrain()
        state_regions = V3StateRegion()
        countries = V3Country()

    def load_sixth():
        global country_ranks, country_types, culture_graphics, named_colors, battle_conditions, commander_ranks
        country_ranks = V3CountryRank()
        country_types = V3CountryType()
        culture_graphics = V3CultureGraphics()
        named_colors = V3NamedColor()
        battle_conditions = V3BattleCondition()
        commander_ranks = V3CommanderRank()

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
    def load_first():
        global gui_types
        gui_types = GuiType()

    def load_second():
        global gui_templates
        gui_templates = GuiTemplate()
        gui_templates.remove("inside")
        gui_templates.remove("you")
        gui_templates.remove("can")
        gui_templates.remove("but")
        gui_templates.remove("on")
        gui_templates.remove("within")
        gui_templates.remove("names")

    thread1 = threading.Thread(target=load_first)
    thread2 = threading.Thread(target=load_second)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    # Cache created objects
    sublime.set_timeout_async(lambda: cache_all_objects(), 0)


def plugin_loaded():
    global settings, v3_files_path, v3_mod_files, gui_files_path, gui_mod_files
    settings = sublime.load_settings("Victoria Syntax.sublime-settings")
    v3_files_path = settings.get("Victoria3FilesPath")
    v3_mod_files = settings.get("PathsToModFiles")
    gui_files_path = settings.get("GuiBaseGamePath")
    gui_mod_files = settings.get("PathsToGuiModFiles")
    script_enabled = settings.get("DisableVictoriaScriptingFeatures")

    if check_mod_for_changes():
        # Create new objects
        if script_enabled:
            sublime.set_timeout_async(lambda: create_game_objects(), 0)
        else:
            sublime.set_timeout_async(lambda: load_gui_objects(), 0)
    elif settings.get("DisableVictoriaScriptingFeatures"):
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
        scripted_triggers.keys(), "Scripted Triggers", "string.scripted.trigger"
    )
    lines += write_syntax(
        scripted_effects.keys(), "Scripted Effects", "keyword.scripted.effect"
    )
    lines += write_syntax(
        script_values.keys(), "Scripted Values", "storage.type.script.value"
    )

    # All GameObjects get entity.name scope
    lines += write_syntax(ai_strats.keys(), "Ai Strategies", "entity.name.ai.strat")
    lines += write_syntax(bgs.keys(), "Building Groups", "entity.name.bg")
    lines += write_syntax(buildings.keys(), "Buildings", "entity.name.building")
    lines += write_syntax(
        char_traits.keys(), "Character Traits", "entity.name.character.trait"
    )
    lines += write_syntax(cultures.keys(), "Cultures", "entity.name.culture")
    lines += write_syntax(mods.keys(), "Modifiers", "entity.name.modifier")
    lines += write_syntax(decrees.keys(), "Decrees", "entity.name.decree")
    lines += write_syntax(
        diplo_actions.keys(), "Diplomatic Actions", "entity.name.diplo.action"
    )
    lines += write_syntax(
        diplo_plays.keys(), "Diplomatic Plays", "entity.name.diplo.play"
    )
    lines += write_syntax(game_rules.keys(), "Game Rules", "entity.name.game.rule")
    lines += write_syntax(goods.keys(), "Trade Goods", "entity.name.trade.good")
    lines += write_syntax(gov_types.keys(), "Gov Types", "entity.name.gov.type")
    lines += write_syntax(ideologies.keys(), "Ideologies", "entity.name.ideology")
    lines += write_syntax(
        institutions.keys(), "Institutions", "entity.name.institution"
    )
    lines += write_syntax(ig_traits.keys(), "Ig Traits", "entity.name.ig.trait")
    lines += write_syntax(igs.keys(), "Interest Groups", "entity.name.interest.group")
    lines += write_syntax(jes.keys(), "Journal Entries", "entity.name.journal.entry")
    lines += write_syntax(law_groups.keys(), "Law Groups", "entity.name.law.group")
    lines += write_syntax(laws.keys(), "Laws", "entity.name.law")
    lines += write_syntax(parties.keys(), "Parties", "entity.name.party")
    lines += write_syntax(pop_needs.keys(), "Pop Needs", "entity.name.pop.need")
    lines += write_syntax(pop_types.keys(), "Pop Types", "entity.name.pop.type")
    lines += write_syntax(
        pm_groups.keys(), "Production Method Groups", "entity.name.pm.groups"
    )
    lines += write_syntax(pms.keys(), "Production Methods", "entity.name.pm")
    lines += write_syntax(religions.keys(), "Religions", "entity.name.religion")
    lines += write_syntax(
        state_traits.keys(), "State Traits", "entity.name.state.trait"
    )
    lines += write_syntax(
        strategic_regions.keys(), "Strategic Regions", "entity.name.strategic.region"
    )
    lines += write_syntax(
        subject_types.keys(), "Subject Types", "entity.name.subject.type"
    )
    lines += write_syntax(technologies.keys(), "Technologies", "entity.name.tech")
    lines += write_syntax(terrains.keys(), "Terrains", "entity.name.terrain")
    lines += write_syntax(
        state_regions.keys(), "State Regions", "entity.name.state.region"
    )
    lines += write_syntax(countries.keys(), "Countries", "entity.name.countries")
    lines += write_syntax(
        country_ranks.keys(), "Country Ranks", "entity.name.country.ranks"
    )
    lines += write_syntax(
        country_types.keys(), "Country Types", "entity.name.country.types"
    )
    lines += write_syntax(
        culture_graphics.keys(), "Culture Graphics", "entity.name.culture.graphics"
    )
    lines += write_syntax(
        named_colors.keys(), "Named Colors", "entity.name.named.colors"
    )
    lines += write_syntax(
        battle_conditions.keys(), "Battle Conditions", "entity.name.battle.conditions"
    )
    lines += write_syntax(
        commander_ranks.keys(), "Commander Ranks", "entity.name.commander.ranks"
    )
    lines += write_syntax(
        proposal_types.keys(), "Proposal Types", "entity.name.proposal.type"
    )
    lines += write_syntax(
        discrimination_traits.keys(),
        "Discrimination Traits",
        "entity.name.discrimination.trait",
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


FIND_SIMPLE_DECLARATION_RE = '\s?=\s?(")?'
FIND_ERROR_RE = '\s?=\s?"?([A-Za-z_][A-Za-z_0-9]*)"?'
FIND_SCOPE_RE = ':"?([A-Za-z_][A-Za-z_0-9]*)"?'


class V3CompletionsEventListener(sublime_plugin.EventListener):
    def __init__(self):
        self.trigger_field = False
        self.effect_field = False
        self.modifier_field = False
        self.mtth_field = False
        self.trigger_views = []
        self.effect_views = []
        self.modfier_views = []
        self.mtth_views = []

        self.show_ai = False
        self.show_b = False
        self.show_bg = False
        self.show_c_traits = False
        self.show_ai_views = []
        self.show_b_views = []
        self.show_bg_views = []
        self.show_c_traits_views = []
        self.culture = False
        self.culture_views = []
        self.decree = False
        self.decree_views = []
        self.diplo_action = False
        self.diplo_action_views = []
        self.diplo_play = False
        self.diplo_play_views = []
        self.game_rule = False
        self.game_rule_views = []
        self.good = False
        self.good_views = []
        self.gov_type = False
        self.gov_type_views = []
        self.ideology = False
        self.ideology_views = []
        self.ig = False
        self.ig_views = []
        self.institution = False
        self.institution_views = []
        self.journal = False
        self.journal_views = []
        self.law_group = False
        self.law_group_views = []
        self.law = False
        self.law_views = []
        self.modifier = False
        self.modifier_views = []
        self.party = False
        self.party_views = []
        self.pop_type = False
        self.pop_type_views = []
        self.pm = False
        self.pm_views = []
        self.pop_type_views = []
        self.religion = False
        self.religion_views = []
        self.state_trait = False
        self.state_trait_views = []
        self.strategic_region = False
        self.strategic_region_views = []
        self.subject_type = False
        self.subject_type_views = []
        self.tech = False
        self.tech_views = []
        self.terrain = False
        self.terrain_views = []
        self.state_region = False
        self.state_region_views = []
        self.countries = False
        self.countries_views = []
        self.country_ranks = False
        self.country_ranks_views = []
        self.country_types = False
        self.country_types_views = []
        self.culture_graphics = False
        self.culture_graphics_views = []
        self.named_colors = False
        self.named_colors_views = []
        self.battle_conditions = False
        self.battle_conditions_views = []
        self.commander_ranks = False
        self.commander_ranks_views = []

        self.proposal_types = False
        self.proposal_types_views = []
        self.discrimination_traits = False
        self.discrimination_traits_views = []

        self.error_words = []

    def on_deactivated_async(self, view):
        """
        Remove field states when view loses focus
        if cursor was in a field in the old view but not the new view the completions will still be accurate
        save the id of the view so it can be readded when it regains focus
        """

        if not settings.get("DisableVictoriaScriptingFeatures"):
            return

        vid = view.id()
        if self.trigger_field:
            self.trigger_field = False
            self.trigger_views.append(vid)
        if self.effect_field:
            self.effect_field = False
            self.effect_views.append(vid)
        if self.modifier_field:
            self.modifier_field = False
            self.modfier_views.append(vid)
        if self.mtth_field:
            self.mtth_field = False
            self.mtth_views.append(vid)
        if self.show_ai:
            self.show_ai = False
            self.show_ai_views.append(vid)
        if self.show_b:
            self.show_b = False
            self.show_b_views.append(vid)
        if self.show_bg:
            self.show_bg = False
            self.show_bg_views.append(vid)
        if self.show_c_traits:
            self.show_c_traits = False
            self.show_c_traits_views.append(vid)
        if self.culture:
            self.culture = False
            self.culture_views.append(vid)
        if self.decree:
            self.decree = False
            self.decree_views.append(vid)
        if self.diplo_action:
            self.diplo_action = False
            self.diplo_action_views.append(vid)
        if self.diplo_play:
            self.diplo_play = False
            self.diplo_play_views.append(vid)
        if self.game_rule:
            self.game_rule = False
            self.game_rule_views.append(vid)
        if self.good:
            self.good = False
            self.good_views.append(vid)
        if self.gov_type:
            self.gov_type = False
            self.gov_type_views.append(vid)
        if self.ideology:
            self.ideology = False
            self.ideology_views.append(vid)
        if self.ig:
            self.ig = False
            self.ig_views.append(vid)
        if self.institution:
            self.institution = False
            self.institution_views.append(vid)
        if self.journal:
            self.journal = False
            self.journal_views.append(vid)
        if self.journal:
            self.journal = False
            self.journal_views.append(vid)
        if self.law:
            self.law = False
            self.law_views.append(vid)
        if self.modifier:
            self.modifier = False
            self.modifier_views.append(vid)
        if self.party:
            self.party = False
            self.party_views.append(vid)
        if self.pop_type:
            self.pop_type = False
            self.pop_type_views.append(vid)
        if self.pm:
            self.pm = False
            self.pm_views.append(vid)
        if self.religion:
            self.religion = False
            self.religion_views.append(vid)
        if self.state_trait:
            self.state_trait = False
            self.state_trait_views.append(vid)
        if self.strategic_region:
            self.strategic_region = False
            self.strategic_region_views.append(vid)
        if self.subject_type:
            self.subject_type = False
            self.subject_type_views.append(vid)
        if self.tech:
            self.tech = False
            self.tech_views.append(vid)
        if self.terrain:
            self.terrain = False
            self.terrain_views.append(vid)
        if self.state_region:
            self.state_region = False
            self.state_region_views.append(vid)
        if self.countries:
            self.countries = False
            self.countries_views.append(vid)
        if self.country_ranks:
            self.country_ranks = False
            self.country_ranks_views.append(vid)
        if self.country_types:
            self.country_types = False
            self.country_types_views.append(vid)
        if self.culture_graphics:
            self.culture_graphics = False
            self.culture_graphics_views.append(vid)
        if self.named_colors:
            self.named_colors = False
            self.named_colors_views.append(vid)
        if self.battle_conditions:
            self.battle_conditions = False
            self.battle_conditions_views.append(vid)
        if self.commander_ranks:
            self.commander_ranks = False
            self.commander_ranks_views.append(vid)
        if self.proposal_types:
            self.proposal_types = False
            self.proposal_types_views.append(vid)
        if self.discrimination_traits:
            self.discrimination_traits = False
            self.discrimination_traits_views.append(vid)

    def on_activated_async(self, view):
        if not settings.get("DisableVictoriaScriptingFeatures"):
            return

        vid = view.id()
        if vid in self.trigger_views:
            self.trigger_field = True
            self.trigger_views.remove(vid)
        if vid in self.effect_views:
            self.effect_field = True
            self.effect_views.remove(vid)
        if vid in self.modfier_views:
            self.modifier_field = True
            self.modfier_views.remove(vid)
        if vid in self.mtth_views:
            self.mtth_field = True
            self.mtth_views.remove(vid)
        if self.show_ai_views:
            self.show_ai = True
            self.show_ai_views.remove(vid)
        if self.show_b_views:
            self.show_b = True
            self.show_b_views.remove(vid)
        if self.show_bg_views:
            self.show_bg = True
            self.show_bg_views.remove(vid)
        if self.show_c_traits_views:
            self.show_c_traits = True
            self.show_c_traits_views.remove(vid)
        if self.culture_views:
            self.culture = True
            self.culture_views.remove(vid)
        if self.decree_views:
            self.decree = True
            self.decree_views.remove(vid)
        if self.diplo_action_views:
            self.diplo_action = True
            self.diplo_action_views.remove(vid)
        if self.diplo_play_views:
            self.diplo_play = True
            self.diplo_play_views.remove(vid)
        if self.game_rule_views:
            self.game_rule = True
            self.game_rule_views.remove(vid)
        if self.good_views:
            self.good = True
            self.good_views.remove(vid)
        if self.gov_type_views:
            self.gov_type = True
            self.gov_type_views.remove(vid)
        if self.ideology_views:
            self.ideology = True
            self.ideology_views.remove(vid)
        if self.ig_views:
            self.ig = True
            self.ig_views.remove(vid)
        if self.institution_views:
            self.institution = True
            self.institution_views.remove(vid)
        if self.journal_views:
            self.journal = True
            self.journal_views.remove(vid)
        if self.law_group_views:
            self.law_group = True
            self.law_group_views.remove(vid)
        if self.law_views:
            self.law = True
            self.law_views.remove(vid)
        if self.modifier_views:
            self.modifier = True
            self.modifier_views.remove(vid)
        if self.party_views:
            self.party = True
            self.party_views.remove(vid)
        if self.pop_type_views:
            self.pop_type = True
            self.pop_type_views.remove(vid)
        if self.pm_views:
            self.pm = True
            self.pm_views.remove(vid)
        if self.religion_views:
            self.religion = True
            self.religion_views.remove(vid)
        if self.state_trait_views:
            self.state_trait = True
            self.state_trait_views.remove(vid)
        if self.strategic_region_views:
            self.strategic_region = True
            self.strategic_region_views.remove(vid)
        if self.subject_type_views:
            self.subject_type = True
            self.subject_type_views.remove(vid)
        if self.tech_views:
            self.tech = True
            self.tech_views.remove(vid)
        if self.terrain_views:
            self.terrain = True
            self.terrain_views.remove(vid)
        if self.state_region_views:
            self.state_region = True
            self.state_region_views.remove(vid)
        if self.countries_views:
            self.countries = True
            self.countries_views.remove(vid)
        if self.country_ranks_views:
            self.country_ranks = True
            self.country_ranks_views.remove(vid)
        if self.country_types_views:
            self.country_types = True
            self.country_types_views.remove(vid)
        if self.culture_graphics_views:
            self.culture_graphics = True
            self.culture_graphics_views.remove(vid)
        if self.named_colors_views:
            self.named_colors = True
            self.named_colors_views.remove(vid)
        if self.battle_conditions_views:
            self.battle_conditions = True
            self.battle_conditions_views.remove(vid)
        if self.commander_ranks_views:
            self.commander_ranks = True
            self.commander_ranks_views.remove(vid)
        if self.proposal_types_views:
            self.proposal_types = True
            self.proposal_types_views.remove(vid)
        if self.discrimination_traits_views:
            self.discrimination_traits = True
            self.discrimination_traits_views.remove(vid)

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

        if not settings.get("DisableVictoriaScriptingFeatures"):
            return

        fname = view.file_name()

        if self.show_ai:
            self.show_ai = False
            ai = ai_strats.keys()
            ai = sorted(ai)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_MARKUP, "A", "Ai Strategy"),
                        details=" ",
                    )
                    # Calling sorted() twice makes it so completions are ordered by
                    # 1. the number of times they appear in the current buffer
                    # 2. if they dont appear they show up alphabetically
                    for key in sorted(ai)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.show_b:
            self.show_b = False
            b = buildings.keys()
            b = sorted(b)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "B", "Building"),
                        details=" ",
                    )
                    for key in sorted(b)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.show_bg:
            self.show_bg = False
            bg = bgs.keys()
            bg = sorted(bg)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "B", "Building Group"),
                        details=" ",
                    )
                    for key in sorted(bg)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.show_c_traits:
            self.show_c_traits = False
            ct = char_traits.keys()
            ct = sorted(ct)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "C", "Character Trait"),
                        details=" ",
                    )
                    for key in sorted(ct)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.culture:
            self.culture = False
            cu = cultures.keys()
            cu = sorted(cu)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "C", "Culture"),
                        details=" ",
                    )
                    for key in sorted(cu)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.decree:
            self.decree = False
            de = decrees.keys()
            de = sorted(de)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_MARKUP, "D", "Decree"),
                        details=" ",
                    )
                    for key in sorted(de)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.diplo_action:
            self.diplo_action = False
            da = diplo_actions.keys()
            da = sorted(da)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "D", "Diplomatic Action"),
                        details=" ",
                    )
                    for key in sorted(da)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.diplo_play:
            self.diplo_play = False
            dp = diplo_plays.keys()
            dp = sorted(dp)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "D", "Diplomatic Play"),
                        details=" ",
                    )
                    for key in sorted(dp)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.game_rule:
            self.game_rule = False
            gr = game_rules.keys()
            gr = sorted(gr)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "G", "Game Rule"),
                        details=" ",
                    )
                    for key in sorted(gr)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.good:
            self.good = False
            go = goods.keys()
            go = sorted(go)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "G", "Trade Good"),
                        details=" ",
                    )
                    for key in sorted(go)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.gov_type:
            self.gov_type = False
            gov = gov_types.keys()
            gov = sorted(gov)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "G", "Government Type"),
                        details=" ",
                    )
                    for key in sorted(gov)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.ideology:
            self.ideology = False
            idea = ideologies.keys()
            idea = sorted(idea)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "I", "Ideology"),
                        details=" ",
                    )
                    for key in sorted(idea)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.institution:
            self.institution = False
            ins = institutions.keys()
            ins = sorted(ins)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "I", "Institution"),
                        details=" ",
                    )
                    for key in sorted(ins)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.ig:
            self.ig = False
            interest = igs.keys()
            interest = sorted(interest)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_MARKUP, "I", "Interest Group"),
                        details=" ",
                    )
                    for key in sorted(interest)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.journal:
            self.journal = False
            je = jes.keys()
            je = sorted(je)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_TYPE, "J", "Journal Entry"),
                        details=" ",
                    )
                    for key in sorted(je)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.law_group:
            self.law_group = False
            lg = law_groups.keys()
            lg = sorted(lg)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "L", "Law Group"),
                        details=" ",
                    )
                    for key in sorted(lg)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.law:
            self.law = False
            law = laws.keys()
            law = sorted(law)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "L", "Law"),
                        details=" ",
                    )
                    for key in sorted(law)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.modifier:
            self.modifier = False
            mod = mods.keys()
            mod = sorted(mod)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "M", "Modifier"),
                        details=" ",
                    )
                    for key in sorted(mod)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.party:
            self.party = False
            pa = parties.keys()
            pa = sorted(pa)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_TYPE, "P", "Political Party"),
                        details=" ",
                    )
                    for key in sorted(pa)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.pop_type:
            self.pop_type = False
            pop = pop_types.keys()
            pop = sorted(pop)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "P", "Pop Type"),
                        details=" ",
                    )
                    for key in sorted(pop)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.pm:
            self.pm = False
            pm = pms.keys()
            pm = sorted(pm)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "P", "Production Method"),
                        details=" ",
                    )
                    for key in sorted(pm)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.religion:
            self.religion = False
            rel = religions.keys()
            rel = sorted(rel)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "R", "Religion"),
                        details=" ",
                    )
                    for key in sorted(rel)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.state_trait:
            self.state_trait = False
            state_trait = state_traits.keys()
            state_trait = sorted(state_trait)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "S", "State Trait"),
                        details=" ",
                    )
                    for key in sorted(state_trait)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.strategic_region:
            self.strategic_region = False
            sr = strategic_regions.keys()
            sr = sorted(sr)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "S", "Strategic Region"),
                        details=" ",
                    )
                    for key in sorted(sr)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.subject_type:
            self.subject_type = False
            st = subject_types.keys()
            st = sorted(st)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_TYPE, "S", "Subject Type"),
                        details=" ",
                    )
                    for key in sorted(st)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.tech:
            self.tech = False
            te = technologies.keys()
            te = sorted(te)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "T", "Technology"),
                        details=" ",
                    )
                    for key in sorted(te)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.terrain:
            self.terrain = False
            terr = terrains.keys()
            terr = sorted(terr)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Terrain"),
                        details=" ",
                    )
                    for key in sorted(terr)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.state_region:
            self.state_region = False
            streg = state_regions.keys()
            streg = sorted(streg)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "S", "State Region"),
                        details=" ",
                    )
                    for key in sorted(streg)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.countries:
            self.countries = False
            c = countries.keys()
            c = sorted(c)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "C", "Country"),
                        details=" ",
                    )
                    for key in sorted(c)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.country_ranks:
            self.country_ranks = False
            cr = country_ranks.keys()
            cr = sorted(cr)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "C", "Country Ranks"),
                        details=" ",
                    )
                    for key in sorted(cr)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.country_types:
            self.country_types = False
            ct = country_types.keys()
            ct = sorted(ct)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "C", "Country Types"),
                        details=" ",
                    )
                    for key in sorted(ct)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.culture_graphics:
            self.culture_graphics = False
            cg = culture_graphics.keys()
            cg = sorted(cg)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "C", "Country Types"),
                        details=" ",
                    )
                    for key in sorted(cg)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.named_colors:
            self.named_colors = False
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=obj.key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "C", "Named Color"),
                        details=" ",
                        annotation=obj.color,
                    )
                    for obj in named_colors
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.battle_conditions:
            self.battle_conditions = False
            bc = battle_conditions.keys()
            bc = sorted(bc)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "B", "Battle Condition"),
                        details=" ",
                    )
                    for key in sorted(bc)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.commander_ranks:
            self.commander_ranks = False
            crk = commander_ranks.keys()
            crk = sorted(crk)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "C", "Commander Rank"),
                        details=" ",
                    )
                    for key in sorted(crk)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.proposal_types:
            self.proposal_types = False
            prt = proposal_types.keys()
            prt = sorted(prt)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "P", "Proposal Types"),
                        details=" ",
                    )
                    for key in sorted(prt)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        if self.discrimination_traits:
            self.discrimination_traits = False
            dit = discrimination_traits.keys()
            dit = sorted(dit)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_VARIABLE, "D", "Discrimination Traits"),
                        details=" ",
                    )
                    for key in sorted(dit)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )

        else:
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
            if self.modifier_field or re.search("(modifiers)", fname):
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

    def simple_scope_match(self, view):
        view_region = sublime.Region(0, view.size())
        view_str = view.substr(view_region)

        # Get the starting bracket index from the syntax scopes
        start_trigger_brackets = view.find_by_selector("meta.trigger.bracket")
        trigger_regions = []
        for br in start_trigger_brackets:
            trigger_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

        start_effect_brackets = view.find_by_selector("meta.effect.bracket")
        effect_regions = []
        for br in start_effect_brackets:
            effect_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

        start_value_brackets = view.find_by_selector("meta.value.bracket")
        value_regions = []
        for br in start_value_brackets:
            value_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

        start_modifier_brackets = view.find_by_selector("meta.modifier.bracket")
        modifier_regions = []
        for br in start_modifier_brackets:
            modifier_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

        selection = view.sel()
        if not selection[0].empty():
            return

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
        # self.trigger_field = False
        # self.effect_field = False
        # self.modifier_field = False
        # self.mtth_field = False
        self.show_ai = False
        self.show_b = False
        self.show_bg = False
        self.show_c_traits = False
        self.culture = False
        self.decree = False
        self.diplo_action = False
        self.diplo_play = False
        self.game_rule = False
        self.good = False
        self.gov_type = False
        self.ideology = False
        self.ig = False
        self.institution = False
        self.journal = False
        self.law_group = False
        self.law = False
        self.modifier = False
        self.party = False
        self.pop_type = False
        self.pm = False
        self.religion = False
        self.state_trait = False
        self.strategic_region = False
        self.subject_type = False
        self.tech = False
        self.terrain = False
        self.state_region = False
        self.countries = False
        self.country_ranks = False
        self.country_types = False
        self.culture_graphics = False
        self.named_colors = False
        self.battle_conditions = False
        self.commander_ranks = False
        self.proposal_types = False
        self.discrimination_traits = False

    def check_for_simple_completions(self, view, point):
        """
        Check if the current cursor position should trigger a autocompletion item
        this is for simple declarations like: remove_building = CursorHere
        """
        self.reset_shown()

        if view.substr(point) == "=":
            return

        line = view.substr(view.line(point))

        for i in self.error_words:
            if i in line:
                view.erase_regions(i)
                self.error_words.remove(i)

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
            "has_ideology",
            "set_ideology",
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
        battle_conditions = ["has_battle_condition"]

        proposal_types_list = ["post_proposal"]
        discrimination_traits_list = ["has_discrimination_trait"]

        # Ai Strats
        for i in ai_list:
            # Error checking if I end up wanting it
            # match = re.search(f"{i}{FIND_ERROR_RE}", line)
            # if match and match.groups()[0] not in keys:
            # 	word = match.groups()[0]
            # 	error_region = sublime.Region((line.rfind(word) + view.line(point).a), (line.rfind(word) + len(word)) + view.line(point).a)
            # 	view.add_regions(view.substr(error_region), [error_region], "invalid", "", sublime.PERSISTENT | sublime.DRAW_SOLID_UNDERLINE |sublime.DRAW_NO_OUTLINE )
            # 	self.error_words.append(view.substr(error_region))
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2  # move over another position if quote is present
                # Check if current point is in one of 3 positions: ={1nospace}{2space}{3quote}
                if idx == point or idx + y == point or idx + 1 == point:
                    #
                    # if len([x for x in ai_strats.keys() if x in line]) == 0:
                    self.show_ai = True
                    view.run_command("auto_complete")
                    break
        # Buildings
        for i in b_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.show_b = True
                    view.run_command("auto_complete")
                    break
        # Building Scopes
        if "b:" in line:
            idx = (
                line.index("b:") + view.line(point).a + 2
            )  # add the length of "b:" so index is at the end where completion should happen
            if idx == point:
                self.show_b = True
                view.run_command("auto_complete")
        # Building Groups
        for i in bg_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.show_bg = True
                    view.run_command("auto_complete")
                    break
        # Character Traits
        for i in char_traits_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.show_c_traits = True
                    view.run_command("auto_complete")
                    break
        # Culture Scopes
        if "cu:" in line:
            idx = line.index("cu:") + view.line(point).a + 3
            if idx == point:
                self.culture = True
                view.run_command("auto_complete")
        # Cultures
        for i in culture_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.culture = True
                    view.run_command("auto_complete")
                    break
        # Decree Scopes
        if "decree_cost:" in line:
            idx = line.index("decree_cost:") + view.line(point).a + 12
            if idx == point:
                self.decree = True
                view.run_command("auto_complete")
        # Decrees
        for i in decree_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.decree = True
                    view.run_command("auto_complete")
                    break
        # Diplo Actions
        for i in diplo_action_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.diplo_action = True
                    view.run_command("auto_complete")
                    break
        # Diplo Plays
        for i in diplo_play_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.diplo_play = True
                    view.run_command("auto_complete")
                    break
        # Game Rules
        for i in game_rules_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.game_rule = True
                    view.run_command("auto_complete")
                    break
        # Trade goods
        for i in trade_goods_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.good = True
                    view.run_command("auto_complete")
                    break
        # Trade good Scopes
        if "goods:" in line:
            idx = line.index("goods:") + view.line(point).a + 6
            if idx == point:
                self.good = True
                view.run_command("auto_complete")
        if "g:" in line:
            idx = line.index("g:") + view.line(point).a + 2
            if idx == point:
                self.good = True
                view.run_command("auto_complete")
        # Government Types
        for i in gov_types_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.gov_type = True
                    view.run_command("auto_complete")
                    break
        # Ideologies
        for i in ideologies_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.ideology = True
                    view.run_command("auto_complete")
                    break
        # Institutions
        for i in institutions_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.institution = True
                    view.run_command("auto_complete")
                    break
        # Institution Scope
        if "institution:" in line:
            idx = line.index("institution:") + view.line(point).a + 12
            if idx == point:
                self.institution = True
                view.run_command("auto_complete")
        # Interest Groups
        for i in ig_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.ig = True
                    view.run_command("auto_complete")
                    break
        # Ig Scope
        if "ig:" in line:
            idx = line.index("ig:") + view.line(point).a + 3
            if idx == point:
                self.ig = True
                view.run_command("auto_complete")
        if "interest_group:" in line:
            idx = line.index("interest_group:") + view.line(point).a + 15
            if idx == point:
                self.ig = True
                view.run_command("auto_complete")
        # Journal Entries
        for i in journal_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.journal = True
                    view.run_command("auto_complete")
                    break
        # Journal Entry Scopes
        if "je:" in line:
            idx = line.index("je:") + view.line(point).a + 3
            if idx == point:
                self.journal = True
                view.run_command("auto_complete")
        # Law Group Scopes
        if "active_law:" in line:
            idx = line.index("active_law:") + view.line(point).a + 11
            if idx == point:
                self.law_group = True
                view.run_command("auto_complete")
        # Law Scopes
        if "law_type:" in line:
            idx = line.index("law_type:") + view.line(point).a + 9
            if idx == point:
                self.law = True
                view.run_command("auto_complete")
        # Modifiers
        for i in modifier_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.modifier = True
                    view.run_command("auto_complete")
                    break
        # Parties
        for i in party_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.party = True
                    view.run_command("auto_complete")
                    break
        # Party Scopes
        if "py:" in line:
            idx = line.index("py:") + view.line(point).a + 3
            if idx == point:
                self.party = True
                view.run_command("auto_complete")
        if "party:" in line:
            idx = line.index("party:") + view.line(point).a + 6
            if idx == point:
                self.party = True
                view.run_command("auto_complete")
        # Pop Types
        for i in pops_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.pop_type = True
                    view.run_command("auto_complete")
                    break
        if "pop_type:" in line:
            idx = line.index("pop_type:") + view.line(point).a + 9
            if idx == point:
                self.pop_type = True
                view.run_command("auto_complete")
        # Production Methods
        for i in pms_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.pm = True
                    view.run_command("auto_complete")
                    break
        # Religions
        for i in religions_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.religion = True
                    view.run_command("auto_complete")
                    break
        if "rel:" in line:
            idx = line.index("rel:") + view.line(point).a + 4
            if idx == point:
                self.religion = True
                view.run_command("auto_complete")
        if "religion:" in line:
            idx = line.index("religion:") + view.line(point).a + 4
            if idx == point:
                self.religion = True
                view.run_command("auto_complete")
        # State Trait
        for i in state_trait_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.state_trait = True
                    view.run_command("auto_complete")
                    break
        # Strategic Region
        for i in strategic_regions_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.strategic_region = True
                    view.run_command("auto_complete")
                    break
        if "sr:" in line:
            idx = line.index("sr:") + view.line(point).a + 3
            if idx == point:
                self.strategic_region = True
                view.run_command("auto_complete")
        # Subject Type
        for i in subject_type_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.subject_type = True
                    view.run_command("auto_complete")
                    break
        # Technologies
        for i in tech_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.tech = True
                    view.run_command("auto_complete")
                    break
        # Terrains
        for i in terrain_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.terrain = True
                    view.run_command("auto_complete")
                    break
        # State Regions
        for i in state_regions_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.state_region = True
                    view.run_command("auto_complete")
                    break
        if "s:" in line:
            idx = line.index("s:") + view.line(point).a + 2
            if idx == point:
                self.state_region = True
                view.run_command("auto_complete")
        # Country Scopes
        if "c:" in line:
            idx = line.index("c:") + view.line(point).a + 2
            if idx == point:
                self.countries = True
                view.run_command("auto_complete")
        # Country Ranks
        if "rank_value:" in line:
            idx = line.index("rank_value:") + view.line(point).a + 11
            if idx == point:
                self.country_ranks = True
                view.run_command("auto_complete")
        # Country Types
        for i in country_types:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.country_types = True
                    view.run_command("auto_complete")
                    break
        # Culture Graphics
        for i in culture_graphics:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.culture_graphics = True
                    view.run_command("auto_complete")
                    break
        # Named Colors
        for i in named_colors:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.named_colors = True
                    view.run_command("auto_complete")
                    break
        # Battle Conditions
        for i in battle_conditions:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.battle_conditions = True
                    view.run_command("auto_complete")
                    break
        # Commander Ranks
        for i in commander_ranks:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.commander_ranks = True
                    view.run_command("auto_complete")
                    break

        # Proposal Types
        for i in proposal_types_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.proposal_types = True
                    view.run_command("auto_complete")
                    break
        # Discrimination Traits
        for i in discrimination_traits_list:
            r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
            if r:
                y = 0
                idx = line.index(i) + view.line(point).a + len(i) + 2
                if r.groups()[0] == '"':
                    y = 2
                if idx == point or idx + y == point or idx + 1 == point:
                    self.discrimination_traits = True
                    view.run_command("auto_complete")
                    break

    def check_for_complex_completions(self, view, point):
        view_str = view.substr(sublime.Region(0, view.size()))

        for br in view.find_by_selector("meta.ig.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            if i.contains(point):
                self.ig = True
                view.run_command("auto_complete")

        for br in view.find_by_selector("meta.goods.simple.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            if i.contains(point):
                self.good = True
                view.run_command("auto_complete")

        for br in view.find_by_selector("meta.ideology.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            if i.contains(point):
                self.ideology = True
                view.run_command("auto_complete")

        for br in view.find_by_selector("meta.law.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            if i.contains(point):
                self.law = True
                view.run_command("auto_complete")

        for br in view.find_by_selector("meta.tech.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            if i.contains(point):
                self.tech = True
                view.run_command("auto_complete")

        for br in view.find_by_selector("meta.bg.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            s = view.substr(i)
            if "type = " in s:
                fpoint = (
                    s.index("type = ") + 7
                ) + i.a  # add 7 = amount of chars in "type = ", so cursor ends up at end of statement
                if fpoint == point:
                    self.show_bg = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.da.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            s = view.substr(i)
            if "type = " in s:
                fpoint = (view.substr(i).index("type = ") + 7) + i.a
                if fpoint == point:
                    self.diplo_action = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.dp.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            s = view.substr(i)
            if "type = " in s:
                fpoint = (view.substr(i).index("type = ") + 7) + i.a
                if fpoint == point:
                    self.diplo_play = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.je.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            s = view.substr(i)
            if "type = " in s:
                fpoint = (view.substr(i).index("type = ") + 7) + i.a
                if fpoint == point:
                    self.journal = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.mods.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            s = view.substr(i)
            if "name = " in s:
                fpoint = (view.substr(i).index("name = ") + 7) + i.a
                if fpoint == point:
                    self.modifier = True
                    view.run_command("auto_complete")

        for br in view.find_by_selector("meta.subjects.bracket"):
            i = sublime.Region(br.a, self.getIndex(view_str, br.a))
            s = view.substr(i)
            if "type = " in s:
                fpoint = (view.substr(i).index("type = ") + 7) + i.a
                if fpoint == point:
                    self.subject_type = True
                    view.run_command("auto_complete")

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

        if not settings.get("DisableVictoriaScriptingFeatures"):
            return

        self.simple_scope_match(view)
        # Only do when there is 1 selection, doens't make sense with multiple selections
        if len(view.sel()) == 1:
            self.check_for_simple_completions(view, view.sel()[0].a)
            self.check_for_complex_completions(view, view.sel()[0].a)


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
        out = re.findall("(title|desc|name|custom_tooltip|text|flavor)\s?=\s?(.+)", out)

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
    def __init__(self):
        self.view = None
        self.view_str = None

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

        if not settings.get("DisableVictoriaScriptingFeatures"):
            return

        self.view = view
        self.view_str = view.substr(sublime.Region(0, view.size()))

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
    def on_hover(sef, view, point, hover_zone):
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
# -    Open Included Shader File   -
# ----------------------------------


pos = -1
posa = -1
posb = -1
out_point = -1
out_view = ""
file = ""


class OpenPdxShaderHeaderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Command for href
        global out_point, out_view
        if self.check_scope(out_view, out_point):
            self.open_file(out_view)

    def check_scope(self, view, point):
        global pos, posa, posb, file

        scopesStr = view.scope_name(point)
        scopeList = scopesStr.split(" ")
        if scopeList[1] == "string.quoted.double.include.hlsl":
            posLine = view.line(point)
            posa = posLine.a + 2
            posb = posLine.b - 1
            pos = 1
            file = view.substr(sublime.Region(posa, posb))
            return True
        else:
            self.pos = -1
            return False

    def open_file(self, view):
        global pos, file
        if pos != -1:
            scopeRegion = view.extract_scope(pos)
            originalFilePath = file.replace("/", "\\")
            # Search order is from absolute path of launching file, list order of user paths, finally Unity project paths.
            basePath = ""
            curFile = view.file_name()
            if curFile is not None:
                basePath = view.file_name().rsplit("\\", 1)[0] + "\\"
            paths = [basePath]

            self.settingsBasePaths = settings.get("OpenHeaderBasePaths", [])
            settingsIncludePaths = settings.get("OpenHeaderIncludePaths", [])
            settingsPaths = []
            for index in range(0, len(settingsIncludePaths)):
                newSettingsPath = re.sub(
                    "(\$base_path)(\[)(\d+)(\])",
                    self.path_replace,
                    settingsIncludePaths[index],
                )
                paths.append(newSettingsPath)

            # Try to find paths expected relative to a Unity project's root folder.
            assetDir, embeddedPackagePaths, cachedPackagePaths = self.get_unity_paths(
                basePath
            )
            if assetDir:
                paths.append(assetDir)

            for path in paths:
                newPath = os.path.normpath(path + "\\" + originalFilePath)
                fileExists = os.path.isfile(newPath)
                if fileExists:
                    self.open_or_switch_to(newPath)
                    return

            targetPathParts = originalFilePath.split("\\")
            if len(targetPathParts) >= 3 and targetPathParts[0].lower() == "packages":
                packageName = targetPathParts[1]
                targetRelative = "\\".join(targetPathParts[2:])
                packagePaths = embeddedPackagePaths + cachedPackagePaths
                embeddedPackagePaths.extend(packagePaths)

                for packagePath in packagePaths:
                    if os.path.basename(packagePath).split("@")[0] == packageName:
                        targetFile = os.path.normpath(
                            os.path.join(packagePath, targetRelative)
                        )
                        if os.path.isfile(targetFile):
                            self.open_or_switch_to(targetFile)
                            return

                lastLength = -1
                currentDir = basePath
                while len(currentDir) != lastLength:
                    lastLength = len(currentDir)
                    currentDir = os.path.dirname(currentDir)
                    targetFile = os.path.normpath(
                        currentDir + "\\" + packageName + "\\" + targetRelative
                    )
                    targetFile = targetFile.replace("\\", "/")
                    if os.path.isfile(targetFile):
                        self.open_or_switch_to(targetFile)
                        return

    def path_replace(self, match_object):
        # Given the pattern of (\$base_path)(\[)(\d+)(\]), \d+ is group 3
        index = int(match_object.group(3))
        if index < len(self.settingsBasePaths):
            return self.settingsBasePaths[index]
        return "ERRORSTRING"

    def open_or_switch_to(self, targetFile):
        fileView = sublime.active_window().find_open_file(targetFile)
        if fileView is None:
            fileView = sublime.active_window().open_file(targetFile)
        sublime.active_window().focus_view(fileView)

    def get_unity_paths(self, basePath):
        lastLength = -1
        currentDir = basePath
        while len(currentDir) != lastLength:
            lastLength = len(currentDir)
            currentDir = os.path.dirname(currentDir)
            assetsDir = os.path.normpath(currentDir + "/Assets")
            packagesDir = os.path.normpath(currentDir + "/Packages")
            packageCacheDir = os.path.normpath(currentDir + "/Library/PackageCache")

            # If both Assets and Packages folders exist then assume it is the project's root, but don't rely on
            # Library/PackageCache folder existing in case it hasn't been generated yet.
            if os.path.isdir(assetsDir) and os.path.isdir(packagesDir):
                embeddedPackagePaths = [
                    packagesDir + "/" + p for p in next(os.walk(packagesDir))[1]
                ]
                cachedPackagePaths = []
                if os.path.isdir(packageCacheDir):
                    cachedPackagePaths = [
                        packageCacheDir + "/" + p
                        for p in next(os.walk(packageCacheDir))[1]
                    ]
                return (assetsDir, embeddedPackagePaths, cachedPackagePaths)

        return (None, [], [])


class HeaderHoverListener(sublime_plugin.EventListener):
    def on_hover(self, view, point, hover_zone):
        global out_point, out_view
        if settings.get("OpenHeaderEnabled") is False:
            return

        try:
            if view.syntax().name != "PdxShader":
                return
        except AttributeError:
            return

        out_point = point
        out_view = view
        scopesStr = view.scope_name(point)
        scopeList = scopesStr.split(" ")
        if scopeList[1] == "string.quoted.double.include.hlsl":
            self.show_hover_popup(view, point)

    def show_hover_popup(self, view, point):
        posLine = view.line(point)
        posa = posLine.a + 2
        posb = posLine.b - 1
        file = view.substr(sublime.Region(posa, posb))
        hoverBody = """
			<body id="vic-body">
				<style>%s</style>
				<h1>Header File</h1>
				<a href="subl:open_pdx_shader_header" title="If file does not open add path to package settings">Open %s</a>
			</body>
		""" % (
            css.default,
            file,
        )

        view.show_popup(
            hoverBody,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=502,
        )


# ----------------------------------
# -          If Def Utils          -
# ----------------------------------


PreprocessorBlockListScanDown = {"if", "ifdef", "ifndef"}

PreprocessorBlockListScanUp = {"endif"}

PreprocessorBlockListScanBoth = {"elif", "else"}


class IfDefMatchListener(sublime_plugin.EventListener):
    def on_hover(sef, view, point, hover_zone):
        if settings.get("IfDefMatchEnabled", True) is False:
            return
        if not view:
            return

        try:
            if view.syntax().name != "PdxShader":
                return
        except AttributeError:
            return

        def on_navigate(href):
            view.window().open_file(
                href, sublime.ENCODED_POSITION | sublime.FORCE_GROUP
            )

        def do_hover(view, point, startSection, endSection, seperator):
            hoverBody = """
				<body id=show-ifdefmatch>
					<style>
						%s
					</style>
					%s
					%s
					%s
				</body>
			""" % (
                css.default,
                startSection,
                seperator,
                endSection,
            )

            view.show_popup(
                hoverBody,
                flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                location=point,
                max_width=1024,
                on_navigate=on_navigate,
            )

        def FormatLocation(file, row, col):
            return "%s:%d:%d" % (file, row + 1, col)

        def FormatHover(category, href, hrefText):
            return '<h1>%s</h1><p><a href="%s">%s</a></p>' % (category, href, hrefText)

        def ScanDown(view, point):
            stackSize = 0
            offsetToNextLine = view.full_line(point).size()
            viewLength = view.size()
            while point + offsetToNextLine <= viewLength:
                newLine = view.full_line(point + offsetToNextLine)
                trimmedNewLineStart = view.find_by_class(
                    newLine.begin(), True, sublime.CLASS_WORD_START
                )
                newLineScopesStr = view.scope_name(trimmedNewLineStart)
                newLineScopeList = newLineScopesStr.split(" ")
                for newScope in newLineScopeList:
                    if newScope == "keyword.control.preprocessor.hlsl":
                        newLineWord = view.substr(newLine).lstrip()
                        newLineWordForMatch = newLineWord.lstrip("#")
                        newLineMatchArray = newLineWordForMatch.split()
                        if len(newLineMatchArray) != 0:
                            newLineWordForMatch = newLineMatchArray[0]
                        else:
                            break
                        if newLineWordForMatch in PreprocessorBlockListScanDown:
                            stackSize += 1
                        elif newLineWordForMatch in PreprocessorBlockListScanUp:
                            if stackSize == 0:
                                row, col = view.rowcol(newLine.begin())
                                return FormatHover(
                                    "Block End:",
                                    FormatLocation(view.file_name(), row, col),
                                    newLineWord.rstrip(),
                                )
                            else:
                                stackSize -= 1
                        break
                offsetToNextLine += newLine.size()

        def ScanUp(view, point):
            stackSize = 0
            row, col = view.rowcol(point)
            offsetToNextLine = col + 1
            while point - offsetToNextLine > 0:
                newLine = view.full_line(point - offsetToNextLine)
                trimmedNewLineStart = view.find_by_class(
                    newLine.begin(), True, sublime.CLASS_WORD_START
                )
                newLineScopesStr = view.scope_name(trimmedNewLineStart)
                newLineScopeList = newLineScopesStr.split(" ")
                for newScope in newLineScopeList:
                    if newScope == "keyword.control.preprocessor.hlsl":
                        newLineWord = view.substr(newLine).lstrip()
                        newLineWordForMatch = newLineWord.lstrip("#")
                        newLineMatchArray = newLineWordForMatch.split()
                        if len(newLineMatchArray) != 0:
                            newLineWordForMatch = newLineMatchArray[0]
                        else:
                            break
                        if newLineWordForMatch in PreprocessorBlockListScanUp:
                            stackSize += 1
                        elif newLineWordForMatch in PreprocessorBlockListScanDown:
                            if stackSize == 0:
                                row, col = view.rowcol(newLine.begin())
                                return FormatHover(
                                    "Block Start:",
                                    FormatLocation(view.file_name(), row, col),
                                    newLineWord.rstrip(),
                                )
                            else:
                                stackSize -= 1
                        break
                offsetToNextLine += newLine.size()

        startSection = ""
        endSection = ""
        seperator = ""
        scopesStr = view.scope_name(point)
        scopeList = scopesStr.split(" ")
        for scope in scopeList:
            if scope == "keyword.control.preprocessor.hlsl":
                posWord = view.word(point)
                ifdefWord = view.substr(posWord)
                if ifdefWord in PreprocessorBlockListScanDown:
                    endSection = ScanDown(view, point)
                    break
                elif ifdefWord in PreprocessorBlockListScanUp:
                    startSection = ScanUp(view, point)
                    break
                elif ifdefWord in PreprocessorBlockListScanBoth:
                    endSection = ScanDown(view, point)
                    startSection = ScanUp(view, point)
                    seperator = "<br>"
                    break
        if (len(startSection) != 0) or (len(endSection) != 0):
            do_hover(view, point, startSection, endSection, seperator)


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
            and not settings.get("DisableVictoriaScriptingFeatures")
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

        if gui_templates.contains(word):
            self.show_gui_popup(
                view, point, word, gui_templates.access(word), "Gui Template"
            )

        if gui_types.contains(word):
            self.show_gui_popup(view, point, word, gui_types.access(word), "Gui Type")

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

        # Check if currently hovered word is equal to any game object and show goto definition popup if found
        if ai_strats.contains(word):
            self.show_popup_default(
                view, point, word, ai_strats.access(word), "Ai Strategies"
            )

        if bgs.contains(word):
            self.show_popup_default(
                view, point, word, bgs.access(word), "Building Group"
            )

        if buildings.contains(word):
            self.show_popup_default(
                view, point, word, buildings.access(word), "Building"
            )

        if char_traits.contains(word):
            self.show_popup_default(
                view, point, word, char_traits.access(word), "Character Trait"
            )

        if cultures.contains(word):
            self.show_popup_default(view, point, word, cultures.access(word), "Culture")

        if decrees.contains(word):
            self.show_popup_default(view, point, word, decrees.access(word), "Decree")

        if diplo_actions.contains(word):
            self.show_popup_default(
                view, point, word, diplo_actions.access(word), "Diplomatic Action"
            )

        if diplo_plays.contains(word):
            self.show_popup_default(
                view, point, word, diplo_plays.access(word), "Diplomatic Play"
            )

        if game_rules.contains(word):
            self.show_popup_default(
                view, point, word, game_rules.access(word), "Game Rule"
            )

        if goods.contains(word):
            self.show_popup_default(view, point, word, goods.access(word), "Trade Good")

        if gov_types.contains(word):
            self.show_popup_default(
                view, point, word, gov_types.access(word), "Government Type"
            )

        if ideologies.contains(word):
            self.show_popup_default(
                view, point, word, ideologies.access(word), "Ideology"
            )

        if institutions.contains(word):
            self.show_popup_default(
                view, point, word, institutions.access(word), "Institution"
            )

        if ig_traits.contains(word):
            self.show_popup_default(
                view, point, word, ig_traits.access(word), "Interest Group Traits"
            )

        if igs.contains(word):
            self.show_popup_default(
                view, point, word, igs.access(word), "Interest Group"
            )

        if jes.contains(word):
            self.show_popup_default(
                view, point, word, jes.access(word), "Journal Entry"
            )

        if law_groups.contains(word):
            self.show_popup_default(
                view, point, word, law_groups.access(word), "Law Group"
            )

        if laws.contains(word):
            self.show_popup_default(view, point, word, laws.access(word), "Law")

        if mods.contains(word):
            self.show_popup_default(view, point, word, mods.access(word), "Modifier")

        if parties.contains(word):
            self.show_popup_default(view, point, word, parties.access(word), "Party")

        if pop_needs.contains(word):
            self.show_popup_default(
                view, point, word, pop_needs.access(word), "Pop Need"
            )

        if pop_types.contains(word):
            self.show_popup_default(
                view, point, word, pop_types.access(word), "Pop Type"
            )

        if pm_groups.contains(word):
            self.show_popup_default(
                view, point, word, pm_groups.access(word), "Production Method Group"
            )

        if pms.contains(word):
            self.show_popup_default(
                view, point, word, pms.access(word), "Production Method"
            )

        if religions.contains(word):
            self.show_popup_default(
                view, point, word, religions.access(word), "Religion"
            )

        if script_values.contains(word):
            self.show_popup_default(
                view, point, word, script_values.access(word), "Script Value"
            )

        if scripted_effects.contains(word):
            self.show_popup_default(
                view, point, word, scripted_effects.access(word), "Scripted Effect"
            )

        if scripted_modifiers.contains(word):
            self.show_popup_default(
                view, point, word, scripted_modifiers.access(word), "Scripted Modifer"
            )

        if scripted_triggers.contains(word):
            self.show_popup_default(
                view, point, word, scripted_triggers.access(word), "Scripted Trigger"
            )

        if state_traits.contains(word):
            self.show_popup_default(
                view, point, word, state_traits.access(word), "State Trait"
            )

        if strategic_regions.contains(word):
            self.show_popup_default(
                view, point, word, strategic_regions.access(word), "Strategic Region"
            )

        if subject_types.contains(word):
            self.show_popup_default(
                view, point, word, subject_types.access(word), "Subject Types"
            )

        if technologies.contains(word):
            self.show_popup_default(
                view, point, word, technologies.access(word), "Technology"
            )

        if terrains.contains(word):
            self.show_popup_default(view, point, word, terrains.access(word), "Terrain")

        if state_regions.contains(word):
            self.show_popup_default(
                view, point, word, state_regions.access(word), "State Region"
            )

        if countries.contains(word):
            self.show_popup_default(
                view, point, word, countries.access(word), "Country"
            )

        if country_ranks.contains(word):
            self.show_popup_default(
                view, point, word, country_ranks.access(word), "Country Rank"
            )

        if country_types.contains(word):
            self.show_popup_default(
                view, point, word, country_types.access(word), "Country Type"
            )

        if culture_graphics.contains(word):
            self.show_popup_default(
                view, point, word, culture_graphics.access(word), "Culture Graphic"
            )

        if named_colors.contains(word):
            self.show_popup_named_color(
                view, point, word, named_colors.access(word), "Named Color"
            )

        if battle_conditions.contains(word):
            self.show_popup_default(
                view, point, word, battle_conditions.access(word), "Battle Condition"
            )

        if commander_ranks.contains(word):
            self.show_popup_default(
                view, point, word, commander_ranks.access(word), "Commander Rank"
            )

        if proposal_types.contains(word):
            self.show_popup_default(
                view, point, word, proposal_types.access(word), "Proposal Type"
            )

        if discrimination_traits.contains(word):
            self.show_popup_default(
                view,
                point,
                word,
                discrimination_traits.access(word),
                "Discrimination Trait",
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
                    % (goto_url, shortname, line, shortname, line)
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
                    % (goto_url, shortname, line, shortname, line)
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
        except Exception as e:
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
        if x:
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
                '[A-Za-z_][A-Za-z_0-9]*\s?=\s?"?/?(gfx)?', line_region.a
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
        word_position_b = posLine.b - 6
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
        video_file_path = False
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


# def get_keys(gui_functions):
# 	keys = dict()
# 	for i in gui_functions:
# 		keys[i.name] = i.name
# 	return keys

# datatypefile = "C:\\Users\\demen\\Documents\\Paradox Interactive\\Victoria 3\\logs\\data_types\\data_types_common.txt"

# with open(datatypefile, "r") as file:
# 	file_lines = file.read()

# lines = file_lines.split("-----------------------")
# lines = [x for x in lines if x.strip()]

# functions = []
# type_definitions = []

# for i in lines:
# 	description = ""
# 	definition_type = ""
# 	return_type = ""
# 	x = i.strip().split("\n")
# 	function_name = x[0].split("(")[0]
# 	if len(function_name) == 2:
# 		# Type definition
# 		definition_type = function_name[1]
# 		type_definitions.append(function_name[0])
# 	if len(function_name) == 3:
# 		# Function without description
# 		definition_type = function_name[1]
# 		return_type = function_name[2]
# 	if len(function_name) == 4:
# 		# Function with description
# 		description = function_name[1]
# 		definition_type = function_name[2]
# 		return_type = function_name[3]

# 	gui_function = GuiFunction(datatypefile, function_name, 0, definition_type, return_type, description)
# 	functions.append(gui_function)

# with open("C:\\Users\\demen\\Documents\\Paradox Interactive\\Victoria 3\\logs\\data_types\\data_types_common.txt", "r") as file:
# 	file_lines = file.readlines()
# 	for count, i in enumerate(file_lines):
# 		name = i.strip()
# 		keys_dict = get_keys(functions)
# 		if name in keys_dict:
# 			for j, fun in enumerate(functions):
# 				if fun.name == name:
# 					functions[j].line = count + 1

# print(functions[0].name)

# class GuiFunction:
# 	def __init__(self, file, name, line, def_type, return_type=None, description=None):
# 		self.file = file
# 		self.name = name
# 		self.line = line
# 		self.def_type = def_type
# 		self.return_type = return_type
# 		self.description = description
