"""
Checks the current position of the cursor and determine what kind of block we are inside of in script.
Set a status message in the status bar to let the user know what kind of block it is and also set a flag to let autocomplete know what type of completions to provide.
"""

import sublime
from .utils import get_index


class ScopeMatch:
    def get_regions(self, view, selector, view_str):
        start_brackets = view.find_by_selector(selector)
        return [
            sublime.Region(br.a, get_index(view_str, br.a)) for br in start_brackets
        ]

    def simple_scope_match(self, view):
        selection = view.sel()
        if not selection[0].empty():
            return

        view_str = view.substr(sublime.Region(0, view.size()))

        # Get the starting bracket index from the syntax scopes
        trigger_regions = self.get_regions(view, "meta.trigger.bracket", view_str)
        effect_regions = self.get_regions(view, "meta.effect.bracket", view_str)
        value_regions = self.get_regions(view, "meta.value.bracket", view_str)
        modifier_regions = self.get_regions(view, "meta.modifier.bracket", view_str)

        self.show_status(selection[0].a, trigger_regions, "trigger", view)

        # Have to account for trigger fields inside of effect fields, definetly a better way to do this.
        for block in effect_regions:
            if block.a <= selection[0].a <= block.b:
                view.set_status("effect", "Effect Field")
                self.effect_field = True
                for block in trigger_regions:
                    if block.a <= selection[0].a <= block.b:
                        view.erase_status("effect")
                        self.effect_field = False
                        view.set_status("trigger", "Trigger Field")
                        self.trigger_field = True
                        break
                    else:
                        view.erase_status("trigger")
                        self.trigger_field = False
                break
            else:
                view.erase_status("effect")
                self.effect_field = False

        self.show_status(selection[0].a, modifier_regions, "modifier", view)

        self.show_status(selection[0].a, value_regions, "value", view)

        # For actual mtth fields that have a modifier = {} block inside of them, remove the modifier status
        if self.mtth_field and self.modifier_field:
            view.erase_status("modifier")

    def show_status(self, selection, regions, status, view):
        for block in regions:
            if block.a <= selection <= block.b:
                view.set_status(status, status.title() + " Field")
                if status == "trigger":
                    self.trigger_field = True
                elif status == "effect":
                    self.effect_field = True
                elif status == "modifier":
                    self.modifier_field = True
                elif status == "value":
                    self.mtth_field = True
                break
            else:
                view.erase_status(status)
                if status == "trigger":
                    self.trigger_field = False
                elif status == "effect":
                    self.effect_field = False
                elif status == "modifier":
                    self.modifier_field = False
                elif status == "value":
                    self.mtth_field = False
