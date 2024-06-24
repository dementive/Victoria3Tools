import sublime

from JominiTools.src import JominiPlugin


class VictoriaPlugin(JominiPlugin):
    @property
    def name(self):
        return "Victoria3Tools"

    @property
    def settings(self):
        return sublime.load_settings("Victoria.sublime-settings")

    @property
    def script_syntax_name(self):
        return "Victoria Script"

    @property
    def localization_syntax_name(self):
        return "Victoria Localization"

    @property
    def gui_syntax_name(self) -> str:
        return "Victoria Gui"
