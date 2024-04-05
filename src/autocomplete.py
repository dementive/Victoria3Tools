"""
Code for the autocomplete features of the plugin
"""

import re
from typing import List

import sublime

from .game_object_manager import GameObjectManager
from .utils import get_index


class AutoComplete:
    def __init__(self):
        manager = GameObjectManager()
        self.fields = {
            # Note: these need to have the same names as they do in the game_objects dict
            "trigger_field": [],
            "effect_field": [],
            "modifier_field": [],
            "mtth_field": [],
            manager.ai_strats.name: [],
            manager.battle_conditions.name: [],
            manager.bgs.name: [],
            manager.buildings.name: [],
            manager.char_traits.name: [],
            manager.combat_unit_type.name: [],
            manager.commander_orders.name: [],
            manager.commander_ranks.name: [],
            manager.companies.name: [],
            manager.countries.name: [],
            manager.country_ranks.name: [],
            manager.country_types.name: [],
            manager.culture_graphics.name: [],
            manager.cultures.name: [],
            manager.custom_loc.name: [],
            manager.decrees.name: [],
            manager.diplo_actions.name: [],
            manager.diplo_plays.name: [],
            manager.discrimination_traits.name: [],
            manager.game_rules.name: [],
            manager.goods.name: [],
            manager.gov_types.name: [],
            manager.ideologies.name: [],
            manager.igs.name: [],
            manager.institutions.name: [],
            manager.jes.name: [],
            manager.law_groups.name: [],
            manager.laws.name: [],
            manager.mobilization_options.name: [],
            manager.mods.name: [],
            manager.named_colors.name: [],
            manager.parties.name: [],
            manager.pms.name: [],
            manager.pop_types.name: [],
            manager.proposal_types.name: [],
            manager.religions.name: [],
            manager.scripted_gui.name: [],
            manager.state_regions.name: [],
            manager.state_traits.name: [],
            manager.strategic_regions.name: [],
            manager.subject_types.name: [],
            manager.technologies.name: [],
            manager.terrains.name: [],
        }
        for field in self.fields.keys():
            setattr(self, field, False)

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
        self,
        patterns_list: List[str],
        flag_name: str,
        view: sublime.View,
        line: str,
        point: int,
    ):
        for pattern in patterns_list:
            r = re.search(rf'\b{pattern}\s?=\s?(")?', line)
            if not r:
                continue
            y = 0
            idx = line.index(pattern) + view.line(point).a + len(pattern) + 2
            if r.groups()[0] == '"':
                y = 2
            if idx == point or idx + y == point or idx + 1 == point:
                setattr(self, flag_name, True)
                view.run_command("auto_complete")
                return True
        return False

    def check_pattern_and_set_flag(
        self, pattern: str, flag_name: str, view: sublime.View, line: str, point: int
    ):
        if pattern in line:
            idx = line.index(pattern) + view.line(point).a + len(pattern)
            if idx == point:
                setattr(self, flag_name, True)
                view.run_command("auto_complete")

    def check_region_and_set_flag(
        self,
        selector: str,
        flag_name: str,
        view: sublime.View,
        view_str: str,
        point: int,
        string_check_and_move=None,
    ):
        for br in view.find_by_selector(selector):
            i = sublime.Region(br.a, get_index(view_str, br.a))
            s = view.substr(i)
            if string_check_and_move and string_check_and_move in s:
                fpoint = (
                    s.index(string_check_and_move) + len(string_check_and_move)
                ) + i.a
                if fpoint == point:
                    setattr(self, flag_name, True)
                    view.run_command("auto_complete")
            elif i.contains(point) and not string_check_and_move:
                setattr(self, flag_name, True)
                view.run_command("auto_complete")

    def check_complex_completions(self, view, point):
        view_str = view.substr(sublime.Region(0, view.size()))

        # Define the list of selectors and corresponding flags
        manager = GameObjectManager()
        selector_flag_pairs = [
            ("meta.ig.bracket", manager.igs.name),
            ("meta.goods.simple.bracket", manager.goods.name),
            ("meta.ideology.bracket", manager.ideologies.name),
            ("meta.law.bracket", manager.laws.name),
            ("meta.tech.bracket", manager.technologies.name),
            ("meta.building.bracket", manager.buildings.name),
            ("meta.bg.bracket", manager.bgs.name, "type = "),
            ("meta.da.bracket", manager.diplo_actions.name, "type = "),
            ("meta.dp.bracket", manager.diplo_plays.name, "type = "),
            ("meta.je.bracket", manager.jes.name, "type = "),
            ("meta.mods.bracket", manager.mods.name, "name = "),
            ("meta.subjects.bracket", manager.subject_types.name, "type = "),
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
