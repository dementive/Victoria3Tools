"""
Code for the autocomplete features of the plugin
"""

from JominiTools.src import JominiAutoComplete


class AutoComplete(JominiAutoComplete):
    def init_autocomplete(
        self, auto_complete_fields, auto_complete_selector_flag_pairs
    ):
        super().__init__(auto_complete_fields, auto_complete_selector_flag_pairs)
