# Victoria 3 Game Object Class implementations

import os
import re
from colorsys import hsv_to_rgb
from typing import Union

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
    v3_files_path = str(v3_files_path)
    gui_files_path = str(gui_files_path)


# Gui Class implementations
class GuiType(GameObjectBase):
    def __init__(self):
        super().__init__(gui_mod_files, gui_files_path)
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
class AiStrategy(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}ai_strategies")


class BuildingGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}building_groups")


class Building(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}buildings")


class CharacterTrait(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}character_traits")


class Culture(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}cultures")


class Decree(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}decrees")


class DiplomaticAction(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}diplomatic_actions")


class DiplomaticPlay(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}diplomatic_plays")


class GameRules(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}game_rules")


class Goods(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}goods")


class GovernmentType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}government_types")


class Institutions(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}institutions")


class Ideology(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}ideologies")


class InterestGroupTrait(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}interest_group_traits")


class InterestGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}interest_groups")


class JournalEntry(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}journal_entries")


class LawGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}law_groups")


class Law(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}laws")


class Modifier(GameObjectBase):
    def __init__(self):
        super().__init__(
            v3_mod_files, v3_files_path, ignored_files=["00_static_modifiers.txt"]
        )
        self.get_data(f"common{os.sep}modifiers")


class Party(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}parties")


class PopNeed(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}pop_needs")


class PopType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}pop_types")


class ProductionMethodGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}production_method_groups")


class ProductionMethod(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}production_methods")


class Religion(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}religions")


class ScriptValue(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}script_values")


class ScriptedEffect(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}scripted_effects")


class ScriptedModifier(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}scripted_modifiers")


class ScriptedTrigger(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}scripted_triggers")


class StateTrait(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}state_traits")


class StrategicRegion(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}strategic_regions")


class SubjectType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}subject_types")


class Technology(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}technology")


class Terrain(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}terrain")


class StateRegion(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"map_data{os.sep}state_regions")


class Country(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}country_definitions")


class CountryRank(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}country_ranks")


class CountryType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}country_types")


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
        if isinstance(other, NamedColor):
            return self.key == other.key
        elif isinstance(other, str):
            return self.key == other
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, NamedColor):
            return self.key < other.key
        elif isinstance(other, str):
            return self.key < other
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, NamedColor):
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


class NamedColor(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path, level=1)
        self.get_data(f"common{os.sep}named_colors")

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


class BattleCondition(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}battle_conditions")


class CommanderRank(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}commander_ranks")


class CultureGraphics(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}culture_graphics")


class ProposalType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}proposal_types")


class DiscriminationTrait(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}discrimination_traits")


class ModifierType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}modifier_types")


class CombatUnitGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}combat_unit_groups")


class CombatUnitType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}combat_unit_types")


class CommanderOrder(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}commander_orders")


class CompanyType(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}company_types")


class MobilizationOption(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}mobilization_options")


class CustomLoc(GameObjectBase):
    def __init__(self):
        super().__init__(
            v3_mod_files,
            v3_files_path,
            ignored_files=[
                "99_ru_custom_loc.txt",
                "99_de_custom_loc.txt",
                "99_pl_custom_loc.txt",
                "99_fr_custom_loc.txt",
                "99_es_custom_loc.txt",
                "99_br_custom_loc.txt",
            ],
        )
        self.get_data(f"common{os.sep}customizable_localization")


class ScriptedGui(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}scripted_guis")


Victoria3Object = Union[
    GameObjectBase,
    AiStrategy,
    BattleCondition,
    Building,
    BuildingGroup,
    CharacterTrait,
    CombatUnitGroup,
    CombatUnitType,
    CommanderOrder,
    CommanderRank,
    CompanyType,
    Country,
    CountryRank,
    CountryType,
    Culture,
    CultureGraphics,
    CustomLoc,
    Decree,
    DiplomaticAction,
    DiplomaticPlay,
    DiscriminationTrait,
    GameRules,
    Goods,
    GovernmentType,
    GuiTemplate,
    GuiType,
    Ideology,
    Institutions,
    InterestGroup,
    InterestGroupTrait,
    JournalEntry,
    Law,
    LawGroup,
    MobilizationOption,
    Modifier,
    ModifierType,
    NamedColor,
    Party,
    PopNeed,
    PopType,
    ProductionMethod,
    ProductionMethodGroup,
    ProposalType,
    Religion,
    ScriptedEffect,
    ScriptedGui,
    ScriptedModifier,
    ScriptedTrigger,
    ScriptValue,
    StateRegion,
    StateTrait,
    StrategicRegion,
    SubjectType,
    Technology,
    Terrain,
]
