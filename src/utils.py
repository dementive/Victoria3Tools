"""
Utility functions used in various places
"""

import os
import subprocess
import sys
from collections import deque

from .jomini import GameObjectBase


def get_default_game_objects():
    base_object = GameObjectBase()

    # global dictionary of game objects used everywhere
    game_objects = {
        "ai_strats": base_object,
        "battle_conditions": base_object,
        "bgs": base_object,
        "buildings": base_object,
        "char_traits": base_object,
        "combat_unit_group": base_object,
        "combat_unit_type": base_object,
        "commander_orders": base_object,
        "commander_ranks": base_object,
        "companies": base_object,
        "countries": base_object,
        "country_ranks": base_object,
        "country_types": base_object,
        "culture_graphics": base_object,
        "cultures": base_object,
        "decrees": base_object,
        "diplo_actions": base_object,
        "diplo_plays": base_object,
        "discrimination_traits": base_object,
        "game_rules": base_object,
        "goods": base_object,
        "gov_types": base_object,
        "gui_templates": base_object,
        "gui_types": base_object,
        "ideologies": base_object,
        "ig_traits": base_object,
        "igs": base_object,
        "institutions": base_object,
        "jes": base_object,
        "law_groups": base_object,
        "laws": base_object,
        "mobilization_options": base_object,
        "mods": base_object,
        "modifier_types": base_object,
        "named_colors": base_object,
        "parties": base_object,
        "pm_groups": base_object,
        "pms": base_object,
        "pop_needs": base_object,
        "pop_types": base_object,
        "proposal_types": base_object,
        "religions": base_object,
        "script_values": base_object,
        "scripted_effects": base_object,
        "scripted_modifiers": base_object,
        "scripted_triggers": base_object,
        "state_regions": base_object,
        "state_traits": base_object,
        "strategic_regions": base_object,
        "subject_types": base_object,
        "technologies": base_object,
        "terrains": base_object,
    }

    return game_objects


def is_file_in_directory(file_path, directory_path):
    if not os.path.exists(file_path):
        return False

    if not os.path.exists(directory_path):
        return False

    absolute_file_path = os.path.abspath(file_path)
    absolute_directory_path = os.path.abspath(directory_path)

    common_path = os.path.commonpath([absolute_file_path, absolute_directory_path])

    return common_path == absolute_directory_path


# Get the index of a closing bracket in a string given the starting brackets index
def get_index(string, index):
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


def open_path(path):
    system = sys.platform
    if system == "Darwin":  # macOS
        subprocess.call(("open", path))
    elif system == "Windows" or system == "win32" or system == "win":  # Windows
        os.startfile(path)
    else:  # Linux and other Unix-like systems
        subprocess.call(("xdg-open", path))
