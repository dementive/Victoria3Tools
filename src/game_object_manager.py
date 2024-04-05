from typing import Any, Set, Tuple

from .v3_objects import *


class GameObjectData:
    def __init__(self, name: str, obj: type, path: str):
        self.name = name
        self.obj = obj
        self.path = path


class GameObjectManager:
    def __init__(self):
        self.ai_strats = GameObjectData(
            "ai_strats", AiStrategy, "common\\ai_strategies"
        )
        self.battle_conditions = GameObjectData(
            "battle_conditions", BattleCondition, "common\\battle_conditions"
        )
        self.bgs = GameObjectData("bgs", BuildingGroup, "common\\building_groups")
        self.buildings = GameObjectData("buildings", Building, "common\\buildings")
        self.char_traits = GameObjectData(
            "char_traits", CharacterTrait, "common\\character_traits"
        )
        self.combat_unit_group = GameObjectData(
            "combat_unit_group", CombatUnitGroup, "common\\combat_unit_groups"
        )
        self.combat_unit_type = GameObjectData(
            "combat_unit_type", CombatUnitType, "common\\combat_unit_types"
        )
        self.commander_orders = GameObjectData(
            "commander_orders", CommanderOrder, "common\\commander_orders"
        )
        self.commander_ranks = GameObjectData(
            "commander_ranks", CommanderRank, "common\\commander_ranks"
        )
        self.companies = GameObjectData(
            "companies", CompanyType, "common\\company_types"
        )
        self.countries = GameObjectData(
            "countries", Country, "common\\country_definitions"
        )
        self.country_ranks = GameObjectData(
            "country_ranks", CountryRank, "common\\country_ranks"
        )
        self.country_types = GameObjectData(
            "country_types", CountryType, "common\\country_types"
        )
        self.culture_graphics = GameObjectData(
            "culture_graphics", CultureGraphics, "common\\culture_graphics"
        )
        self.cultures = GameObjectData("cultures", Culture, "common\\cultures")
        self.custom_loc = GameObjectData(
            "custom_loc", CustomLoc, "common\\customizable_localization"
        )
        self.decrees = GameObjectData("decrees", Decree, "common\\decrees")
        self.diplo_actions = GameObjectData(
            "diplo_actions", DiplomaticAction, "common\\diplomatic_actions"
        )
        self.diplo_plays = GameObjectData(
            "diplo_plays", DiplomaticPlay, "common\\diplomatic_plays"
        )
        self.discrimination_traits = GameObjectData(
            "discrimination_traits",
            DiscriminationTrait,
            "common\\discrimination_traits",
        )
        self.game_rules = GameObjectData("game_rules", GameRules, "common\\game_rules")
        self.goods = GameObjectData("goods", Goods, "common\\goods")
        self.gov_types = GameObjectData(
            "gov_types", GovernmentType, "common\\government_types"
        )
        self.gui_templates = GameObjectData("gui_templates", GuiTemplate, "gui")
        self.gui_types = GameObjectData("gui_types", GuiType, "gui")
        self.ideologies = GameObjectData("ideologies", Ideology, "common\\ideologies")
        self.ig_traits = GameObjectData(
            "ig_traits", InterestGroupTrait, "common\\interest_group_traits"
        )
        self.igs = GameObjectData("igs", InterestGroup, "common\\interest_groups")
        self.institutions = GameObjectData(
            "institutions", Institutions, "common\\institutions"
        )
        self.jes = GameObjectData("jes", JournalEntry, "common\\journal_entries")
        self.law_groups = GameObjectData("law_groups", LawGroup, "common\\law_groups")
        self.laws = GameObjectData("laws", Law, "common\\laws")
        self.mobilization_options = GameObjectData(
            "mobilization_options", MobilizationOption, "common\\mobilization_options"
        )
        self.modifier_types = GameObjectData(
            "modifier_types", ModifierType, "common\\modifier_types"
        )
        self.mods = GameObjectData("mods", Modifier, "common\\modifiers")
        self.named_colors = GameObjectData(
            "named_colors", NamedColor, "common\\named_colors"
        )
        self.parties = GameObjectData("parties", Party, "common\\parties")
        self.pm_groups = GameObjectData(
            "pm_groups", ProductionMethodGroup, "common\\production_method_groups"
        )
        self.pms = GameObjectData("pms", ProductionMethod, "common\\production_methods")
        self.pop_needs = GameObjectData("pop_needs", PopNeed, "common\\pop_needs")
        self.pop_types = GameObjectData("pop_types", PopType, "common\\pop_types")
        self.proposal_types = GameObjectData(
            "proposal_types", ProposalType, "common\\proposal_types"
        )
        self.religions = GameObjectData("religions", Religion, "common\\religions")
        self.script_values = GameObjectData(
            "script_values", ScriptValue, "common\\script_values"
        )
        self.scripted_effects = GameObjectData(
            "scripted_effects", ScriptedEffect, "common\\scripted_effects"
        )
        self.scripted_gui = GameObjectData(
            "scripted_gui", ScriptedGui, "common\\scripted_guis"
        )
        self.scripted_modifiers = GameObjectData(
            "scripted_modifiers", ScriptedModifier, "common\\scripted_modifiers"
        )
        self.scripted_triggers = GameObjectData(
            "scripted_triggers", ScriptedTrigger, "common\\scripted_triggers"
        )
        self.state_regions = GameObjectData(
            "state_regions", StateRegion, "map_data\\state_regions"
        )
        self.state_traits = GameObjectData(
            "state_traits", StateTrait, "common\\state_traits"
        )
        self.strategic_regions = GameObjectData(
            "strategic_regions", StrategicRegion, "common\\strategic_regions"
        )
        self.subject_types = GameObjectData(
            "subject_types", SubjectType, "common\\subject_types"
        )
        self.technologies = GameObjectData(
            "technologies", Technology, "common\\technology"
        )
        self.terrains = GameObjectData("terrains", Terrain, "common\\terrain")

    def __iter__(self):
        for attr in self.__dict__:
            yield getattr(self, attr)

    def get_objects(self) -> Set[GameObjectData]:
        objects = set()
        for i in self:
            objects.add(i)
        return objects
