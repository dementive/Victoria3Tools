import os
import re

import Default.exec
import sublime
import sublime_plugin


class GotoScriptObjectDefinitionCommand(sublime_plugin.WindowCommand):
    def run(self, path: str, line: str):  # type: ignore
        if os.path.exists(path):
            file_path = "{}:{}:{}".format(path, line, 0)
            self.open_location(self.window, file_path)

    def open_location(self, window, line):
        flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP
        window.open_file(line, flags)


class GotoScriptObjectDefinitionRightCommand(sublime_plugin.WindowCommand):
    def run(self, path: str, line: str):  # type: ignore
        if os.path.exists(path):
            file_path = "{}:{}:{}".format(path, line, 0)
            self.open_location(
                self.window, file_path, side_by_side=True, clear_to_right=True
            )

    def open_location(
        self, window, location, side_by_side=False, replace=False, clear_to_right=False
    ):
        flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP

        if side_by_side:
            flags |= sublime.ADD_TO_SELECTION | sublime.SEMI_TRANSIENT
            if clear_to_right:
                flags |= sublime.CLEAR_TO_RIGHT

        elif replace:
            flags |= sublime.REPLACE_MRU | sublime.SEMI_TRANSIENT

        window.open_file(location, flags)


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


class QuietExecuteCommand(sublime_plugin.WindowCommand):
    """
    Simple version of Default.exec.py that only runs the process and shows no panel or messages
    """

    def __init__(self, window):
        super().__init__(window)
        self.proc = None

    def run(
        self,
        cmd=None,
        shell_cmd=None,
        working_dir="",
        encoding="utf-8",
        env={},
        **kwargs,
    ):
        self.encoding = encoding
        merged_env = env.copy()
        if self.window.active_view():
            user_env = self.window.active_view().settings().get("build_env")
            if user_env:
                merged_env.update(user_env)

        if working_dir != "":
            os.chdir(working_dir)

        try:
            # Run process
            self.proc = Default.exec.AsyncProcess(
                cmd, shell_cmd, merged_env, self, **kwargs
            )
            self.proc.start()
        except Exception:
            sublime.status_message("Build error")

    def on_data(self, proc, data):
        return

    def on_finished(self, proc):
        return
