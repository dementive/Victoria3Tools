# Class to hold css styles for sublime plugin

from sublime import packages_path


class CSS:
    def __init__(self):
        self.default = None
        self.effect = None
        self.trigger = None
        self.scope = None
        self.dark = None
        self.get_styles()

    def get_styles(self):
        default_path = packages_path() + "/Victoria3Tools/src/styles/default.css"
        effect_path = packages_path() + "/Victoria3Tools/src/styles/effect.css"
        trigger_path = packages_path() + "/Victoria3Tools/src/styles/trigger.css"
        scope_path = packages_path() + "/Victoria3Tools/src/styles/scope.css"
        dark_path = packages_path() + "/Victoria3Tools/src/styles/dark.css"

        with open(default_path, "r") as file:
            self.default = file.read()
        with open(effect_path, "r") as file:
            self.effect = file.read()
        with open(trigger_path, "r") as file:
            self.trigger = file.read()
        with open(scope_path, "r") as file:
            self.scope = file.read()
        with open(dark_path, "r") as file:
            self.dark = file.read()
