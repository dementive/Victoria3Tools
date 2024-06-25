"""
The main event listener for the plugin, this is where most of the plugin features actually happen.
The init function of the event listener is treated as the main entry point for the plugin.
"""

import os
import re
import threading
import time
from typing import List, Tuple, Union

import sublime
import sublime_plugin

from JominiTools.src import encoding_check
from .autocomplete import AutoComplete
from .game_data import VictoriaGameData
from .game_objects import write_data_to_syntax
from .game_object_manager import GameObjectManager
from .v3_objects import *
from .plugin import VictoriaPlugin
from JominiTools.src.jomini_objects import *
from JominiTools.src.shaders import on_hover_shaders
from JominiTools.src import (
    ScopeMatch,
    get_file_name,
    get_syntax_name,
    is_file_in_directory,
    GameObjectBase,
    Hover,
    JominiEventListener,
)


class VictoriaEventListener(
    Hover,
    AutoComplete,
    ScopeMatch,
    JominiEventListener,
    sublime_plugin.EventListener,
):
    def write_data_to_syntax(self, game_objects):
        write_data_to_syntax(game_objects)

    def on_init(self, views):
        self.init(VictoriaPlugin())

    def init_game_object_manager(self):
        self.manager = GameObjectManager()

    def init_game_data(self):
        self.game_data = VictoriaGameData()

    def create_all_game_objects(self):
        t0 = time.time()

        def load_first():
            self.game_objects["mods"] = Modifier()

        def load_second():
            self.game_objects[self.manager.state_regions.name] = StateRegion()
            self.game_objects[self.manager.scripted_effects.name] = ScriptedEffect(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.laws.name] = Law()
            self.game_objects[self.manager.ig_traits.name] = InterestGroupTrait()
            self.game_objects[self.manager.ai_strats.name] = AiStrategy()
            self.game_objects[self.manager.pop_types.name] = PopType()
            self.game_objects[self.manager.parties.name] = Party()
            self.game_objects[self.manager.subject_types.name] = SubjectType()
            self.game_objects[self.manager.combat_unit_group.name] = CombatUnitGroup()

        def load_third():
            self.game_objects[self.manager.countries.name] = Country()
            self.game_objects[self.manager.pm_groups.name] = ProductionMethodGroup()
            self.game_objects[self.manager.script_values.name] = ScriptValue(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.ideologies.name] = Ideology()
            self.game_objects[self.manager.bgs.name] = BuildingGroup()
            self.game_objects[self.manager.law_groups.name] = LawGroup()
            self.game_objects[self.manager.religions.name] = Religion()
            self.game_objects[self.manager.decrees.name] = Decree()
            self.game_objects[self.manager.institutions.name] = Institutions()
            self.game_objects[self.manager.country_types.name] = CountryType()

        def load_fourth():
            self.game_objects[self.manager.modifier_types.name] = ModifierType()
            self.game_objects[self.manager.strategic_regions.name] = StrategicRegion()
            self.game_objects[self.manager.companies.name] = CompanyType()
            self.game_objects[self.manager.discrimination_traits.name] = (
                DiscriminationTrait()
            )
            self.game_objects[self.manager.diplo_plays.name] = DiplomaticPlay()
            self.game_objects[self.manager.terrains.name] = Terrain()
            self.game_objects[self.manager.battle_conditions.name] = BattleCondition()
            self.game_objects[self.manager.pop_needs.name] = PopNeed()
            self.game_objects[self.manager.country_ranks.name] = CountryRank()
            self.game_objects[self.manager.scripted_modifiers.name] = ScriptedModifier(
                self.mod_files, self.game_files_path
            )

        def load_fifth():
            self.game_objects[self.manager.pms.name] = ProductionMethod()
            self.game_objects[self.manager.cultures.name] = Culture()
            self.game_objects[self.manager.technologies.name] = Technology()
            self.game_objects[self.manager.named_colors.name] = NamedColor(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.char_traits.name] = CharacterTrait()
            self.game_objects[self.manager.combat_unit_type.name] = CombatUnitType()
            self.game_objects[self.manager.commander_orders.name] = CommanderOrder()
            self.game_objects[self.manager.game_rules.name] = GameRules()
            self.game_objects[self.manager.commander_ranks.name] = CommanderRank()
            self.game_objects[self.manager.culture_graphics.name] = CultureGraphics()

        def load_sixth():
            self.game_objects[self.manager.scripted_triggers.name] = ScriptedTrigger(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.jes.name] = JournalEntry()
            self.game_objects[self.manager.state_traits.name] = StateTrait()
            self.game_objects[self.manager.gov_types.name] = GovernmentType()
            self.game_objects[self.manager.buildings.name] = Building()
            self.game_objects[self.manager.goods.name] = Goods()
            self.game_objects[self.manager.diplo_actions.name] = DiplomaticAction()
            self.game_objects[self.manager.mobilization_options.name] = (
                MobilizationOption()
            )
            self.game_objects[self.manager.proposal_types.name] = ProposalType()
            self.game_objects[self.manager.igs.name] = InterestGroup()
            self.game_objects[self.manager.scripted_gui.name] = ScriptedGui(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.custom_loc.name] = CustomLoc()
            self.game_objects[self.manager.gui_types.name] = GuiType(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.gui_templates.name] = GuiTemplate(
                self.mod_files, self.game_files_path
            )
            self.game_objects[self.manager.gui_templates.name].remove("inside")
            self.game_objects[self.manager.gui_templates.name].remove("you")
            self.game_objects[self.manager.gui_templates.name].remove("can")
            self.game_objects[self.manager.gui_templates.name].remove("but")
            self.game_objects[self.manager.gui_templates.name].remove("on")
            self.game_objects[self.manager.gui_templates.name].remove("within")
            self.game_objects[self.manager.gui_templates.name].remove("names")

        thread1 = threading.Thread(target=load_first)
        thread2 = threading.Thread(target=load_second)
        thread3 = threading.Thread(target=load_third)
        thread4 = threading.Thread(target=load_fourth)
        thread5 = threading.Thread(target=load_fifth)
        thread6 = threading.Thread(target=load_sixth)
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()

        # Write syntax data after creating objects so they actually exist when writing
        sublime.set_timeout_async(lambda: write_data_to_syntax(self.game_objects), 0)

        t1 = time.time()
        print("Time taken to create Victoria 3 objects: {:.3f} seconds".format(t1 - t0))

    def on_deactivated_async(self, view):
        super().on_deactivated_async(view)

    def on_activated_async(self, view):
        super().on_activated_async(view)

    def on_query_completions(
        self, view: sublime.View, prefix: str, locations: List[int]
    ) -> Union[
        None,
        List[Union[str, Tuple[str, str], sublime.CompletionItem]],
        Tuple[
            List[Union[str, Tuple[str, str], sublime.CompletionItem]],
            sublime.AutoCompleteFlags,
        ],
        sublime.CompletionList,
    ]:
        if not view:
            return None

        syntax_name = get_syntax_name(view)

        if not self.plugin.valid_syntax(syntax_name):
            return None

        if self.plugin.is_data_system_syntax(syntax_name):
            for flag, completion in self.game_data.data_system_completion_flag_pairs:
                completion_list = self.create_completion_list(flag, completion)
                if completion_list is not None:
                    return completion_list
            return  # Don't need to check anything else for data system

        for flag, completion in self.game_data.completion_flag_pairs:
            completion_list = self.create_completion_list(flag, completion)
            if completion_list is not None:
                return completion_list

        fname = get_file_name(view)
        # Special completions
        if "script_values" in fname or "scripted_modifiers" in fname:
            e_list = []
            for i in self.game_data.game_effects:
                e_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
                        details=self.game_data.game_effects[i].split("<br>")[0],
                    )
                )
            t_list = []
            for i in self.game_data.game_triggers:
                t_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
                        details=self.game_data.game_triggers[i].split("<br>")[0],
                    )
                )
            return sublime.CompletionList(e_list + t_list)
        if self.trigger_field or "scripted_triggers" in fname:
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
                        details=self.game_data.game_triggers[key].split("<br>")[0],
                    )
                    for key in sorted(self.game_data.game_triggers)
                ]
            )
        if self.mtth_field:
            x = dict(sorted(self.game_data.ValueFieldCompletionList.items()))
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "V", "Value"),
                        details=self.game_data.ValueFieldCompletionList[key],
                    )
                    for key in x
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS
                | sublime.INHIBIT_REORDER,
            )
        if (
            self.effect_field
            or "scripted_effects" in fname
            or f"common{os.sep}history" in fname
        ):
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
                        details=self.game_data.game_effects[key].split("<br>")[0],
                    )
                    for key in sorted(self.game_data.game_effects)
                ]
            )
        if self.modifier_field or re.search("modifiers", fname):
            completions = self.game_objects["modifier_types"].keys()
            completions = sorted(completions)
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_SNIPPET, "M", "Modifier Type"),
                        details=" ",
                    )
                    for key in sorted(completions)
                ],
                flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
                | sublime.INHIBIT_WORD_COMPLETIONS,
            )
        return None

    def on_selection_modified_async(self, view: sublime.View):
        if not view:
            return

        syntax_name = get_syntax_name(view)

        if not self.plugin.valid_syntax(syntax_name):
            return

        if not self.plugin.is_data_system_syntax(syntax_name):
            self.simple_scope_match(view)

        # Only do when there is 1 selections, doens't make sense with multiple selections
        if len(view.sel()) == 1:
            point = view.sel()[0].a
            if (self.plugin.is_data_system_syntax(syntax_name)) and view.substr(
                point
            ) == "'":
                for i in self.game_data.data_system_completion_functions:
                    function_start = point - len(i[1] + "('")
                    if view.substr(view.word(function_start)) == i[1]:
                        setattr(self, i[0], True)
                        view.run_command("auto_complete")
                        return
            self.check_for_simple_completions(view, point)
            self.check_for_complex_completions(view, point)

    def on_post_save_async(self, view):
        if view is None:
            return
        if get_syntax_name(view) != self.plugin.script_syntax_name:
            return
        if not self.settings.get("ScriptValidator"):
            return

        mod_dir = [
            x for x in self.mod_files if is_file_in_directory(get_file_name(view), x)
        ]
        in_mod_dir = any(mod_dir)
        if not in_mod_dir:
            return

        encoding_check(view)

        if self.settings.get("UpdateObjectsOnSave"):
            self.update_saved_game_objects(view, mod_dir)

    def on_hover(self, view: sublime.View, point: int, hover_zone: sublime.HoverZone):
        if not view:
            return

        on_hover_shaders(view, point, self.settings)

        syntax_name = get_syntax_name(view)

        if not self.plugin.valid_syntax(syntax_name):
            return

        if view.match_selector(point, "comment.line"):
            return

        if syntax_name == self.plugin.gui_syntax_name:
            sublime.set_timeout_async(lambda: self.do_gui_hover_async(view, point), 0)
            item = view.substr(view.word(point))
            if (
                self.settings.get("GuiDocsHoverEnabled") is True
                and item in self.game_data.gui_content
            ):
                sublime.set_timeout_async(
                    lambda: self.show_gui_docs_popup(view, point, item, self.game_data),
                    0,
                )

        # Do everything that requires fetching GameObjects in non-blocking thread
        hover_objects = []
        if self.plugin.script_syntax_name == syntax_name:
            hover_objects = self.game_data.script_hover_objects

        if self.plugin.is_data_system_syntax(syntax_name):
            hover_objects = self.game_data.data_system_hover_objects

        # Do everything that requires fetching GameObjects in non-blocking thread
        sublime.set_timeout_async(
            lambda: self.do_hover_async(view, point, hover_objects), 0
        )

        if (
            syntax_name != self.plugin.script_syntax_name
            and syntax_name != self.plugin.gui_syntax_name
        ):
            # For yml only the saved scopes/variables/game objects get hover
            return

        if (
            syntax_name == self.plugin.script_syntax_name
            and self.settings.get("DocsHoverEnabled") is True
        ):
            if view.match_selector(point, "keyword.effect"):
                self.game_data.game_effects.update(self.game_data.CustomEffectsList)
                self.show_hover_docs(
                    view,
                    point,
                    "keyword.effect",
                    self.game_data.game_effects,
                    self.settings,
                )
            elif view.match_selector(point, "string.trigger"):
                self.game_data.game_triggers.update(self.game_data.CustomTriggersList)
                self.show_hover_docs(
                    view,
                    point,
                    "string.trigger",
                    self.game_data.game_triggers,
                    self.settings,
                )
            elif view.match_selector(point, "storage.type.scope"):
                self.game_data.game_scopes.update(self.game_data.CustomScopesList)
                self.show_hover_docs(
                    view,
                    point,
                    "storage.type.scope",
                    self.game_data.game_scopes,
                    self.settings,
                )
            elif view.match_selector(point, "string.modifier.type"):
                self.show_hover_docs(
                    view,
                    point,
                    "string.modifier.type",
                    self.game_data.game_modifiers,
                    self.settings,
                )

        if not self.settings.get("TextureOpenPopup"):
            return

        posLine = view.line(point)
        linestr = view.substr(posLine)
        if ".dds" not in linestr and ".tga" not in linestr:
            return

        texture_raw_start = view.find("gfx", posLine.a)
        texture_raw_end = (
            view.find(".dds", posLine.a)
            if ".dds" in linestr
            else view.find(".tga", posLine.a)
        )
        texture_raw_region = sublime.Region(texture_raw_start.a, texture_raw_end.b)
        texture_raw_path = view.substr(texture_raw_region)
        full_texture_path = os.path.join(self.game_files_path, texture_raw_path)  # type: ignore

        if os.path.exists(full_texture_path):
            texture_name = view.substr(view.word(texture_raw_end.a - 1))
            self.show_texture_hover_popup(view, point, texture_name, full_texture_path)
            return

        # Check mod paths if it's not vanilla
        for mod in [m for m in self.mod_files if os.path.exists(m)]:
            if os.path.exists(mod) and mod.endswith("mod"):
                # if it is the path to the mod directory, get all directories in it
                for directory in [f.path for f in os.scandir(mod) if f.is_dir()]:
                    mod_path = os.path.join(directory, texture_raw_path)
                    if os.path.exists(mod_path):
                        full_texture_path = mod_path
            else:
                mod_path = os.path.join(mod, texture_raw_path)
                if os.path.exists(mod_path):
                    full_texture_path = mod_path

        # The path exists and the point in the view is inside of the path
        if texture_raw_region.contains(point) and os.path.exists(full_texture_path):
            texture_name = view.substr(view.word(texture_raw_end.a - 1))
            self.show_texture_hover_popup(view, point, texture_name, full_texture_path)

    def do_gui_hover_async(self, view: sublime.View, point: int):
        word = view.substr(view.word(point))

        if view.match_selector(point, "comment.line"):
            return

        if gtemplate := self.game_objects["gui_templates"].access(word):
            self.show_gui_popup(
                view,
                point,
                gtemplate,
                "Gui Template",
            )

        if gtype := self.game_objects["gui_types"].access(word):
            self.show_gui_popup(
                view,
                point,
                gtype,
                "Gui Type",
            )

    def update_saved_game_objects(self, view: sublime.View, mod_dir: List[str]):
        dir_to_game_object_dict = self.manager.get_dir_to_game_object_dict()
        filename = get_file_name(view)
        if not filename:
            return
        relative_path = filename.replace(mod_dir[-1], "")[1:]
        directory_path = os.path.dirname(relative_path)
        if directory_path not in dir_to_game_object_dict:
            return

        write_syntax: bool = self.settings.get("UpdateSyntaxOnNewObjectCreation")  # type: ignore
        if write_syntax:
            changed_objects_set = self.jomini_game_object.check_mod_for_changes(
                self.mod_files,
                self.manager.get_dir_to_game_object_dict(),
                self.manager.get_game_object_dirs(),
            )
        else:
            changed_objects_set = self.jomini_game_object.check_mod_for_changes(
                self.mod_files,
                self.manager.get_dir_to_game_object_dict(),
                self.manager.get_game_object_dirs(),
            )
        if changed_objects_set:
            # This checks if an object has actually been added in this save

            game_object_to_check = dir_to_game_object_dict[directory_path]
            game_objects = self.game_objects[game_object_to_check].keys()
            game_objects_in_file = set()

            view_lines = view.lines(sublime.Region(0, len(view)))

            level_1_dirs = {}  # game objects parsed from level 1
            level_2_dirs = {}  # game objects parsed from level 2
            if relative_path in level_1_dirs:
                base_object = GameObjectBase(level=1)
            elif relative_path in level_2_dirs:
                base_object = GameObjectBase(level=2)
            else:
                base_object = GameObjectBase()
            for line in view_lines:
                line = view.substr(line)
                if base_object.should_read(line):
                    found_item = (
                        line.split("=").pop(0).replace(" ", "").replace("\t", "")
                    )
                    if not found_item:
                        continue
                    game_objects_in_file.add(found_item)

            common_objects = [x in game_objects for x in game_objects_in_file]

            # If the loaded objects from this file are not the same as the objects in the cache a new object has been added.
            if not all(common_objects):
                self.load_changed_objects(
                    changed_objects_set,
                    write_syntax,
                )
