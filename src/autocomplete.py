"""
Code for the autocomplete features of the plugin
"""

import re

import sublime
import sublime_plugin

from .utils import get_index


class AutoComplete:
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
            "mobilization_options": [],
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
            "commander_orders": [],
            "combat_unit_type": [],
            "proposal_types": [],
            "companies": [],
            "discrimination_traits": [],
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
        self, patterns_list, flag_name, view, line, point
    ):
        for pattern in patterns_list:
            r = re.search(rf'{pattern}\s?=\s?(")?', line)
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

    def check_region_and_set_flag(
        self, selector, flag_name, view, view_str, point, string_check_and_move=None
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
        selector_flag_pairs = [
            ("meta.ig.bracket", "igs"),
            ("meta.goods.simple.bracket", "goods"),
            ("meta.ideology.bracket", "ideologies"),
            ("meta.law.bracket", "laws"),
            ("meta.tech.bracket", "technologies"),
            ("meta.building.bracket", "buildings"),
            ("meta.bg.bracket", "bgs", "type = "),
            ("meta.da.bracket", "diplo_actions", "type = "),
            ("meta.dp.bracket", "diplo_plays", "type = "),
            ("meta.je.bracket", "jes", "type = "),
            ("meta.mods.bracket", "mods", "name = "),
            ("meta.subjects.bracket", "subject_types", "type = "),
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
