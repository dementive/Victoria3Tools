from .v3_objects import *
from JominiTools.src.jomini_objects import *
from JominiTools.src import JominiGameObjectManager, GameObjectData


class GameObjectManager(JominiGameObjectManager):
    def __init__(self):
        self.ai_strats = GameObjectData(
            "ai_strats", AiStrategy, f"common{os.sep}ai_strategies"
        )
        self.alert_group = GameObjectData(
            "alert_group", AlertGroup, f"common{os.sep}alert_groups"
        )
        self.battle_conditions = GameObjectData(
            "battle_conditions", BattleCondition, f"common{os.sep}battle_conditions"
        )
        self.bgs = GameObjectData(
            "bgs", BuildingGroup, f"common{os.sep}building_groups"
        )
        self.buildings = GameObjectData(
            "buildings", Building, f"common{os.sep}buildings"
        )
        self.canals = GameObjectData("canals", Canal, f"common{os.sep}canals")
        self.char_template = GameObjectData(
            "char_template", CharacterTemplate, f"common{os.sep}character_templates"
        )
        self.char_traits = GameObjectData(
            "char_traits", CharacterTrait, f"common{os.sep}character_traits"
        )
        self.combat_unit_group = GameObjectData(
            "combat_unit_group", CombatUnitGroup, f"common{os.sep}combat_unit_groups"
        )
        self.combat_unit_type = GameObjectData(
            "combat_unit_type", CombatUnitType, f"common{os.sep}combat_unit_types"
        )
        self.commander_orders = GameObjectData(
            "commander_orders", CommanderOrder, f"common{os.sep}commander_orders"
        )
        self.commander_ranks = GameObjectData(
            "commander_ranks", CommanderRank, f"common{os.sep}commander_ranks"
        )
        self.companies = GameObjectData(
            "companies", CompanyType, f"common{os.sep}company_types"
        )
        self.countries = GameObjectData(
            "countries", Country, f"common{os.sep}country_definitions"
        )
        self.country_ranks = GameObjectData(
            "country_ranks", CountryRank, f"common{os.sep}country_ranks"
        )
        self.country_types = GameObjectData(
            "country_types", CountryType, f"common{os.sep}country_types"
        )
        self.culture_graphics = GameObjectData(
            "culture_graphics", CultureGraphics, f"common{os.sep}culture_graphics"
        )
        self.cultures = GameObjectData("cultures", Culture, f"common{os.sep}cultures")
        self.custom_loc = GameObjectData(
            "custom_loc", CustomLoc, f"common{os.sep}customizable_localization"
        )
        self.decrees = GameObjectData("decrees", Decree, f"common{os.sep}decrees")
        self.diplo_actions = GameObjectData(
            "diplo_actions", DiplomaticAction, f"common{os.sep}diplomatic_actions"
        )
        self.diplo_cat = GameObjectData(
            "diplo_cat", DiplomaticCatalyst, f"common{os.sep}diplomatic_catalysts"
        )
        self.diplo_plays = GameObjectData(
            "diplo_plays", DiplomaticPlay, f"common{os.sep}diplomatic_plays"
        )
        self.discrimination_traits = GameObjectData(
            "discrimination_traits",
            DiscriminationTrait,
            f"common{os.sep}discrimination_traits",
        )
        self.game_rules = GameObjectData(
            "game_rules", GameRules, f"common{os.sep}game_rules"
        )
        self.goods = GameObjectData("goods", Goods, f"common{os.sep}goods")
        self.gov_types = GameObjectData(
            "gov_types", GovernmentType, f"common{os.sep}government_types"
        )
        self.gui_templates = GameObjectData("gui_templates", GuiTemplate, "gui")
        self.gui_types = GameObjectData("gui_types", GuiType, "gui")
        self.ideologies = GameObjectData(
            "ideologies", Ideology, f"common{os.sep}ideologies"
        )
        self.ig_traits = GameObjectData(
            "ig_traits", InterestGroupTrait, f"common{os.sep}interest_group_traits"
        )
        self.igs = GameObjectData(
            "igs", InterestGroup, f"common{os.sep}interest_groups"
        )
        self.institutions = GameObjectData(
            "institutions", Institutions, f"common{os.sep}institutions"
        )
        self.jes = GameObjectData("jes", JournalEntry, f"common{os.sep}journal_entries")
        self.law_groups = GameObjectData(
            "law_groups", LawGroup, f"common{os.sep}law_groups"
        )
        self.laws = GameObjectData("laws", Law, f"common{os.sep}laws")
        self.mobilization_options = GameObjectData(
            "mobilization_options",
            MobilizationOption,
            f"common{os.sep}mobilization_options",
        )
        self.modifier_types = GameObjectData(
            "modifier_types", ModifierType, f"common{os.sep}modifier_types"
        )
        self.mods = GameObjectData("mods", Modifier, f"common{os.sep}modifiers")
        self.named_colors = GameObjectData(
            "named_colors", NamedColor, f"common{os.sep}named_colors"
        )
        self.parties = GameObjectData("parties", Party, f"common{os.sep}parties")
        self.pm_groups = GameObjectData(
            "pm_groups",
            ProductionMethodGroup,
            f"common{os.sep}production_method_groups",
        )
        self.pms = GameObjectData(
            "pms", ProductionMethod, f"common{os.sep}production_methods"
        )
        self.pop_needs = GameObjectData(
            "pop_needs", PopNeed, f"common{os.sep}pop_needs"
        )
        self.pop_types = GameObjectData(
            "pop_types", PopType, f"common{os.sep}pop_types"
        )
        self.proposal_types = GameObjectData(
            "proposal_types", ProposalType, f"common{os.sep}proposal_types"
        )
        self.religions = GameObjectData(
            "religions", Religion, f"common{os.sep}religions"
        )
        self.script_values = GameObjectData(
            "script_values", ScriptValue, f"common{os.sep}script_values"
        )
        self.scripted_effects = GameObjectData(
            "scripted_effects", ScriptedEffect, f"common{os.sep}scripted_effects"
        )
        self.scripted_gui = GameObjectData(
            "scripted_gui", ScriptedGui, f"common{os.sep}scripted_guis"
        )
        self.scripted_modifiers = GameObjectData(
            "scripted_modifiers", ScriptedModifier, f"common{os.sep}scripted_modifiers"
        )
        self.scripted_triggers = GameObjectData(
            "scripted_triggers", ScriptedTrigger, f"common{os.sep}scripted_triggers"
        )
        self.state_regions = GameObjectData(
            "state_regions", StateRegion, f"map_data{os.sep}state_regions"
        )
        self.state_traits = GameObjectData(
            "state_traits", StateTrait, f"common{os.sep}state_traits"
        )
        self.strategic_regions = GameObjectData(
            "strategic_regions", StrategicRegion, f"common{os.sep}strategic_regions"
        )
        self.subject_types = GameObjectData(
            "subject_types", SubjectType, f"common{os.sep}subject_types"
        )
        self.technologies = GameObjectData(
            "technologies", Technology, f"common{os.sep}technology"
        )
        self.terrain_label = GameObjectData(
            "terrain_label", TerrainLabel, f"common{os.sep}labels"
        )
        self.terrains = GameObjectData("terrains", Terrain, f"common{os.sep}terrain")
        self.messages = GameObjectData("messages", Message, f"common{os.sep}messages")
        self.objectives = GameObjectData(
            "objectives", Objective, f"common{os.sep}objectives"
        )
        self.objective_subgoal = GameObjectData(
            "objective_subgoal", ObjectiveSubgoal, f"common{os.sep}objective_subgoals"
        )
        self.political_lobby = GameObjectData(
            "political_lobby", PoliticalLobby, f"common{os.sep}political_lobbies"
        )
        self.political_lobby_appeasement = GameObjectData(
            "political_lobby_appeasement",
            PoliticalLobbyAppeasement,
            f"common{os.sep}political_lobby_appeasement",
        )
        self.pb_identity = GameObjectData(
            "pb_identity", PowerBlocIdentity, f"common{os.sep}power_bloc_identities"
        )
        self.pb_principle_group = GameObjectData(
            "pb_principle_group",
            PowerBlocPrincipleGroup,
            f"common{os.sep}power_bloc_principle_groups",
        )
        self.pb_principle = GameObjectData(
            "pb_principle", PowerBlocPrinciple, f"common{os.sep}power_bloc_principles"
        )
        self.scripted_progress_bar = GameObjectData(
            "scripted_progress_bar",
            ScriptedProgressBar,
            f"common{os.sep}scripted_progress_bars",
        )
