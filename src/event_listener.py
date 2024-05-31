"""
The main event listener for the plugin, this is where most of the plugin features actually happen.
The init function of the event listener is treated as the main entry point for the plugin.
"""

import os
import re
import threading
import time
from typing import List, Set, Tuple, Union

import sublime
import sublime_plugin

from .autocomplete import AutoComplete
from .encoding import encoding_check
from .game_data import GameData
from .game_object_manager import GameObjectManager
from .game_objects import (
    add_color_scheme_scopes,
    cache_all_objects,
    check_for_syntax_changes,
    check_mod_for_changes,
    get_gui_objects_from_cache,
    get_objects_from_cache,
    handle_image_cache,
    load_game_objects_json,
    write_data_to_syntax,
)
from .hover import Hover
from .jomini import PdxScriptObject
from .scope_match import ScopeMatch
from .shaders import on_hover_shaders
from .utils import (
    get_default_game_objects,
    get_file_name,
    get_game_object_to_class_dict,
    get_syntax_name,
    is_file_in_directory,
    open_path,
)
from .v3_objects import *


class VictoriaEventListener(
    Hover, AutoComplete, ScopeMatch, sublime_plugin.EventListener
):
    def on_init(self, views):
        self.game_objects = get_default_game_objects()
        self.GameData = GameData()
        self.settings = sublime.load_settings("Victoria Syntax.sublime-settings")
        self.v3_files_path = self.settings.get("Victoria3FilesPath")
        self.v3_mod_files = self.settings.get("PathsToModFiles")
        self.gui_files_path = self.settings.get("GuiBaseGamePath")
        self.gui_mod_files = self.settings.get("PathsToGuiModFiles")

        script_enabled = self.settings.get("EnableVictoriaScriptingFeatures")
        syntax_changes = check_for_syntax_changes()
        changed_objects_set = check_mod_for_changes(self.v3_mod_files)

        if len(load_game_objects_json()) != len(self.game_objects):
            # Create new objects
            if script_enabled:
                sublime.set_timeout_async(lambda: self.create_all_game_objects(), 0)
                sublime.active_window().run_command("vic_run_tiger")
            else:
                sublime.set_timeout_async(lambda: self.load_gui_objects(), 0)
        elif changed_objects_set:
            self.load_changed_objects(changed_objects_set)
            if script_enabled:
                sublime.active_window().run_command("vic_run_tiger")
        elif not script_enabled:
            self.game_objects = get_gui_objects_from_cache()
        else:
            # Load cached objects
            self.game_objects = get_objects_from_cache()
            if syntax_changes:
                sublime.set_timeout_async(
                    lambda: write_data_to_syntax(self.game_objects), 0
                )

        # # Uncomment this and use the output to balance the load between the threads in create_all_game_objects
        # from .utils import print_load_balanced_game_object_creation

        # sublime.set_timeout_async(
        #     lambda: print_load_balanced_game_object_creation(self.game_objects), 0
        # )

        handle_image_cache(self.settings)
        add_color_scheme_scopes()

    def load_changed_objects(self, changed_objects_set: Set[str], write_syntax=True):
        # Load objects that have changed since they were last cached
        self.game_objects = get_objects_from_cache()

        sublime.set_timeout_async(
            lambda: self.create_game_objects(changed_objects_set), 0
        )
        if write_syntax:
            sublime.set_timeout_async(
                lambda: write_data_to_syntax(self.game_objects), 0
            )

        # Cache created objects
        sublime.set_timeout_async(lambda: cache_all_objects(self.game_objects), 0)

    def create_game_objects(
        self,
        changed_objects_set: Set[str],
    ):
        game_object_to_class_dict = get_game_object_to_class_dict()
        for i in changed_objects_set:
            # TODO - threading and load balancing here if the expected number of objects to be created is > 250
            self.game_objects[i] = game_object_to_class_dict[i]()

    def create_all_game_objects(self):
        t0 = time.time()
        manager = GameObjectManager()

        def load_first():
            self.game_objects["mods"] = Modifier()

        def load_second():
            self.game_objects[manager.state_regions.name] = StateRegion()
            self.game_objects[manager.scripted_effects.name] = ScriptedEffect()
            self.game_objects[manager.laws.name] = Law()
            self.game_objects[manager.ig_traits.name] = InterestGroupTrait()
            self.game_objects[manager.ai_strats.name] = AiStrategy()
            self.game_objects[manager.pop_types.name] = PopType()
            self.game_objects[manager.parties.name] = Party()
            self.game_objects[manager.subject_types.name] = SubjectType()
            self.game_objects[manager.combat_unit_group.name] = CombatUnitGroup()

        def load_third():
            self.game_objects[manager.countries.name] = Country()
            self.game_objects[manager.pm_groups.name] = ProductionMethodGroup()
            self.game_objects[manager.script_values.name] = ScriptValue()
            self.game_objects[manager.ideologies.name] = Ideology()
            self.game_objects[manager.bgs.name] = BuildingGroup()
            self.game_objects[manager.law_groups.name] = LawGroup()
            self.game_objects[manager.religions.name] = Religion()
            self.game_objects[manager.decrees.name] = Decree()
            self.game_objects[manager.institutions.name] = Institutions()
            self.game_objects[manager.country_types.name] = CountryType()

        def load_fourth():
            self.game_objects[manager.modifier_types.name] = ModifierType()
            self.game_objects[manager.strategic_regions.name] = StrategicRegion()
            self.game_objects[manager.companies.name] = CompanyType()
            self.game_objects[manager.discrimination_traits.name] = (
                DiscriminationTrait()
            )
            self.game_objects[manager.diplo_plays.name] = DiplomaticPlay()
            self.game_objects[manager.terrains.name] = Terrain()
            self.game_objects[manager.battle_conditions.name] = BattleCondition()
            self.game_objects[manager.pop_needs.name] = PopNeed()
            self.game_objects[manager.country_ranks.name] = CountryRank()
            self.game_objects[manager.scripted_modifiers.name] = ScriptedModifier()

        def load_fifth():
            self.game_objects[manager.pms.name] = ProductionMethod()
            self.game_objects[manager.cultures.name] = Culture()
            self.game_objects[manager.technologies.name] = Technology()
            self.game_objects[manager.named_colors.name] = NamedColor()
            self.game_objects[manager.char_traits.name] = CharacterTrait()
            self.game_objects[manager.combat_unit_type.name] = CombatUnitType()
            self.game_objects[manager.commander_orders.name] = CommanderOrder()
            self.game_objects[manager.game_rules.name] = GameRules()
            self.game_objects[manager.commander_ranks.name] = CommanderRank()
            self.game_objects[manager.culture_graphics.name] = CultureGraphics()

        def load_sixth():
            self.game_objects[manager.scripted_triggers.name] = ScriptedTrigger()
            self.game_objects[manager.jes.name] = JournalEntry()
            self.game_objects[manager.state_traits.name] = StateTrait()
            self.game_objects[manager.gov_types.name] = GovernmentType()
            self.game_objects[manager.buildings.name] = Building()
            self.game_objects[manager.goods.name] = Goods()
            self.game_objects[manager.diplo_actions.name] = DiplomaticAction()
            self.game_objects[manager.mobilization_options.name] = MobilizationOption()
            self.game_objects[manager.proposal_types.name] = ProposalType()
            self.game_objects[manager.igs.name] = InterestGroup()
            self.game_objects[manager.scripted_gui.name] = ScriptedGui()
            self.game_objects[manager.custom_loc.name] = CustomLoc()

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

        # Load gui objects after script objects
        sublime.set_timeout_async(lambda: self.load_gui_objects(), 0)

        t1 = time.time()
        print("Time taken to create Victoria 3 objects: {:.3f} seconds".format(t1 - t0))

    def load_gui_objects(self):
        global game_objects
        manager = GameObjectManager()
        self.game_objects[manager.gui_types.name] = GuiType()
        self.game_objects[manager.gui_templates.name] = GuiTemplate()
        self.game_objects[manager.gui_templates.name].remove("inside")
        self.game_objects[manager.gui_templates.name].remove("you")
        self.game_objects[manager.gui_templates.name].remove("can")
        self.game_objects[manager.gui_templates.name].remove("but")
        self.game_objects[manager.gui_templates.name].remove("on")
        self.game_objects[manager.gui_templates.name].remove("within")
        self.game_objects[manager.gui_templates.name].remove("names")

        # Cache created objects
        sublime.set_timeout_async(lambda: cache_all_objects(self.game_objects), 0)
        sublime.set_timeout_async(
            lambda: check_mod_for_changes(self.v3_mod_files), 0
        )  # Update hashes for each game object directory

    def on_deactivated_async(self, view: sublime.View):
        """
        Remove field states when view loses focus
        if cursor was in a field in the old view but not the new view the completions will still be accurate
        save the id of the view so it can be readded when it regains focus
        """

        if not self.settings.get("EnableVictoriaScriptingFeatures"):
            return

        vid = view.id()
        for field, views in self.fields.items():
            if getattr(self, field):
                setattr(self, field, False)
                views.append(vid)

    def on_activated_async(self, view: sublime.View):
        if not self.settings.get("EnableVictoriaScriptingFeatures"):
            return

        vid = view.id()
        for field, views in self.fields.items():
            if vid in views:
                setattr(self, field, True)
                views.remove(vid)

    def create_completion_list(self, flag_name: str, completion_kind):
        if not getattr(self, flag_name, False):
            return None

        completions = self.game_objects[flag_name].keys()
        completions = sorted(completions)
        return sublime.CompletionList(
            [
                sublime.CompletionItem(
                    trigger=key,
                    completion_format=sublime.COMPLETION_FORMAT_TEXT,
                    kind=completion_kind,
                    details=" ",
                )
                # Calling sorted() twice makes it so completions are ordered by
                # 1. the number of times they appear in the current buffer
                # 2. if they dont appear they show up alphabetically
                for key in sorted(completions)
            ],
            flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS
            | sublime.INHIBIT_WORD_COMPLETIONS,
        )

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

        if (
            syntax_name != "Victoria Script"
            and syntax_name != "Victoria Localization"
            and syntax_name != "Jomini Gui"
        ):
            return None

        if not self.settings.get("EnableVictoriaScriptingFeatures"):
            return

        if syntax_name == "Victoria Localization" or syntax_name == "Jomini Gui":
            for flag, completion in self.GameData.data_system_completion_flag_pairs:
                completion_list = self.create_completion_list(flag, completion)
                if completion_list is not None:
                    return completion_list
            return  # Don't need to check anything else for data system

        for flag, completion in self.GameData.completion_flag_pairs:
            completion_list = self.create_completion_list(flag, completion)
            if completion_list is not None:
                return completion_list

        fname = get_file_name(view)
        # Special completions
        if "script_values" in fname or "scripted_modifiers" in fname:
            e_list = []
            for i in self.GameData.EffectsList:
                e_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
                        details=self.GameData.EffectsList[i].split("<br>")[0],
                    )
                )
            t_list = []
            for i in self.GameData.TriggersList:
                t_list.append(
                    sublime.CompletionItem(
                        trigger=i,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
                        details=self.GameData.TriggersList[i].split("<br>")[0],
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
                        details=self.GameData.TriggersList[key].split("<br>")[0],
                    )
                    for key in sorted(self.GameData.TriggersList)
                ]
            )
        if self.mtth_field:
            x = dict(sorted(self.GameData.ValueFieldCompletionList.items()))
            return sublime.CompletionList(
                [
                    sublime.CompletionItem(
                        trigger=key,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_NAMESPACE, "V", "Value"),
                        details=self.GameData.ValueFieldCompletionList[key],
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
                        details=self.GameData.EffectsList[key].split("<br>")[0],
                    )
                    for key in sorted(self.GameData.EffectsList)
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

    def check_for_simple_completions(self, view: sublime.View, point: int):
        """
        Check if the current cursor position should trigger a autocompletion item
        this is for simple declarations like: remove_building = CursorHere
        """
        self.reset_shown()

        if view.substr(point) == "=":
            return

        line = view.substr(view.line(point))

        for patterns, flag in self.GameData.simple_completion_pattern_flag_pairs:
            if self.check_for_patterns_and_set_flag(patterns, flag, view, line, point):
                return

        for pattern, flag in self.GameData.simple_completion_scope_pattern_flag_pairs:
            self.check_pattern_and_set_flag(pattern, flag, view, line, point)

    def on_selection_modified_async(self, view: sublime.View):
        if not view:
            return

        syntax_name = get_syntax_name(view)

        if (
            syntax_name != "Victoria Script"
            and syntax_name != "Victoria Localization"
            and syntax_name != "Jomini Gui"
        ):
            return None

        if not self.settings.get("EnableVictoriaScriptingFeatures"):
            return

        self.simple_scope_match(view)
        # Only do when there is 1 selection, doens't make sense with multiple selections
        if len(view.sel()) == 1:
            point = view.sel()[0].a
            if (
                syntax_name == "Victoria Localization" or syntax_name == "Jomini Gui"
            ) and view.substr(point) == "'":
                for i in self.GameData.data_system_completion_functions:
                    function_start = point - len(i[1] + "('")
                    if view.substr(view.word(function_start)) == i[1]:
                        setattr(self, i[0], True)
                        view.run_command("auto_complete")
                        return
            self.check_for_simple_completions(view, point)
            self.check_complex_completions(view, point)

    def on_post_save_async(self, view):
        if view is None:
            return
        try:
            if view.syntax().name != "Victoria Script":
                return
        except AttributeError:
            return
        if self.settings.get("ScriptValidator") is False:
            return

        if not self.settings.get("EnableVictoriaScriptingFeatures"):
            return

        in_mod_dir = any(
            [x for x in self.v3_mod_files if is_file_in_directory(view.file_name(), x)]
        )

        if in_mod_dir:
            encoding_check(view)

    def on_hover(self, view: sublime.View, point: int, hover_zone: sublime.HoverZone):
        if not view:
            return

        on_hover_shaders(view, point, self.settings, self.GameData)

        syntax_name = get_syntax_name(view)

        if (
            syntax_name != "Victoria Script"
            and syntax_name != "Victoria Localization"
            and syntax_name != "Jomini Gui"
        ):
            return None

        if view.match_selector(point, "comment.line"):
            return

        if syntax_name == "Jomini Gui":
            sublime.set_timeout_async(lambda: self.do_gui_hover_async(view, point), 0)
            item = view.substr(view.word(point))
            if (
                self.settings.get("GuiDocsHoverEnabled") is True
                and item in self.GameData.GuiContent
            ):
                sublime.set_timeout_async(
                    lambda: self.show_gui_docs_popup(view, point, item, self.GameData),
                    0,
                )

        # Do everything that requires fetching GameObjects in non-blocking thread
        sublime.set_timeout_async(lambda: self.do_hover_async(view, point), 0)

        if syntax_name != "Victoria Script":
            # For yml only the saved scopes/variables/game objects get hover
            return

        if syntax_name == "Victoria Script" and self.settings.get(
            "EnableVictoriaScriptingFeatures"
        ):
            if self.settings.get("DocsHoverEnabled") is True:
                if view.match_selector(point, "keyword.effect"):
                    self.show_hover_docs(
                        view,
                        point,
                        "keyword.effect",
                        self.GameData.EffectsList,
                        self.settings,
                    )

                if view.match_selector(point, "string.trigger"):
                    self.GameData.TriggersList.update(self.GameData.CustomTriggersList)
                    self.show_hover_docs(
                        view,
                        point,
                        "string.trigger",
                        self.GameData.TriggersList,
                        self.settings,
                    )

                if view.match_selector(point, "storage.type.scope"):
                    self.GameData.ScopesList.update(self.GameData.CustomScopesList)
                    self.show_hover_docs(
                        view,
                        point,
                        "storage.type.scope",
                        self.GameData.ScopesList,
                        self.settings,
                    )

        if not self.settings.get("TextureOpenPopup"):
            return

        posLine = view.line(point)
        linestr = view.substr(posLine)
        if ".dds" not in linestr and ".tga" not in linestr:
            return

        if (
            syntax_name == "Victoria Script"
            and f"common{os.sep}coat_of_arms" in get_file_name(view)
        ):
            if "pattern" in linestr:
                raw_start = view.find("pattern", posLine.a)
                raw_end = (
                    view.find(".dds", posLine.a)
                    if ".dds" in linestr
                    else view.find(".tga", posLine.a)
                )
                raw_region = sublime.Region(raw_start.a + 10, raw_end.b)
                raw_path = view.substr(raw_region).replace('"', "")
                full_texture_path = os.path.join(
                    self.v3_files_path,
                    f"{os.sep}gfx{os.sep}coat_of_arms{os.sep}patterns{os.sep}",
                    raw_path,  # type: ignore
                )

                full_texture_path = full_texture_path
                if raw_region.contains(point) and os.path.exists(full_texture_path):
                    texture_name = view.substr(view.word(raw_end.a - 1))
                    self.show_texture_hover_popup(
                        view, point, texture_name, full_texture_path
                    )
                    return
            if "texture" in linestr:
                raw_start = view.find("texture", posLine.a)
                raw_end = (
                    view.find(".dds", posLine.a)
                    if ".dds" in linestr
                    else view.find(".tga", posLine.a)
                )
                raw_region = sublime.Region(raw_start.a + 10, raw_end.b)
                raw_path = view.substr(raw_region).replace('"', "")
                full_texture_path = os.path.join(
                    self.v3_files_path,
                    f"{os.sep}gfx{os.sep}coat_of_arms{os.sep}colored_emblems{os.sep}",
                    raw_path,
                )
                if not os.path.exists(full_texture_path):
                    full_texture_path = os.path.join(
                        self.v3_files_path,
                        f"{os.sep}gfx{os.sep}coat_of_arms{os.sep}textured_emblems{os.sep}",
                        raw_path,
                    )
                if raw_region.contains(point) and os.path.exists(full_texture_path):
                    texture_name = view.substr(view.word(raw_end.a - 1))
                    self.show_texture_hover_popup(
                        view, point, texture_name, full_texture_path
                    )
                    return

        texture_raw_start = view.find("gfx", posLine.a)
        texture_raw_end = (
            view.find(".dds", posLine.a)
            if ".dds" in linestr
            else view.find(".tga", posLine.a)
        )
        texture_raw_region = sublime.Region(texture_raw_start.a, texture_raw_end.b)
        texture_raw_path = view.substr(texture_raw_region)
        if syntax_name == "Jomini Gui":
            full_texture_path = os.path.join(self.gui_files_path, texture_raw_path)
        else:
            full_texture_path = os.path.join(self.v3_files_path, texture_raw_path)

        if os.path.exists(full_texture_path):
            texture_name = view.substr(view.word(texture_raw_end.a - 1))
            self.show_texture_hover_popup(view, point, texture_name, full_texture_path)
            return

        # Check mod paths if it's not vanilla
        for mod in [m for m in v3_mod_files if os.path.exists(m)]:
            mod_path = os.path.join(mod, texture_raw_path)
            if mod.endswith("mod"):
                # if it is the path to the mod directory, get all directories in it
                for directory in [f.path for f in os.scandir(mod) if f.is_dir()]:
                    mod_path = os.path.join(directory, texture_raw_path)
                    if os.path.exists(mod_path):
                        full_texture_path = mod_path
            else:
                if os.path.exists(mod_path):
                    full_texture_path = mod_path

        if syntax_name == "Jomini Gui":
            for mod in [m for m in gui_mod_files if os.path.exists(m)]:
                if mod.endswith("mod"):
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

    def do_hover_async(self, view: sublime.View, point: int):
        word_region = view.word(point)
        word = view.substr(word_region)
        fname = get_file_name(view)
        current_line_num = view.rowcol(point)[0] + 1

        if view.match_selector(point, "comment.line"):
            return

        if view.match_selector(point, "entity.name.function.scope.declaration"):
            if fname and (
                "scripted_triggers" in fname
                or "scripted_effects" in fname
                or "scripted_modifiers" in fname
            ):
                word = self.handle_scripted_args(view, point)
            self.show_popup_default(
                view,
                point,
                PdxScriptObject(word, fname, current_line_num),  # type: ignore
                "Scope Declaration",
            )

        if view.match_selector(point, "entity.name.function.var.declaration"):
            if fname and (
                "scripted_triggers" in fname
                or "scripted_effects" in fname
                or "scripted_modifiers" in fname
            ):
                word = self.handle_scripted_args(view, point)
            self.show_popup_default(
                view,
                point,
                PdxScriptObject(word, fname, current_line_num),  # type: ignore
                "Variable Declaration",
            )

        if view.match_selector(
            point, "entity.name.scripted.arg"
        ) or view.match_selector(point, "variable.language.scripted.arg"):
            self.show_popup_default(
                view,
                point,
                PdxScriptObject(word, fname, current_line_num),  # type: ignore
                "Scripted Argument",
            )
            return

        if (
            view.match_selector(point, "variable.parameter.scope.usage")
            or view.match_selector(point, "variable.parameter.remove.var")
            or view.match_selector(point, "variable.parameter.trigger.usage")
            or view.match_selector(point, "variable.parameter.variable.usage")
        ):
            if fname and (
                "scripted_triggers" in fname
                or "scripted_effects" in fname
                or "scripted_modifiers" in fname
            ):
                word = self.handle_scripted_args(view, point)
            if view.match_selector(point, "variable.parameter.scope.usage"):
                self.show_popup_default(
                    view,
                    point,
                    PdxScriptObject(word, fname, current_line_num),  # type: ignore
                    "Saved Scope",
                )
            else:
                self.show_popup_default(
                    view,
                    point,
                    PdxScriptObject(word, fname, current_line_num),  # type: ignore
                    "Saved Variable",
                )

        hover_objects = list()
        syntax_name = get_syntax_name(view)
        manager = GameObjectManager()
        if syntax_name == "Victoria Script":
            hover_objects = [
                (manager.ai_strats.name, "Ai Strategies"),
                (manager.bgs.name, "Building Group"),
                (manager.buildings.name, "Building"),
                (manager.char_traits.name, "Character Trait"),
                (manager.cultures.name, "Culture"),
                (manager.decrees.name, "Decree"),
                (manager.diplo_actions.name, "Diplomatic Action"),
                (manager.diplo_plays.name, "Diplomatic Play"),
                (manager.game_rules.name, "Game Rule"),
                (manager.goods.name, "Trade Good"),
                (manager.gov_types.name, "Government Type"),
                (manager.ideologies.name, "Ideology"),
                (manager.institutions.name, "Institution"),
                (manager.ig_traits.name, "Group Traits"),
                (manager.igs.name, "Interest Group"),
                (manager.jes.name, "Journal Entry"),
                (manager.law_groups.name, "Law Group"),
                (manager.laws.name, "Law"),
                (manager.mods.name, "Modifier"),
                (manager.parties.name, "Party"),
                (manager.pop_needs.name, "Pop Need"),
                (manager.pop_types.name, "Pop Type"),
                (manager.pm_groups.name, "Method Group"),
                (manager.pms.name, "Production Method"),
                (manager.religions.name, "Religion"),
                (manager.script_values.name, "Script Value"),
                (manager.scripted_effects.name, "Scripted Effect"),
                (manager.scripted_modifiers.name, "Scripted Modifer"),
                (manager.scripted_triggers.name, "Scripted Trigger"),
                (manager.state_traits.name, "State Trait"),
                (manager.strategic_regions.name, "Strategic Region"),
                (manager.subject_types.name, "Subject Types"),
                (manager.technologies.name, "Technology"),
                (manager.terrains.name, "Terrain"),
                (manager.state_regions.name, "State Region"),
                (manager.countries.name, "Country"),
                (manager.country_ranks.name, "Country Rank"),
                (manager.companies.name, "Company"),
                (manager.country_types.name, "Country Type"),
                (manager.culture_graphics.name, "Culture Graphic"),
                (manager.named_colors.name, "Named Color"),
                (manager.battle_conditions.name, "Battle Condition"),
                (manager.commander_ranks.name, "Commander Rank"),
                (manager.commander_orders.name, "Commander Order"),
                (manager.proposal_types.name, "Proposal Type"),
                (manager.discrimination_traits.name, "Discrimination Trait"),
                (manager.combat_unit_group.name, "Combat Unit Group"),
                (manager.combat_unit_type.name, "Combat Unit Type"),
                (manager.mobilization_options.name, "Mobilization Options"),
            ]

        if syntax_name == "Victoria Localization" or syntax_name == "Jomini Gui":
            hover_objects = [
                (manager.battle_conditions.name, "Battle Condition"),
                (manager.buildings.name, "Building"),
                (manager.combat_unit_group.name, "Combat Unit Group"),
                (manager.combat_unit_type.name, "Combat Unit Type"),
                (manager.cultures.name, "Culture"),
                (manager.custom_loc.name, "Customizable Localization"),
                (manager.decrees.name, "Decree"),
                (manager.diplo_actions.name, "Diplo_Action"),
                (manager.diplo_plays.name, "Diplo Play"),
                (manager.goods.name, "Goods"),
                (manager.ideologies.name, "Ideology"),
                (manager.institutions.name, "Institution"),
                (manager.igs.name, "Interest Group"),
                (manager.law_groups.name, "Law Group"),
                (manager.laws.name, "Law"),
                (manager.scripted_gui.name, "Scripted Gui"),
                (manager.pop_types.name, "Pop Type"),
                (manager.religions.name, "Religion"),
                (manager.mods.name, "Modifier"),
            ]

        # Iterate over the list and call show_popup_default for each game object
        for hover_object, name in hover_objects:
            game_object = self.game_objects[hover_object].access(word)
            if game_object:
                self.show_popup_default(
                    view,
                    point,
                    game_object,
                    name,
                )
                break


class BrowseBinkVideosCommand(sublime_plugin.TextCommand):
    def run(self, edit, video, play=False):  # type: ignore
        if video:
            if play:
                self.on_done(video, play=True)
            else:
                self.on_done(video)

    def input_description(self):
        return "Select Video"

    def input(self, args):
        if "video" not in args:
            return VideoInputHandler()

    def on_done(self, video, play=False):
        video = f"gfx{os.sep}event_pictures{os.sep}" + video
        settings = sublime.load_settings("Victoria Syntax.sublime-settings")
        v3_files_path = settings.get("Victoria3FilesPath")
        video_path = v3_files_path + os.sep + video
        if not os.path.exists(video_path):
            # Check mod paths if it's not vanilla
            for mod in v3_mod_files:
                mod_path = mod + os.sep + video
                if os.path.exists(mod_path):
                    video_path = mod_path

        open_path(video_path)


class VideoInputHandler(sublime_plugin.ListInputHandler):
    def name(self):
        return "video"

    def list_items(self):
        keys = []
        game_data = GameData()
        for x in game_data.EventVideos:
            keys.append(x.replace(f"gfx{os.sep}event_pictures{os.sep}", ""))
        return keys
