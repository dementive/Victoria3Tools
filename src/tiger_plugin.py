"""
All the code for handling the integration of vic3-tiger into the plugin.
"""

import sublime
import sublime_plugin

from JominiTools.src import (
    JominiTigerEventListener,
    JominiTigerOutputCommand,
    JominiExecuteTigerCommand,
    JominiRunTigerCommand,
    TigerInputHandler,
)


class VicTigerEventListener(JominiTigerEventListener, sublime_plugin.EventListener):
    def __init__(self):
        super().__init__("Victoria3Tools")

    def on_load_async(self, view):
        settings = sublime.load_settings("Victoria.sublime-settings")
        self._on_load_async(view, settings)

    def on_hover(self, view, point, hover_zone):
        settings = sublime.load_settings("Victoria.sublime-settings")
        self._on_hover(view, point, hover_zone, settings)


class VicTigerOutputCommand(JominiTigerOutputCommand, sublime_plugin.WindowCommand):
    def __init__(self, window):
        self.window = window
        super().__init__(
            "Victoria3Tools",
            sublime.load_settings("Victoria.sublime-settings"),
            "Victoria Tiger",
            self.window,
        )

    def run(self, view_type):  # type: ignore
        self._run(view_type)

    def input(self, args):
        if "view_type" not in args:
            return TigerInputHandler()


class VicExecuteTigerCommand(JominiExecuteTigerCommand, sublime_plugin.WindowCommand):
    def __init__(self, window):
        self.window = window
        super().__init__("Victoria3Tools", "vic3-tiger", self.window)

    def run(
        self,
        cmd=None,
        shell_cmd=None,
        working_dir="",
        encoding="utf-8",
        env={},
        word_wrap=True,
        syntax="Packages/JSON/JSON.sublime-syntax",
        **kwargs,
    ):
        self._run(
            cmd,
            shell_cmd,
            working_dir,
            encoding,
            env,
            word_wrap,
            syntax,
        )


class RunTigerCommand(JominiRunTigerCommand, sublime_plugin.WindowCommand):
    def __init__(self, window):
        self.window = window
        super().__init__(
            sublime.load_settings("Victoria.sublime-settings"),
            "/Victoria3Tools/Vic3Tiger/vic3-tiger",
            "vic3-tiger",
            "vic_execute_tiger",
        )

    def run(self):
        self._run()


class VicEditTigerConfigCommand(sublime_plugin.WindowCommand):
    def run(self):
        conf_file = (
            sublime.packages_path() + "/Victoria3Tools/Vic3Tiger/vic3-tiger.conf"
        )
        view = self.window.open_file(conf_file)
        view.assign_syntax("scope:source.ruby")
