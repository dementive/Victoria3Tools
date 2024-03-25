"""
The main event listener for the plugin, this is where most of the plugin features actually happen.
The init function of the event listener is treated as the main entry point for the plugin.
"""

import os
import re
import time
import threading

import sublime, sublime_plugin
from .jomini import PdxScriptObject
from .v3_objects import *
from .game_objects import (
    check_mod_for_changes,
    get_objects_from_cache,
    get_gui_objects_from_cache,
    write_data_to_syntax,
    cache_all_objects,
    add_color_scheme_scopes,
    handle_image_cache,
)
from .css import CSS
from .game_data import GameData
from .scope_match import ScopeMatch
from .autocomplete import AutoComplete
from .hover import Hover
from .encoding import encoding_check
from .shaders import on_hover_shaders
from .utils import *


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
        if check_mod_for_changes(self.v3_mod_files):
            # Create new objects
            if script_enabled:
                sublime.set_timeout_async(lambda: self.create_game_objects(), 0)
            else:
                sublime.set_timeout_async(lambda: self.load_gui_objects(), 0)
        elif not script_enabled:
            self.game_objects = get_gui_objects_from_cache()
        else:
            # Load cached objects
            self.game_objects = get_objects_from_cache()

        handle_image_cache(self.settings)
        add_color_scheme_scopes()

    def create_game_objects(self):
        t0 = time.time()

        def load_first():
            self.game_objects["ai_strats"] = V3AiStrategy()
            self.game_objects["bgs"] = V3BuildingGroup()
            self.game_objects["buildings"] = V3Building()
            self.game_objects["char_traits"] = V3CharacterTrait()
            self.game_objects["cultures"] = V3Culture()
            self.game_objects["decrees"] = V3Decree()
            self.game_objects["diplo_actions"] = V3DiplomaticAction()
            self.game_objects["diplo_plays"] = V3DiplomaticPlay()
            self.game_objects["companies"] = V3CompanyType()

        def load_second():
            self.game_objects["mods"] = V3Modifier()
            self.game_objects["game_rules"] = V3GameRules()
            self.game_objects["gov_types"] = V3GovernmentType()
            self.game_objects["ideologies"] = V3Ideology()
            self.game_objects["institutions"] = V3Institutions()
            self.game_objects["ig_traits"] = V3InterestGroupTrait()
            self.game_objects["igs"] = V3InterestGroup()
            self.game_objects["commander_orders"] = V3CommanderOrder()

        def load_third():
            self.game_objects["jes"] = V3JournalEntry()
            self.game_objects["law_groups"] = V3LawGroup()
            self.game_objects["mobilization_options"] = V3MobilizationOption()
            self.game_objects["laws"] = V3Law()
            self.game_objects["parties"] = V3Party()
            self.game_objects["pop_needs"] = V3PopNeed()
            self.game_objects["pop_types"] = V3PopType()
            self.game_objects["pm_groups"] = V3ProductionMethodGroup()

        def load_fourth():
            self.game_objects["pms"] = V3ProductionMethod()
            self.game_objects["religions"] = V3Religion()
            self.game_objects["script_values"] = V3ScriptValue()
            self.game_objects["scripted_effects"] = V3ScriptedEffect()
            self.game_objects["scripted_modifiers"] = V3ScriptedModifier()
            self.game_objects["scripted_triggers"] = V3ScriptedTrigger()
            self.game_objects["proposal_types"] = V3ProposalType()
            self.game_objects["discrimination_traits"] = V3DiscriminationTrait()

        def load_fifth():
            self.game_objects["combat_unit_group"] = V3CombatUnitGroup()
            self.game_objects["strategic_regions"] = V3StrategicRegion()
            self.game_objects["goods"] = V3Goods()
            self.game_objects["subject_types"] = V3SubjectType()
            self.game_objects["technologies"] = V3Technology()
            self.game_objects["terrains"] = V3Terrain()
            self.game_objects["state_regions"] = V3StateRegion()
            self.game_objects["state_traits"] = V3StateTrait()
            self.game_objects["countries"] = V3Country()
            self.game_objects["countries"].remove("NOR")

        def load_sixth():
            self.game_objects["country_ranks"] = V3CountryRank()
            self.game_objects["country_types"] = V3CountryType()
            self.game_objects["culture_graphics"] = V3CultureGraphics()
            self.game_objects["modifier_types"] = V3ModifierType()
            self.game_objects["named_colors"] = V3NamedColor()
            self.game_objects["battle_conditions"] = V3BattleCondition()
            self.game_objects["commander_ranks"] = V3CommanderRank()
            self.game_objects["combat_unit_type"] = V3CombatUnitType()

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
        self.game_objects["gui_types"] = GuiType()
        self.game_objects["gui_templates"] = GuiTemplate()
        self.game_objects["gui_templates"].remove("inside")
        self.game_objects["gui_templates"].remove("you")
        self.game_objects["gui_templates"].remove("can")
        self.game_objects["gui_templates"].remove("but")
        self.game_objects["gui_templates"].remove("on")
        self.game_objects["gui_templates"].remove("within")
        self.game_objects["gui_templates"].remove("names")

        # Cache created objects
        sublime.set_timeout_async(lambda: cache_all_objects(self.game_objects), 0)

    def on_deactivated_async(self, view):
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

    def on_activated_async(self, view):
        if not self.settings.get("EnableVictoriaScriptingFeatures"):
            return

        vid = view.id()
        for field, views in self.fields.items():
            if vid in views:
                setattr(self, field, True)
                views.remove(vid)

    def create_completion_list(self, flag_name, completion_kind):
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

    def on_query_completions(self, view, prefix, locations):
        if not view:
            return None

        try:
            if view.syntax().name != "Victoria Script":
                return None
        except AttributeError:
            return None

        if not self.settings.get("EnableVictoriaScriptingFeatures"):
            return

        fname = view.file_name()

        for flag, completion in self.GameData.completion_flag_pairs:
            completion_list = self.create_completion_list(flag, completion)
            if completion_list is not None:
                return completion_list

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
            or "common/history" in fname
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

    def check_for_simple_completions(self, view, point):
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

    def on_selection_modified_async(self, view):
        if not view:
            return

        try:
            if view.syntax().name != "Victoria Script":
                return
        except AttributeError:
            return

        if not self.settings.get("EnableVictoriaScriptingFeatures"):
            return

        self.simple_scope_match(view)
        # Only do when there is 1 selection, doens't make sense with multiple selections
        if len(view.sel()) == 1:
            self.check_for_simple_completions(view, view.sel()[0].a)
            self.check_complex_completions(view, view.sel()[0].a)

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
            [
                x
                for x in self.v3_mod_files
                if is_file_in_directory(self.view.file_name(), x)
            ]
        )

        if in_mod_dir:
            encoding_check(view)

    def on_hover(self, view, point, hover_zone):
        if not view:
            return

        on_hover_shaders(view, point, self.settings, self.GameData)

        try:
            if view.syntax().name not in (
                "Victoria Script",
                "Victoria Gui",
            ):
                return
        except AttributeError:
            return

        if view.match_selector(point, "comment.line"):
            return

        if view.syntax().name == "Victoria Gui":
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

        if view.syntax().name == "Victoria Script" and self.settings.get(
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

                # Do everything that requires fetching GameObjects in non-blocking thread
                sublime.set_timeout_async(lambda: self.do_hover_async(view, point), 0)

        if self.settings.get("TextureOpenPopup") != True:
            return

        posLine = view.line(point)
        linestr = view.substr(posLine)
        if ".dds" not in linestr and ".tga" not in linestr:
            return

        if (
            view.syntax().name == "Victoria Script"
            and "common/coat_of_arms" in view.file_name()
            or "common\\coat_of_arms" in view.file_name()
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
                    self.v3_files_path, "/gfx/coat_of_arms/patterns/", raw_path
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
                    self.v3_files_path, "/gfx/coat_of_arms/colored_emblems/", raw_path
                )
                if not os.path.exists(full_texture_path):
                    full_texture_path = os.path.join(
                        self.v3_files_path,
                        "/gfx/coat_of_arms/textured_emblems/",
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
        if view.syntax().name == "Victoria Gui":
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

        if view.syntax().name == "Victoria Gui":
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

    def do_gui_hover_async(self, view, point):
        word = view.substr(view.word(point))

        if view.match_selector(point, "comment.line"):
            return

        if self.game_objects["gui_templates"].contains(word):
            self.show_gui_popup(
                view,
                point,
                word,
                self.game_objects["gui_templates"].access(word),
                "Gui Template",
            )

        if self.game_objects["gui_types"].contains(word):
            self.show_gui_popup(
                view,
                point,
                word,
                self.game_objects["gui_types"].access(word),
                "Gui Type",
            )

    def do_hover_async(self, view, point):
        word_region = view.word(point)
        word = view.substr(word_region)
        fname = view.file_name()
        current_line_num = view.rowcol(point)[0] + 1

        if view.match_selector(point, "comment.line"):
            return

        if view.match_selector(point, "entity.name.function.scope.declaration"):
            self.show_popup_default(
                view,
                point,
                word,
                PdxScriptObject(word, fname, current_line_num),
                "Scope Declaration",
            )

        if view.match_selector(point, "entity.name.function.var.declaration"):
            self.show_popup_default(
                view,
                point,
                word,
                PdxScriptObject(word, fname, current_line_num),
                "Variable Declaration",
            )

        if (
            view.match_selector(point, "variable.parameter.scope.usage")
            or view.match_selector(point, "variable.parameter.remove.var")
            or view.match_selector(point, "variable.parameter.trigger.usage")
            or view.match_selector(point, "variable.parameter.variable.usage")
        ):
            if view.match_selector(point, "variable.parameter.scope.usage"):
                self.show_popup_default(
                    view,
                    point,
                    word,
                    PdxScriptObject(word, fname, current_line_num),
                    "Saved Scope",
                )
            else:
                self.show_popup_default(
                    view,
                    point,
                    word,
                    PdxScriptObject(word, fname, current_line_num),
                    "Saved Variable",
                )

        hover_objects = [
            ("ai_strats", "Ai Strategies"),
            ("bgs", "Building Group"),
            ("buildings", "Building"),
            ("char_traits", "Character Trait"),
            ("cultures", "Culture"),
            ("decrees", "Decree"),
            ("diplo_actions", "Diplomatic Action"),
            ("diplo_plays", "Diplomatic Play"),
            ("game_rules", "Game Rule"),
            ("goods", "Trade Good"),
            ("gov_types", "Government Type"),
            ("ideologies", "Ideology"),
            ("institutions", "Institution"),
            ("ig_traits", "Group Traits"),
            ("igs", "Interest Group"),
            ("jes", "Journal Entry"),
            ("law_groups", "Law Group"),
            ("laws", "Law"),
            ("mods", "Modifier"),
            ("parties", "Party"),
            ("pop_needs", "Pop Need"),
            ("pop_types", "Pop Type"),
            ("pm_groups", "Method Group"),
            ("pms", "Production Method"),
            ("religions", "Religion"),
            ("script_values", "Script Value"),
            ("scripted_effects", "Scripted Effect"),
            ("scripted_modifiers", "Scripted Modifer"),
            ("scripted_triggers", "Scripted Trigger"),
            ("state_traits", "State Trait"),
            ("strategic_regions", "Strategic Region"),
            ("subject_types", "Subject Types"),
            ("technologies", "Technology"),
            ("terrains", "Terrain"),
            ("state_regions", "State Region"),
            ("countries", "Country"),
            ("country_ranks", "Country Rank"),
            ("companies", "Company"),
            ("country_types", "Country Type"),
            ("culture_graphics", "Culture Graphic"),
            ("named_colors", "Named Color"),
            ("battle_conditions", "Battle Condition"),
            ("commander_ranks", "Commander Rank"),
            ("commander_orders", "Commander Order"),
            ("proposal_types", "Proposal Type"),
            ("discrimination_traits", "Discrimination Trait"),
            ("combat_unit_group", "Combat Unit Group"),
            ("combat_unit_type", "Combat Unit Type"),
            ("mobilization_options", "Mobilization Options"),
        ]

        # Iterate over the list and call show_popup_default for each game object
        for hover_object, name in hover_objects:
            if self.game_objects[hover_object].contains(word):
                self.show_popup_default(
                    view,
                    point,
                    word,
                    self.game_objects[hover_object].access(word),
                    name,
                )


class BrowseBinkVideosCommand(sublime_plugin.TextCommand):
    def run(self, edit, video, play=False):
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
        video = "gfx/event_pictures/" + video
        settings = sublime.load_settings("Victoria Syntax.sublime-settings")
        v3_files_path = settings.get("Victoria3FilesPath")
        video_path = v3_files_path + "/" + video
        if not os.path.exists(video_path):
            # Check mod paths if it's not vanilla
            for mod in v3_mod_files:
                mod_path = mod + "/" + video
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
            keys.append(x.replace("gfx/event_pictures/", ""))
        return keys
