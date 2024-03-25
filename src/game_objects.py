"""
Code related to loading, saving, and caching vic3 game objects
"""

import sublime
import os
import sys
import hashlib

parent_directory = os.path.abspath("..")
sys.path.append(parent_directory)

from Victoria3Tools.object_cache import GameObjectCache
from .jomini import dict_to_game_object as make_object
from .utils import get_default_game_objects


def check_mod_for_changes(v3_mod_files):
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
        for dirpath, dirnames, filenames in os.walk(path):
            mod_files = [
                x for x in filenames if x.endswith(".txt") or x.endswith(".gui")
            ]
            if mod_files:
                for i, j in enumerate(mod_files):
                    full_path = dirpath + "/" + mod_files[i]
                    stats_dict[full_path] = os.stat(full_path).st_mtime
        stats_string = str()
        for i in stats_dict:
            value = stats_dict[i]
            stats_string += f"{mod_name}{value}"

        with open(mod_cache_path, "a") as f:
            f.write(hashlib.sha256(stats_string.encode()).hexdigest())
            f.write("\n")

    with open(mod_cache_path, "r") as f:
        # Save written mod classes
        new_mod_cache = "".join(f.readlines())

    return True if mod_cache != new_mod_cache else False


def cache_all_objects(game_objects):
    # Write all generated objects to cache
    path = sublime.packages_path() + f"/Victoria3Tools/object_cache.py"
    with open(path, "w") as f:
        f.write("class GameObjectCache:\n\tdef __init__(self):")
        for i in game_objects:
            f.write(f"\n\t\tself.{i} = {game_objects[i].to_json()}")


def get_gui_objects_from_cache():
    object_cache = GameObjectCache()
    game_objects = get_default_game_objects()

    game_objects["gui_types"] = make_object(object_cache.gui_types)
    game_objects["gui_templates"] = make_object(object_cache.gui_templates)

    return game_objects


def get_objects_from_cache():
    object_cache = GameObjectCache()
    game_objects = get_default_game_objects()

    for i in game_objects:
        game_objects[i] = make_object(getattr(object_cache, i))

    return game_objects


def handle_image_cache(settings):
    cache_size_limit = settings.get("MaxImageCacheSize")
    cache = sublime.packages_path() + "/Victoria3Tools/Convert DDS/cache/"
    cache_files = [x for x in os.listdir(cache) if x.endswith(".png")]
    if len(cache_files) > cache_size_limit:
        for i in cache_files:
            os.remove(os.path.join(cache, i))
        sublime.status_message("Cleared Image Cache")


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


def write_data_to_syntax(game_objects):
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
        game_objects["modifier_types"].keys(),
        "Modifier Type",
        "string.modifier.type",
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
        game_objects["mobilization_options"].keys(),
        "Mobilization Options",
        "entity.name.mobilization.option",
    )
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
        game_objects["commander_orders"].keys(),
        "Commander Orders",
        "entity.name.commander.orders",
    )
    lines += write_syntax(
        game_objects["proposal_types"].keys(),
        "Proposal Types",
        "entity.name.proposal.type",
    )
    lines += write_syntax(
        game_objects["companies"].keys(),
        "Companies",
        "entity.name.company",
    )
    lines += write_syntax(
        game_objects["discrimination_traits"].keys(),
        "Discrimination Traits",
        "entity.name.discrimination.trait",
    )
    lines += write_syntax(
        game_objects["combat_unit_group"].keys(),
        "Combat Unit Group",
        "entity.name.combat.unit.group",
    )
    lines += write_syntax(
        game_objects["combat_unit_type"].keys(),
        "Combat Unit Type",
        "entity.name.combat.unit.type",
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
        bg_modifs.append(f"building_group_{i}_throughput_add")
        bg_modifs.append(f"building_group_{i}_standard_of_living_add")
        bg_modifs.append(f"building_group_{i}_unincorporated_throughput_add")
        bg_modifs.append(f"building_group_{i}_fertility_mult")
        bg_modifs.append(f"building_group_{i}_mortality_mult")
        country_modifs.append(f"country_subsidies_{i}")
        for j in game_objects["pop_types"].keys():
            bg_modifs.append(f"building_group_{i}_{j}_fertility_mult")
            bg_modifs.append(f"building_group_{i}_{j}_mortality_mult")
            bg_modifs.append(f"building_group_{i}_{j}_standard_of_living_add")

    # building_output_(TRADE_GOOD)_add
    # building_input_(TRADE_GOOD)_add
    # building_output_(TRADE_GOOD)_mult
    # for i in game_objects["goods"].keys():
    # building_modifs.append(f"building_output_{i}_add")
    # building_modifs.append(f"building_input_{i}_add")
    # building_modifs.append(f"building_output_{i}_mult")
    # goods_modifs.append(f"goods_input_{i}_add")
    # goods_modifs.append(f"goods_output_{i}_add")

    # building_(BUILDING)_throughput_add
    for i in game_objects["buildings"].keys():
        building_modifs.append(f"{i}_throughput_add")

    # character_(BATTLE_CONDITION)_mult
    # for i in game_objects["battle_conditions"].keys():
    #     character_modifs.append(f"character_{i}_mult")

    # state_(RELIGION)_standard_of_living_add
    for i in game_objects["religions"].keys():
        state_modifs.append(f"state_{i}_standard_of_living_add")

    for i in game_objects["cultures"].keys():
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
        building_modifs.append(f"building_{i}_fertility_mult")
        building_modifs.append(f"building_{i}_mortality_mult")
        building_modifs.append(f"building_{i}_shares_add")
        building_modifs.append(f"building_{i}_shares_mult")
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
