"""
Plugin features related to the game's data system functions.
Data system features that are not coupled to game objects should go here.
"""

from typing import List

import sublime
import sublime_plugin

from .utils import IterViews, get_syntax_name


class VictoriaDataSystemEventListener(sublime_plugin.EventListener):
    def on_init(self, views: List[sublime.View]):
        self.settings = sublime.load_settings("Victoria Syntax.sublime-settings")

    def on_selection_modified_async(self, view):
        if not view:
            return

        syntax_name = get_syntax_name(view)

        if syntax_name != "Victoria Localization" and syntax_name != "Jomini Gui":
            return

        if len(view.sel()) == 1:
            point = view.sel()[0].a
            if view.match_selector(point, "empty.scope.prompt") or view.match_selector(
                point, "empty.scope.variable"
            ):
                view.run_command("auto_complete")

    def on_query_completions(
        self, view: sublime.View, prefix: str, locations: List[int]
    ):
        if not view:
            return None

        syntax_name = get_syntax_name(view)

        if syntax_name != "Victoria Localization" and syntax_name != "Jomini Gui":
            return

        fname = view.file_name()
        if not fname:
            return

        if len(view.sel()) == 1:
            point = view.sel()[0].a
            if view.match_selector(point, "empty.scope.prompt"):
                return get_prompt_completions(
                    "Scope", "entity.name.function.scope.declaration"
                )
            if view.match_selector(point, "empty.scope.variable"):
                return get_prompt_completions(
                    "Variable", "entity.name.function.var.declaration"
                )


def get_prompt_completions(kind: str, selector: str):
    found_words = set()

    for view in IterViews(sublime.windows()):
        if get_syntax_name(view) != "Victoria Script":
            continue

        scope_regions = view.find_by_selector(selector)
        for region in scope_regions:
            found_words.add(view.substr(region))

    if not found_words:
        return None

    return sublime.CompletionList(
        [
            sublime.CompletionItem(
                trigger=key,
                completion=key,
                completion_format=sublime.COMPLETION_FORMAT_SNIPPET,
                kind=(sublime.KIND_ID_NAMESPACE, kind[0], kind),
            )
            for key in sorted(found_words)
        ],
        flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS,
    )
