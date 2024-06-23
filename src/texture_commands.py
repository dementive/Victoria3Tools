"""
Commands for opening and viewing textures in sublime or another program
"""

from typing import List
import sublime
import sublime_plugin

from JominiTools.src import (
    JominiShowAllTexturesCommand,
    JominiTextureEventListener,
    JominiToggleAllTexturesCommand,
)


class V3TextureEventListener(JominiTextureEventListener, sublime_plugin.EventListener):
    def on_init(self, views: List[sublime.View]):
        settings = sublime.load_settings("Victoria.sublime-settings")
        self.init(settings)

    def on_post_text_command(self, view: sublime.View, command_name: str, args):
        super().on_post_text_command(view, command_name, args)

    def on_load_async(self, view: sublime.View):
        super().on_load_async(view)


class V3ToggleAllTexturesCommand(
    JominiToggleAllTexturesCommand, sublime_plugin.ApplicationCommand
):
    def __init__(self):
        super().__init__()

    def run(self):
        self._run()


class V3ShowAllTexturesCommand(
    JominiShowAllTexturesCommand, sublime_plugin.WindowCommand
):
    def run(self):
        settings = sublime.load_settings("Victoria.sublime-settings")
        self._run(self.window, settings)
