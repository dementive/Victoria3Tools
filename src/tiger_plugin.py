"""
All the code for handling the integration of vic3-tiger into the plugin.
"""

import json
import os

import Default.exec
import sublime
import sublime_plugin

from .css import CSS
from .tiger import TigerJsonObject

css_basic_style = CSS().default
tiger_objects = dict()


class Vic3TigerEventListener(sublime_plugin.EventListener):
    def on_init(self, views):
        self.settings = sublime.load_settings("Victoria Syntax.sublime-settings")

    def on_load_async(self, view):
        if not self.settings.get("Vic3TigerShowErrorsInline"):
            return

        path = view.file_name()
        if path not in tiger_objects:
            return

        file_errors = tiger_objects[path]
        error_regions = list()
        warning_regions = list()
        tips_regions = list()
        if isinstance(file_errors, list):
            for i in file_errors:
                point = view.text_point(i["linenr"] - 1, i["column"] - 1)
                length = i["length"] if i["length"] is not None else 0
                if i["severity"] == "fatal" or i["severity"] == "error":
                    error_regions.append(sublime.Region(point, point + length))
                if i["severity"] == "warning" or i["severity"] == "untidy":
                    warning_regions.append(sublime.Region(point, point + length))
                if i["severity"] == "tips":
                    tips_regions.append(sublime.Region(point, point + length))
        else:
            point = view.text_point(
                file_errors["linenr"] - 1, file_errors["column"] - 1
            )
            length = file_errors["length"] if file_errors["length"] is not None else 0
            if file_errors["severity"] == "fatal" or file_errors["severity"] == "error":
                error_regions.append(sublime.Region(point, point + length))
            if (
                file_errors["severity"] == "warning"
                or file_errors["severity"] == "untidy"
            ):
                warning_regions.append(sublime.Region(point, point + length))
            if file_errors["severity"] == "tips":
                tips_regions.append(sublime.Region(point, point + length))

        if error_regions:
            add_inline_error(view, error_regions, "region.redish")
        if warning_regions:
            add_inline_error(view, warning_regions, "region.yellowish")
        if tips_regions:
            add_inline_error(view, tips_regions, "region.greenish")

    def on_hover(self, view, point, hover_zone):
        if not self.settings.get("Vic3TigerShowErrorsInline"):
            return

        if not view:
            return

        path = view.file_name()
        if path not in tiger_objects:
            return

        file_errors = tiger_objects[path]
        file_error = ""
        if isinstance(file_errors, list):
            for i in file_errors:
                # We can deduce the current error being hovered over by knowing the Region of the row and column it is in
                region_start = view.text_point(i["linenr"] - 1, i["column"] - 1)
                length = i["length"] if i["length"] is not None else 0
                region_end = region_start + length
                error_region = sublime.Region(region_start, region_end)
                if error_region.contains(point):
                    file_error = i
        else:
            region_start = view.text_point(
                file_errors["linenr"] - 1, file_errors["column"] - 1
            )
            region_end = region_start + file_errors["length"]
            error_region = sublime.Region(region_start, region_end)
            if error_region.contains(point):
                file_error = file_errors

        if not file_error:
            return

        error = [x for x in view.get_regions("region.redish") if x.contains(point)]
        warning = [x for x in view.get_regions("region.yellowish") if x.contains(point)]
        tips = [x for x in view.get_regions("region.greenish") if x.contains(point)]

        info = file_error["info"]
        if not info:
            info = ""
        info = "<p>" + info + "</p>"

        header_color = ""
        if error:
            header_color = "red"
        if warning:
            header_color = "yellow"
        if tips:
            header_color = "green"

        header = f"{file_error['severity']}({file_error['key']})"
        example = f'<h2 class="code-header {header_color}-text">{header}</h2>'
        example += f'<div class="box-for-codebox"><div class="codebox"><code>{file_error["message"]}</code><br><code>{info}</code></div></div>'
        hover_body = """
            <body id="vic-body">
                <style>%s</style>
                %s
            </body>
        """ % (
            css_basic_style,
            example,
        )

        view.show_popup(
            hover_body,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=1024,
        )


# Tiger json object creation
def get_tiger_objects():
    global tiger_objects
    path = sublime.packages_path() + "/Victoria3Tools/tiger.json"
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for i in data:
        # Add location data to list in the same way the display() function does so the indexes stay the same
        previous_locations = list()
        for j in i["locations"]:
            fullpath = j["fullpath"]
            if fullpath not in previous_locations:
                if fullpath in tiger_objects:
                    old_data = tiger_objects[j["fullpath"]]
                    new_data = {
                        "severity": i["severity"],
                        "key": i["key"],
                        "info": i["info"],
                        "message": i["message"],
                        "linenr": j["linenr"],
                        "column": j["column"],
                        "length": j["length"],
                    }
                    if isinstance(old_data, list):
                        old_data.append(new_data)
                    else:
                        old_data = [old_data, new_data]

                    tiger_objects[j["fullpath"]] = old_data
                else:
                    tiger_objects[j["fullpath"]] = {
                        "severity": i["severity"],
                        "key": i["key"],
                        "info": i["info"],
                        "message": i["message"],
                        "linenr": j["linenr"],
                        "column": j["column"],
                        "length": j["length"],
                    }

            previous_locations.append(j["fullpath"])


def add_inline_error(view, regions, scope):
    view.add_regions(
        scope,
        regions,
        scope,
        flags=(
            sublime.DRAW_NO_FILL
            | sublime.DRAW_NO_OUTLINE
            | sublime.DRAW_SQUIGGLY_UNDERLINE
        ),
    )


class VicTigerInputHandler(sublime_plugin.ListInputHandler):
    def name(self):
        return "view_type"

    def list_items(self):
        return ["Panel", "Tab"]


class VicShowTigerOutputCommand(sublime_plugin.WindowCommand):
    def run(self, view_type):
        path = sublime.packages_path() + "/Victoria3Tools/tiger.json"
        self.settings = sublime.load_settings("Victoria Syntax.sublime-settings")
        self.v3_files_path = self.settings.get("Victoria3FilesPath")

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        view_text = str()
        self.path_locations = list()
        for i in data:
            # Add location data to list in the same way the display() function does so the indexes stay the same
            previous_locations = list()
            for j in i["locations"]:
                if j["fullpath"] not in previous_locations:
                    self.path_locations.append((j["linenr"], j["column"]))
                previous_locations.append(j["fullpath"])

            obj = TigerJsonObject(
                i["confidence"],
                i["info"],
                i["key"],
                i["locations"],
                i["message"],
                i["severity"],
            )

            view_text += obj.display()

        if view_type == "Panel":
            if self.window.find_output_panel("exec") is None:
                self.output_view = self.window.create_output_panel("exec")
                self.window.run_command("show_panel", {"panel": "output.exec"})
            else:
                self.window.destroy_output_panel("exec")
                self.output_view = self.window.create_output_panel("exec")
                self.window.run_command("show_panel", {"panel": "output.exec"})
        else:
            self.output_view = self.window.new_file(flags=sublime.TRANSIENT)
            self.output_view.set_name("Tiger Output")
            self.output_view.set_scratch(True)

        if self.output_view:
            self.view_creation(view_text)

    def input(self, args):
        if "view_type" not in args:
            return VicTigerInputHandler()

    def view_creation(self, view_text):
        self.window.focus_view(self.output_view)
        self.output_view.set_read_only(True)
        self.output_view.assign_syntax("Vic3Tiger.sublime-syntax")
        s = self.output_view.settings()
        s.set("word_wrap", True)
        s.set("line_numbers", False)
        s.set("gutter", False)
        s.set("scroll_past_end", False)
        if not view_text:
            view_text = "vic3-tiger found no errors :)"
        self.output_view.run_command(
            "append", {"characters": view_text, "force": True, "scroll_to_end": True}
        )

        self.add_annotations()

    def add_annotations(self):
        regions = self.output_view.find_by_selector("string.file.path")
        annotations = list()

        for i in range(len(regions)):
            href_str = (
                self.output_view.substr(regions[i]).lstrip(" ")
                + ":"
                + str(self.path_locations[i][0])
                + ":"
                + str(self.path_locations[i][1])
            )
            annotation_body = """
                <body id="vic-body">
                    <style>%s</style>
                    <a href="%s" >Open %s</a>
                </body>
            """ % (
                css_basic_style,
                href_str,
                self.output_view.substr(regions[i]),
            )
            annotations.append(annotation_body)

        self.output_view.add_regions(
            "file_to_open",
            regions,
            "string.file.path",
            flags=(sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE),
            annotations=annotations,
            on_navigate=self.annotation_callback,
        )

    def annotation_callback(self, string):
        string = string.replace("\n", "").split(":")
        path = self.settings.get("Vic3TigerModPath") + "\\" + string[0]

        if not os.path.exists(path):
            path = self.v3_files_path + "\\" + string[0]

        if os.path.exists(path):
            file_path = "{}:{}:{}".format(path, string[1], string[2])
            flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP
            self.window.open_file(file_path, flags)


class VicExecuteTigerCommand(sublime_plugin.WindowCommand):
    """
    Version of Default.exec.py specifically for executing tiger and piping it's output to a file.
    It is basically the same except it does not pull up the output panel and it only outputs the text the subprocess sends.
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
        word_wrap=True,
        syntax="Packages/JSON/JSON.sublime-syntax",
        **kwargs,
    ):
        self.output_view = self.window.find_output_panel("exec")
        if self.output_view is None:
            # Try not to call get_output_panel until the regexes are assigned
            self.output_view = self.window.create_output_panel("exec")

        # Default the to the current files directory if no working directory
        # was given
        if (
            working_dir == ""
            and self.window.active_view()
            and self.window.active_view().file_name()
        ):
            working_dir = os.path.dirname(self.window.active_view().file_name())

        self.output_view.settings().set("result_base_dir", working_dir)
        self.output_view.settings().set("word_wrap", word_wrap)
        self.output_view.settings().set("line_numbers", False)
        self.output_view.settings().set("gutter", False)
        self.output_view.settings().set("scroll_past_end", False)
        self.output_view.assign_syntax(syntax)

        # Call create_output_panel a second time after assigning the above
        # settings, so that it'll be picked up as a result buffer
        self.window.create_output_panel("exec")

        self.window.focus_view(self.output_view)

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
        except Exception as e:
            print(e)
            sublime.status_message("Build error")

    def write(self, characters):
        self.output_view.run_command(
            "append", {"characters": characters, "force": True, "scroll_to_end": True}
        )

    def on_data(self, proc, data):
        if proc != self.proc:
            return

        self.write(data)

    def on_finished(self, proc):
        if proc != self.proc:
            return

        text = self.output_view.substr(sublime.Region(0, self.output_view.size()))
        # Find where the json starts by splitting off the header output
        # This will break if there is a "[" in the header but that should never happen
        json_start_index = text.find("[")

        if json_start_index != -1:
            tiger_json_output = text[json_start_index:]
            output_file = sublime.packages_path() + "/Victoria3Tools/tiger.json"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(tiger_json_output)
            sublime.status_message("vic3-tiger.exe has finished running.")
            sublime.set_timeout_async(lambda: get_tiger_objects(), 0)


class VicRunTigerCommand(sublime_plugin.WindowCommand):
    def run(self):
        settings = sublime.load_settings("Victoria Syntax.sublime-settings")
        mod_path = settings.get("Vic3TigerModPath")

        if not os.path.exists(mod_path):
            return

        tiger_exe_path = settings.get("Vic3TigerBinaryPath")

        if not os.path.exists(tiger_exe_path):
            tiger_exe_path = (
                sublime.packages_path() + "/Victoria3Tools/Vic3Tiger/vic3-tiger.exe"
            )
        window = sublime.active_window()

        if not settings.get("Vic3TigerUseDefaultConfig"):
            conf_file = (
                sublime.packages_path() + "/Victoria3Tools/Vic3Tiger/vic3-tiger.conf"
            )
            cmd = [tiger_exe_path, mod_path, "--json", "--config", conf_file]
        else:
            cmd = [tiger_exe_path, mod_path, "--json"]

        sublime.status_message("vic3-tiger.exe has started running...")
        window.run_command("vic_execute_tiger", {"cmd": cmd})


class VicEditTigerConfigCommand(sublime_plugin.WindowCommand):
    def run(self):
        conf_file = (
            sublime.packages_path() + "/Victoria3Tools/Vic3Tiger/vic3-tiger.conf"
        )
        view = self.window.open_file(conf_file)
        view.assign_syntax("scope:source.ruby")
