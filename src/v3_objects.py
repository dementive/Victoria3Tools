# Victoria 3 Game Object Class implementations

import os
import re
from colorsys import hsv_to_rgb

import sublime

from .jomini import GameObjectBase, PdxScriptObject, PdxScriptObjectType

v3_files_path = ""
v3_mod_files = []
gui_files_path = ""
gui_mod_files = []


def plugin_loaded():
    global settings, v3_files_path, v3_mod_files, gui_files_path, gui_mod_files
    settings = sublime.load_settings("Victoria Syntax.sublime-settings")
    v3_files_path = settings.get("Victoria3FilesPath")
    v3_mod_files = settings.get("PathsToModFiles")
    gui_files_path = settings.get("GuiBaseGamePath")
    gui_mod_files = settings.get("PathsToGuiModFiles")


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
                                r"type\s([A-Za-z_][A-Za-z_0-9]*)\s?=", line
                            )
                            if found_item and found_item.groups()[0]:
                                found_item = found_item.groups()[0]
                                obj_list.append(
                                    PdxScriptObject(found_item, file_path, i + 1)
                                )
        return PdxScriptObjectType(obj_list)

    def should_read(self, x: str) -> bool:
        # Check if a line should be read
        out = re.search(r"type\s[A-Za-z_][A-Za-z_0-9]*\s?=", x)
        return True if out else False


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
                                r"template\s([A-Za-z_][A-Za-z_0-9]*)", line
                            )
                            if found_item and found_item.groups()[0]:
                                found_item = found_item.groups()[0]
                                obj_list.append(
                                    PdxScriptObject(found_item, file_path, i + 1)
                                )
        return PdxScriptObjectType(obj_list)

    def should_read(self, x: str) -> bool:
        # Check if a line should be read
        out = re.search(r"template\s[A-Za-z_][A-Za-z_0-9]*", x)
        return True if out else False


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
        try:
            obj_list.append(
                PdxColorObject(i, objects[i][0], objects[i][1], objects[i][2])
            )
        except IndexError:
            pass
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
        out = re.search(r"([A-Za-z_][A-Za-z_0-9]*)\s*=", x)
        return True if out else False


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


class V3ModifierType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\modifier_types")


class V3CombatUnitGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\combat_unit_groups")


class V3CombatUnitType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\combat_unit_types")


class V3CommanderOrder(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\commander_orders")


class V3CompanyType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\company_types")


class V3MobilizationOption(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data("common\\mobilization_options")
