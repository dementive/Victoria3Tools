"""
Plugin features related to the game's data system functions.
Data system features that are not coupled to game objects should go here.
"""

from typing import List
import sublime
import sublime_plugin

from JominiTools.src import JominiDataSystemEventListener
from .plugin import VictoriaPlugin


class ImperatorDataSystemEventListener(
    JominiDataSystemEventListener, sublime_plugin.EventListener
):
    def __init__(self):
        super().__init__(VictoriaPlugin())

    def on_selection_modified_async(self, view):
        super().on_selection_modified_async(view)

    def on_query_completions(
        self, view: sublime.View, prefix: str, locations: List[int]
    ):
        super().on_query_completions(view, prefix, locations)
