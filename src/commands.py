import os
import re
from typing import List

import sublime
import sublime_plugin

from JominiTools.src.utils import open_path
from .game_data import VictoriaGameData


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
        settings = sublime.load_settings("Victoria.sublime-settings")
        v3_files_path: str = settings.get("GameFilesPath")  # type: ignore
        v3_mod_files: List = settings.get("PathsToModFiles")  # type: ignore
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
        game_data = VictoriaGameData()
        for x in game_data.EventVideos:
            keys.append(x.replace(f"gfx{os.sep}event_pictures{os.sep}", ""))
        return keys


class LocalizeCurrentFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window = sublime.active_window()
        view = window.active_view()
        if not view:
            return
        view_region = sublime.Region(0, view.size())
        view_str = view.substr(view_region)
        loc_list = self.localize_tokens(view_str)

        # Insert into new view
        window.run_command("new_file")
        loc_view = window.active_view()
        if not loc_view:
            return
        loc_view.set_name("Localization")
        for i in loc_list:
            loc_view.insert(edit, len(loc_view), i)

    def localize_tokens(self, file_contents):
        out_list = []
        file_contents = file_contents.replace("desc = {", "").replace(
            "custom_tooltip = {", ""
        )
        out = re.sub("(#).*", "", file_contents)
        out = out.replace(" ", "")
        out = re.findall(
            r"(title|desc|name|custom_tooltip|text|flavor)\s?=\s?(.+)", out
        )

        for i in out:
            key = i[1].replace('"', "")
            # Exclude modifiers and variables
            if (
                key.endswith("_mod")
                or key.endswith("_var")
                or key.endswith("_cooldown")
            ):
                pass
            else:
                if (
                    not key.endswith("tt")
                    and not key.endswith("ttt")
                    and key.endswith(".t")
                    or key.endswith("title")
                ):
                    loced = key.replace("_", " ")
                    key = "\n" + key + ':0 "' + loced + '"'
                else:
                    loced = key.replace("_", " ")
                    key = "\n" + key + ':0 "' + loced + '"'
                    key = key.replace("\t", "")
                out_list.append(key)

        return out_list


class FolderHandler(sublime_plugin.TextCommand):
    def input_description(self):
        return "Fold Level"

    def input(self, args):
        if "level" not in args:
            return FoldingInputHandler()

    def run(self, edit: sublime.Edit, level: str):  # type: ignore
        if level != "Unfold All":
            self.view.run_command("fold_by_level", {"level": int(level)})
        else:
            self.view.run_command("unfold_all")


class FoldingInputHandler(sublime_plugin.ListInputHandler):
    def name(self):
        return "level"

    def list_items(self):
        keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "Unfold All"]
        return keys
