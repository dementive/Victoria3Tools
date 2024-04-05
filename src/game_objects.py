"""
Code related to loading, saving, and caching vic3 game objects
"""

import ast
import hashlib
import json
import os
from typing import Any, Dict, List, Set

import sublime

from .game_object_manager import GameObjectManager
from .jomini import dict_to_game_object as make_object
from .utils import (
    get_default_game_objects,
    get_dir_to_game_object_dict,
    get_game_object_dirs,
)
from .v3_objects import Victoria3Object


def check_mod_for_changes(v3_mod_files: List[Any], write_syntax=False) -> Set[str]:
    """
    Check if any changes have been made to mod files
    if changes have been made this returns a set of game objects that need to be recreated and cached
    """
    object_cache_path = sublime.packages_path() + f"/Victoria3Tools/object_cache.json"
    if os.stat(object_cache_path).st_size < 200:
        # If there are no objects in the cache, they all need to be created
        return set(get_dir_to_game_object_dict().values())
    mod_cache_path = sublime.packages_path() + f"/Victoria3Tools/mod_cache.json"
    with open(mod_cache_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    game_object_dirs = get_game_object_dirs()
    # Add the names and output of os.stat.st_mtime together for all the files in the current mods into stats_string
    for path in v3_mod_files:
        mod_name = path.replace("\\", "/").rstrip("/").rpartition("/")[2]
        for dirpath, dirnames, filenames in os.walk(path):
            relative_path = dirpath.replace(path, "")[1:]
            if relative_path not in game_object_dirs:
                continue

            mod_files = [
                x for x in filenames if x.endswith(".txt") or x.endswith(".gui")
            ]

            if not mod_files:
                continue

            stats_string = str()
            for i in mod_files:
                full_path = dirpath + "/" + i
                value = os.stat(full_path).st_mtime
                stats_string += f"{mod_name}{value}"

            # Encode stats_string for each game object directory
            game_object_dirs[relative_path] = hashlib.sha256(
                stats_string.encode()
            ).hexdigest()

    with open(mod_cache_path, "w") as f:
        if write_syntax:
            json_to_write = [game_object_dirs, "write_syntax"]
        else:
            json_to_write = [game_object_dirs]

        f.write(json.dumps(json_to_write))

    changed_objects = set()
    dir_to_game_object_dict = get_dir_to_game_object_dict()

    for i in compare_dicts(game_object_dirs, data[0]):
        if i in dir_to_game_object_dict:
            changed_objects.add(dir_to_game_object_dict[i])

    return changed_objects


def compare_dicts(dict1: Dict, dict2: Dict):
    # Compare two dictionaries and return a set of all the keys with values that are not the same in both
    common_keys = set(dict1.keys()) & set(dict2.keys())
    unequal_keys = set()

    for key in common_keys:
        if dict1[key] != dict2[key]:
            unequal_keys.add(key)

    return unequal_keys


def check_for_syntax_changes() -> bool:
    mod_cache_path = sublime.packages_path() + f"/Victoria3Tools/mod_cache.json"
    with open(mod_cache_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    if len(data) > 1:
        return True
    return False


def load_game_objects_json():
    path = sublime.packages_path() + f"/Victoria3Tools/object_cache.json"
    with open(path, "r") as f:
        data = json.load(f)
    return data


def cache_all_objects(game_objects: Dict[str, Victoria3Object]):
    # Write all generated objects to cache
    path = sublime.packages_path() + f"/Victoria3Tools/object_cache.json"
    objects = dict()
    for i in game_objects:
        objects[i] = game_objects[i].to_json()
    with open(path, "w") as f:
        f.write(json.dumps(objects))


def get_gui_objects_from_cache() -> Dict[str, Victoria3Object]:
    path = sublime.packages_path() + f"/Victoria3Tools/object_cache.json"
    game_objects = get_default_game_objects()
    with open(path, "r") as f:
        data = json.load(f)
    for i in game_objects:
        if i in data and i in ("gui_types", "gui_templates"):
            game_objects[i] = make_object(ast.literal_eval(data[i]))

    return game_objects


def get_objects_from_cache() -> Dict[str, Victoria3Object]:
    path = sublime.packages_path() + f"/Victoria3Tools/object_cache.json"
    game_objects = get_default_game_objects()
    with open(path, "r") as f:
        data = json.load(f)
    for i in game_objects:
        if i in data:
            game_objects[i] = make_object(ast.literal_eval(data[i]))

    return game_objects


def handle_image_cache(settings: sublime.Settings):
    cache_size_limit = settings.get("MaxImageCacheSize")
    cache = sublime.packages_path() + "/Victoria3Tools/Convert DDS/cache/"
    cache_files = [x for x in os.listdir(cache) if x.endswith(".png")]
    if len(cache_files) > cache_size_limit:  # type: ignore
        for i in cache_files:
            os.remove(os.path.join(cache, i))
        sublime.status_message("Cleared Image Cache")


def add_color_scheme_scopes():
    # Add scopes for yml text formatting to color scheme
    DEFAULT_CS = "Packages/Color Scheme - Default/Monokai.sublime-color-scheme"
    prefs = sublime.load_settings("Preferences.sublime-settings")
    cs = prefs.get("color_scheme", DEFAULT_CS)
    scheme_cache_path = os.path.join(
        sublime.packages_path(), "User", "PdxTools", cs  # type: ignore
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

    manager = GameObjectManager()
    # Append all other matches to auto-generated-content section
    lines += write_syntax(
        game_objects[manager.scripted_triggers.name].keys(),
        "Scripted Triggers",
        "string.scripted.trigger",
    )
    lines += write_syntax(
        game_objects[manager.scripted_effects.name].keys(),
        "Scripted Effects",
        "keyword.scripted.effect",
    )
    lines += write_syntax(
        game_objects[manager.script_values.name].keys(),
        "Scripted Values",
        "storage.type.script.value",
    )

    # All GameObjects get entity.name scope
    lines += write_syntax(
        game_objects[manager.ai_strats.name].keys(),
        "Ai Strategies",
        "entity.name.ai.strat",
    )
    lines += write_syntax(
        game_objects[manager.bgs.name].keys(), "Building Groups", "entity.name.bg"
    )
    lines += write_syntax(
        game_objects[manager.buildings.name].keys(), "Buildings", "entity.name.building"
    )
    lines += write_syntax(
        game_objects[manager.char_traits.name].keys(),
        "Character Traits",
        "entity.name.character.trait",
    )
    lines += write_syntax(
        game_objects[manager.cultures.name].keys(), "Cultures", "entity.name.culture"
    )
    lines += write_syntax(
        game_objects[manager.mods.name].keys(), "Modifiers", "entity.name.modifier"
    )
    lines += write_syntax(
        game_objects[manager.modifier_types.name].keys(),
        "Modifier Type",
        "string.modifier.type",
    )
    lines += write_syntax(
        game_objects[manager.decrees.name].keys(), "Decrees", "entity.name.decree"
    )
    lines += write_syntax(
        game_objects[manager.diplo_actions.name].keys(),
        "Diplomatic Actions",
        "entity.name.diplo.action",
    )
    lines += write_syntax(
        game_objects[manager.diplo_plays.name].keys(),
        "Diplomatic Plays",
        "entity.name.diplo.play",
    )
    lines += write_syntax(
        game_objects[manager.game_rules.name].keys(),
        "Game Rules",
        "entity.name.game.rule",
    )
    lines += write_syntax(
        game_objects[manager.goods.name].keys(), "Trade Goods", "entity.name.trade.good"
    )
    lines += write_syntax(
        game_objects[manager.gov_types.name].keys(), "Gov Types", "entity.name.gov.type"
    )
    lines += write_syntax(
        game_objects[manager.ideologies.name].keys(),
        "Ideologies",
        "entity.name.ideology",
    )
    lines += write_syntax(
        game_objects[manager.institutions.name].keys(),
        "Institutions",
        "entity.name.institution",
    )
    lines += write_syntax(
        game_objects[manager.ig_traits.name].keys(), "Ig Traits", "entity.name.ig.trait"
    )
    lines += write_syntax(
        game_objects[manager.igs.name].keys(),
        "Interest Groups",
        "entity.name.interest.group",
    )
    lines += write_syntax(
        game_objects[manager.jes.name].keys(),
        "Journal Entries",
        "entity.name.journal.entry",
    )
    lines += write_syntax(
        game_objects[manager.law_groups.name].keys(),
        "Law Groups",
        "entity.name.law.group",
    )
    lines += write_syntax(
        game_objects[manager.laws.name].keys(), "Laws", "entity.name.law"
    )
    lines += write_syntax(
        game_objects[manager.mobilization_options.name].keys(),
        "Mobilization Options",
        "entity.name.mobilization.option",
    )
    lines += write_syntax(
        game_objects[manager.parties.name].keys(), "Parties", "entity.name.party"
    )
    lines += write_syntax(
        game_objects[manager.pop_needs.name].keys(), "Pop Needs", "entity.name.pop.need"
    )
    lines += write_syntax(
        game_objects[manager.pop_types.name].keys(), "Pop Types", "entity.name.pop.type"
    )
    lines += write_syntax(
        game_objects[manager.pm_groups.name].keys(),
        "Production Method Groups",
        "entity.name.pm.groups",
    )
    lines += write_syntax(
        game_objects[manager.pms.name].keys(), "Production Methods", "entity.name.pm"
    )
    lines += write_syntax(
        game_objects[manager.religions.name].keys(), "Religions", "entity.name.religion"
    )
    lines += write_syntax(
        game_objects[manager.state_traits.name].keys(),
        "State Traits",
        "entity.name.state.trait",
    )
    lines += write_syntax(
        game_objects[manager.strategic_regions.name].keys(),
        "Strategic Regions",
        "entity.name.strategic.region",
    )
    lines += write_syntax(
        game_objects[manager.subject_types.name].keys(),
        "Subject Types",
        "entity.name.subject.type",
    )
    lines += write_syntax(
        game_objects[manager.technologies.name].keys(),
        "Technologies",
        "entity.name.tech",
    )
    lines += write_syntax(
        game_objects[manager.terrains.name].keys(), "Terrains", "entity.name.terrain"
    )
    lines += write_syntax(
        game_objects[manager.state_regions.name].keys(),
        "State Regions",
        "entity.name.state.region",
    )
    lines += write_syntax(
        game_objects[manager.countries.name].keys(),
        "Countries",
        "entity.name.countries",
    )
    lines += write_syntax(
        game_objects[manager.country_ranks.name].keys(),
        "Country Ranks",
        "entity.name.country.ranks",
    )
    lines += write_syntax(
        game_objects[manager.country_types.name].keys(),
        "Country Types",
        "entity.name.country.types",
    )
    lines += write_syntax(
        game_objects[manager.culture_graphics.name].keys(),
        "Culture Graphics",
        "entity.name.culture.graphics",
    )
    lines += write_syntax(
        game_objects[manager.named_colors.name].keys(),
        "Named Colors",
        "entity.name.named.colors",
    )
    lines += write_syntax(
        game_objects[manager.battle_conditions.name].keys(),
        "Battle Conditions",
        "entity.name.battle.conditions",
    )
    lines += write_syntax(
        game_objects[manager.commander_ranks.name].keys(),
        "Commander Ranks",
        "entity.name.commander.ranks",
    )
    lines += write_syntax(
        game_objects[manager.commander_orders.name].keys(),
        "Commander Orders",
        "entity.name.commander.orders",
    )
    lines += write_syntax(
        game_objects[manager.proposal_types.name].keys(),
        "Proposal Types",
        "entity.name.proposal.type",
    )
    lines += write_syntax(
        game_objects[manager.companies.name].keys(),
        "Companies",
        "entity.name.company",
    )
    lines += write_syntax(
        game_objects[manager.discrimination_traits.name].keys(),
        "Discrimination Traits",
        "entity.name.discrimination.trait",
    )
    lines += write_syntax(
        game_objects[manager.combat_unit_group.name].keys(),
        "Combat Unit Group",
        "entity.name.combat.unit.group",
    )
    lines += write_syntax(
        game_objects[manager.combat_unit_type.name].keys(),
        "Combat Unit Type",
        "entity.name.combat.unit.type",
    )
    lines += write_syntax(
        game_objects[manager.scripted_gui.name].keys(),
        "Scripted Gui",
        "entity.name.scripted.gui",
    )
    lines += write_syntax(
        game_objects[manager.custom_loc.name].keys(),
        "Customizable Localization",
        "entity.name.custom.loc",
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
    for i in game_objects[manager.igs.name].keys():
        ig_modifs.append(f"interest_group_{i}_pol_str_mult")
        ig_modifs.append(f"interest_group_{i}_approval_add")
        ig_modifs.append(f"interest_group_{i}_pop_attraction_mult")

    # building_group_(BG)_(POP_TYPE)_fertility_mult
    # building_group_(BG)_(POP_TYPE)_mortality_mult
    # building_group_(BG)_(POP_TYPE)_standard_of_living_add
    # building_group_(BG)_tax_mult
    # building_group_(BG)_employee_mult
    # country_subsidies_(BG)
    for i in game_objects[manager.bgs.name].keys():
        bg_modifs.append(f"building_group_{i}_tax_mult")
        bg_modifs.append(f"building_group_{i}_employee_mult")
        bg_modifs.append(f"building_group_{i}_throughput_add")
        bg_modifs.append(f"building_group_{i}_standard_of_living_add")
        bg_modifs.append(f"building_group_{i}_unincorporated_throughput_add")
        bg_modifs.append(f"building_group_{i}_fertility_mult")
        bg_modifs.append(f"building_group_{i}_mortality_mult")
        country_modifs.append(f"country_subsidies_{i}")
        for j in game_objects[manager.pop_types.name].keys():
            bg_modifs.append(f"building_group_{i}_{j}_fertility_mult")
            bg_modifs.append(f"building_group_{i}_{j}_mortality_mult")
            bg_modifs.append(f"building_group_{i}_{j}_standard_of_living_add")

    # building_output_(TRADE_GOOD)_add
    # building_input_(TRADE_GOOD)_add
    # building_output_(TRADE_GOOD)_mult
    # for i in game_objects[manager.goods.name].keys():
    # building_modifs.append(f"building_output_{i}_add")
    # building_modifs.append(f"building_input_{i}_add")
    # building_modifs.append(f"building_output_{i}_mult")
    # goods_modifs.append(f"goods_input_{i}_add")
    # goods_modifs.append(f"goods_output_{i}_add")

    # building_(BUILDING)_throughput_add
    for i in game_objects[manager.buildings.name].keys():
        building_modifs.append(f"{i}_throughput_add")

    # character_(BATTLE_CONDITION)_mult
    # for i in game_objects[manager.battle_conditions.name].keys():
    #     character_modifs.append(f"character_{i}_mult")

    # state_(RELIGION)_standard_of_living_add
    for i in game_objects[manager.religions.name].keys():
        state_modifs.append(f"state_{i}_standard_of_living_add")

    for i in game_objects[manager.cultures.name].keys():
        state_modifs.append(f"state_{i}_standard_of_living_add")

    # country_(INSTITUTION)_max_investment_add
    for i in game_objects[manager.institutions.name].keys():
        state_modifs.append(f"country_{i}_max_investment_add")

    for i in game_objects[manager.pop_types.name].keys():
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

    for i in game_objects[manager.laws.name].keys():
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
