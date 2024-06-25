# Victoria 3 Game Object Class implementations

import os
from typing import Union

import sublime

from JominiTools.src import GameObjectBase
from JominiTools.src.jomini_objects import JominiObject

v3_files_path = ""
v3_mod_files = []


def plugin_loaded():
    global settings, v3_files_path, v3_mod_files
    settings = sublime.load_settings("Victoria.sublime-settings")
    v3_files_path = settings.get("GameFilesPath")
    v3_mod_files = settings.get("PathsToModFiles")
    v3_files_path = str(v3_files_path)


# Victoria 3 Game Object Class implementations
class AiStrategy(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}ai_strategies")


class AlertGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}alert_groups")


class BattleCondition(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}battle_conditions")


class BuildingGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}building_groups")


class Building(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}buildings")


class Canal(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}canals")


class CharacterTrait(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}character_traits")


class CharacterTemplate(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}character_templates")


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
            v3_mod_files, v3_files_path, ignored_files=["00_code_static_modifiers.txt"]
        )
        self.get_data(f"common{os.sep}static_modifiers")


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
        self.get_data(f"common{os.sep}modifier_type_definitions")


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


class DiplomaticCatalyst(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}diplomatic_catalysts")


class TerrainLabel(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}labels")


class MobilizationOption(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}mobilization_options")


class Message(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}messages")


class Objective(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}objectives")


class ObjectiveSubgoal(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}objective_subgoals")


class PoliticalLobby(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}political_lobbies")


class PoliticalLobbyAppeasement(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}political_lobby_appeasement")


class PowerBlocIdentity(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}power_bloc_identities")


class PowerBlocPrincipleGroup(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}power_bloc_principle_groups")


class PowerBlocPrinciple(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}power_bloc_principles")


class ScriptedProgressBar(GameObjectBase):
    def __init__(self):
        super().__init__(v3_mod_files, v3_files_path)
        self.get_data(f"common{os.sep}scripted_progress_bars")


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


Victoria3Object = Union[
    GameObjectBase,
    JominiObject,
    AiStrategy,
    AlertGroup,
    BattleCondition,
    Building,
    BuildingGroup,
    Canal,
    CharacterTemplate,
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
    DiplomaticCatalyst,
    DiplomaticPlay,
    DiscriminationTrait,
    GameRules,
    Goods,
    GovernmentType,
    Ideology,
    Institutions,
    InterestGroup,
    InterestGroupTrait,
    JournalEntry,
    Law,
    LawGroup,
    Message,
    MobilizationOption,
    Modifier,
    ModifierType,
    Objective,
    ObjectiveSubgoal,
    Party,
    PoliticalLobby,
    PoliticalLobbyAppeasement,
    PopNeed,
    PopType,
    PowerBlocIdentity,
    PowerBlocPrinciple,
    PowerBlocPrincipleGroup,
    ProductionMethod,
    ProductionMethodGroup,
    ProposalType,
    Religion,
    ScriptedProgressBar,
    StateRegion,
    StateTrait,
    StrategicRegion,
    SubjectType,
    Technology,
    Terrain,
    TerrainLabel,
]
