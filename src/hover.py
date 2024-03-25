"""
Various features for showing information to the user when hovering over specific tokens.
Shows documentation for effects/triggers/scopes from the game logs in pop ups.
Also shows goto definition popups for all game objects as well as saved scopes and variables.
"""

import os
import re
import sublime, sublime_plugin
from .jomini import PdxScriptObject
from .css import CSS

css = CSS()


class Hover:
    def show_hover_docs(self, view, point, scope, collection, settings):
        style = settings.get("DocsPopupStyle")
        if style == "dark":
            style = css.dark
        elif style == "none":
            style = css.default
        elif style == "dynamic":
            if scope == "keyword.effect":
                style = css.effect
            elif scope == "string.trigger":
                style = css.trigger
            elif scope == "storage.type.scope":
                style = css.scope
        item = view.substr(view.word(point))
        if item in collection:
            desc = collection[item]
            hoverBody = """
                <body id="vic-body">
                    <style>%s</style>
                    <p>%s</p>
                </body>
            """ % (
                style,
                desc,
            )

            view.show_popup(
                hoverBody,
                flags=(
                    sublime.HIDE_ON_MOUSE_MOVE_AWAY
                    | sublime.COOPERATE_WITH_AUTO_COMPLETE
                    | sublime.HIDE_ON_CHARACTER_EVENT
                ),
                location=point,
                max_width=1024,
            )
            return

    def show_gui_docs_popup(self, view, point, item, GameData):
        data = GameData.GuiContent[item]
        color = data[0]
        desc = data[1]
        example = data[2]
        if example:
            example = f'<div class="box-for-codebox"><div class="codebox"><code>{example}</code></div></div>'
        if item in example:
            if color == "green":
                example = example.replace(
                    item, f'<code class="green-text">{item}</code>'
                )
            if color == "red":
                example = example.replace(item, f'<code class="red-text">{item}</code>')
            if color == "yellow":
                example = example.replace(
                    item, f'<code class="yellow-text">{item}</code>'
                )
            if color == "blue":
                example = example.replace(
                    item, f'<code class="blue-text">{item}</code>'
                )
            if color == "purple":
                example = example.replace(
                    item, f'<code class="purple-text">{item}</code>'
                )
            if color == "orange":
                example = example.replace(
                    item, f'<code class="orange-text">{item}</code>'
                )

        if item == "template" or item == "using":
            template_example = f'<div class="box-for-codebox"><div class="codebox code">template example_name {{<br>&nbsp;&nbsp;&nbsp;&nbsp;size = {{ 50 50 }}<br>}}<br></div></div>'
            template_example = template_example.replace(
                "template", f'<code class="purple-text">template</code>'
            )
            template_example_text = (
                '<p class="code-header">Example template definition:</p>'
            )
            template_example_text2 = (
                '<br><br><br><p class="code-header">Example template usage:</p>'
            )
            example = example.replace("using", f'<code class="green-text">using</code>')
            example = (
                template_example_text
                + template_example
                + template_example_text2
                + example
            )

        if item == "block" or item == "blockoverride":
            block_example = f'<div class="box-for-codebox"><div class="codebox code">block "example_name" {{<br>&nbsp;&nbsp;&nbsp;&nbsp;visible = no<br>}}<br></div></div>'
            block_example = block_example.replace(
                "block", f'<code class="red-text">block</code>'
            )
            block_example_text = '<p class="code-header">Example block definition:</p>'
            block_example_text2 = (
                '<br><br><br><p class="code-header">Example blockoverride:</p>'
            )
            example = f'<div class="box-for-codebox"><div class="codebox code">blockoverride "example_name" {{<br>&nbsp;&nbsp;&nbsp;&nbsp;visible = yes<br>}}<br></div></div>'
            example = example.replace(
                "blockoverride", f'<code class="red-text">blockoverride</code>'
            )
            example = block_example_text + block_example + block_example_text2 + example

        if item == "type" or item == "types":
            example = f'<div class="box-for-codebox"><div class="codebox code">types My_Types<br>{{<br>&nbsp;&nbsp;&nbsp;&nbsp;type widget_with_size = widget {{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;size = {{ 50 50 }}<br>&nbsp;&nbsp;&nbsp;&nbsp;}}<br>}}<br></div></div>'
            example = example.replace(
                "types", f'<code class="purple-text">types</code>'
            )
            example = example.replace("type", f'<code class="purple-text">type</code>')
            type_example_text = '<p class="code-header">Example type definition:</p>'
            example = type_example_text + example

        hoverBody = """
            <body id="vic-body">
                <style>%s</style>
                <p class=\"codedesc\">%s</p>
                %s
            </body>
        """ % (
            css.default,
            desc,
            example,
        )

        view.show_popup(
            hoverBody,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=1024,
        )

    def show_gui_popup(self, view, point, word, PdxObject, header):
        word_line_num = view.rowcol(point)[0] + 1
        word_file = view.file_name().replace("\\", "/").rstrip("/").rpartition("/")[2]
        definition = ""

        if word_line_num != PdxObject.line:
            definition = f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            goto_args = {"path": PdxObject.path, "line": PdxObject.line}
            goto_url = sublime.command_url("goto_script_object_definition", goto_args)
            definition += (
                """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;"""
                % (
                    goto_url,
                    PdxObject.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    PdxObject.line,
                    PdxObject.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    PdxObject.line,
                )
            )
            goto_right_args = {"path": PdxObject.path, "line": PdxObject.line}
            goto_right_url = sublime.command_url(
                "goto_script_object_definition_right", goto_right_args
            )
            definition += (
                """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                % (goto_right_url)
            )

        references = []
        ref = ""
        for win in sublime.windows():
            for i in [v for v in win.views() if v and v.file_name()]:
                if not i.file_name().endswith(".gui"):
                    continue

                view_region = sublime.Region(0, i.size())
                view_str = i.substr(view_region)
                for j, line in enumerate(view_str.splitlines()):
                    definition_found = False
                    if PdxObject.key in line:
                        filename = (
                            i.file_name()
                            .replace("\\", "/")
                            .rstrip("/")
                            .rpartition("/")[2]
                        )
                        line_num = j + 1
                        if word_line_num == line_num and word_file == filename:
                            # Don't do current word
                            continue
                        elif (
                            line_num == PdxObject.line
                            and i.file_name() == PdxObject.path
                        ):
                            # Don't do definition
                            continue
                        if not definition_found:
                            references.append(f"{i.file_name()}|{line_num}")

        if references:
            ref = f'<p><b>References to&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            for j, i in enumerate(references):
                if j > 10:
                    break
                fname = i.split("|")[0]
                shortname = fname.replace("\\", "/").rstrip("/").rpartition("/")[2]
                line = i.split("|")[1]
                goto_args = {"path": fname, "line": line}
                goto_url = sublime.command_url(
                    "goto_script_object_definition", goto_args
                )
                ref += (
                    """<a href="%s" title="Open %s and goto line %s">%s:%s</a>&nbsp;"""
                    % (
                        goto_url,
                        shortname,
                        line,
                        shortname,
                        line,
                    )
                )
                goto_right_args = {"path": fname, "line": line}
                goto_right_url = sublime.command_url(
                    "goto_script_object_definition_right", goto_right_args
                )
                ref += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )

        link = definition + ref
        if link:
            hoverBody = """
                <body id="vic-body">
                    <style>%s</style>
                    <h1>%s</h1>
                    %s
                </body>
            """ % (
                css.default,
                header,
                link,
            )

            view.show_popup(
                hoverBody,
                flags=(
                    sublime.HIDE_ON_MOUSE_MOVE_AWAY
                    | sublime.COOPERATE_WITH_AUTO_COMPLETE
                    | sublime.HIDE_ON_CHARACTER_EVENT
                ),
                location=point,
                max_width=1024,
            )

    def get_definitions_for_popup(self, view, point, PdxObject, header, def_value=""):
        word_line_num = view.rowcol(point)[0] + 1
        definition = ""
        definitions = []
        if header == "Saved Scope" or header == "Saved Variable":
            for win in sublime.windows():
                for i in [v for v in win.views() if v and v.file_name()]:
                    if i.file_name().endswith(".txt"):
                        variables = [
                            x
                            for x in i.find_by_selector(
                                "entity.name.function.var.declaration"
                            )
                            if i.substr(x) == PdxObject.key
                        ]
                        variables.extend(
                            [
                                x
                                for x in i.find_by_selector(
                                    "entity.name.function.scope.declaration"
                                )
                                if i.substr(x) == PdxObject.key
                            ]
                        )
                        for r in variables:
                            line = i.rowcol(r.a)[0] + 1
                            path = i.file_name()
                            if line == word_line_num and path == PdxObject.path:
                                continue
                            else:
                                definitions.append(
                                    PdxScriptObject(PdxObject.key, path, line)
                                )

            if len(definitions) == 1:
                if def_value:
                    definition = f"<br>{def_value}<br><br>"
                    definition += f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                else:
                    definition = f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            elif len(definitions) > 1:
                if def_value:
                    definition = f"<br>{def_value}<br><br>"
                    definition += f'<p><b>Definitions of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
                else:
                    definition = f'<p><b>Definitions of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            for obj in definitions:
                goto_args = {"path": obj.path, "line": obj.line}
                goto_url = sublime.command_url(
                    "goto_script_object_definition", goto_args
                )
                definition += (
                    """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;"""
                    % (
                        goto_url,
                        obj.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                        obj.line,
                        obj.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                        obj.line,
                    )
                )
                goto_right_args = {"path": obj.path, "line": obj.line}
                goto_right_url = sublime.command_url(
                    "goto_script_object_definition_right", goto_right_args
                )
                definition += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )
                return definition

        if word_line_num != PdxObject.line:
            if def_value:
                definition = f"<br>{def_value}<br><br>"
                definition += f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            else:
                definition = f'<p><b>Definition of&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            goto_args = {"path": PdxObject.path, "line": PdxObject.line}
            goto_url = sublime.command_url("goto_script_object_definition", goto_args)
            definition += (
                """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;"""
                % (
                    goto_url,
                    PdxObject.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    PdxObject.line,
                    PdxObject.path.replace("\\", "/").rstrip("/").rpartition("/")[2],
                    PdxObject.line,
                )
            )
            goto_right_args = {"path": PdxObject.path, "line": PdxObject.line}
            goto_right_url = sublime.command_url(
                "goto_script_object_definition_right", goto_right_args
            )
            definition += (
                """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                % (goto_right_url)
            )

        return definition

    def get_references_for_popup(self, view, point, PdxObject, header):
        word_line_num = view.rowcol(point)[0] + 1
        word_file = view.file_name().replace("\\", "/").rstrip("/").rpartition("/")[2]
        references = []
        ref = ""
        for win in sublime.windows():
            for i in [v for v in win.views() if v and v.file_name()]:
                if not i.file_name().endswith(".txt"):
                    continue

                view_region = sublime.Region(0, i.size())
                view_str = i.substr(view_region)
                for j, line in enumerate(view_str.splitlines()):
                    if re.search(r"\b" + re.escape(PdxObject.key) + r"\b", line):
                        filename = (
                            i.file_name()
                            .replace("\\", "/")
                            .rstrip("/")
                            .rpartition("/")[2]
                        )
                        line_num = j + 1
                        if word_line_num == line_num and word_file == filename:
                            # Don't do current word
                            continue
                        elif (
                            line_num == PdxObject.line
                            and i.file_name() == PdxObject.path
                        ):
                            # Don't do definition
                            continue
                        else:
                            references.append(f"{i.file_name()}|{line_num}")
        if references:
            ref = f'<p><b>References to&nbsp;&nbsp;</b><tt class="variable">{PdxObject.key}</tt></p>'
            for i in references:
                fname = i.split("|")[0]
                shortname = fname.replace("\\", "/").rstrip("/").rpartition("/")[2]
                line = i.split("|")[1]
                goto_args = {"path": fname, "line": line}
                goto_url = sublime.command_url(
                    "goto_script_object_definition", goto_args
                )
                ref += (
                    """<a href="%s" title="Open %s and goto line %s">%s:%s</a>&nbsp;"""
                    % (
                        goto_url,
                        shortname,
                        line,
                        shortname,
                        line,
                    )
                )
                goto_right_args = {"path": fname, "line": line}
                goto_right_url = sublime.command_url(
                    "goto_script_object_definition_right", goto_right_args
                )
                ref += (
                    """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""
                    % (goto_right_url)
                )

        return ref

    def show_popup_default(self, view, point, word, PdxObject, header):
        if view.file_name() is None:
            return

        link = self.get_definitions_for_popup(
            view, point, PdxObject, header
        ) + self.get_references_for_popup(view, point, PdxObject, header)
        if link:
            hoverBody = """
                <body id="vic-body">
                    <style>%s</style>
                    <h1>%s</h1>
                    %s
                </body>
            """ % (
                css.default,
                header,
                link,
            )

            view.show_popup(
                hoverBody,
                flags=(
                    sublime.HIDE_ON_MOUSE_MOVE_AWAY
                    | sublime.COOPERATE_WITH_AUTO_COMPLETE
                    | sublime.HIDE_ON_CHARACTER_EVENT
                ),
                location=point,
                max_width=1024,
            )

    def show_popup_named_color(self, view, point, word, PdxObject, header):
        if view.file_name() is None:
            return

        object_color = PdxObject.color
        css_color = PdxObject.rgb_color
        r = css_color[0]
        g = css_color[1]
        b = css_color[2]
        icon_color = f"rgb({r},{g},{b})"
        color = f'<a class="icon"style="color:{icon_color}">■</a>\t\t\t<code>{object_color}</code>'

        link = self.get_definitions_for_popup(view, point, PdxObject, header, color)
        if link:
            hoverBody = """
                <body id="vic-body">
                    <style>%s</style>
                    <h1>%s</h1>
                    %s
                </body>
            """ % (
                css.default,
                header,
                link,
            )

            view.show_popup(
                hoverBody,
                flags=(
                    sublime.HIDE_ON_MOUSE_MOVE_AWAY
                    | sublime.COOPERATE_WITH_AUTO_COMPLETE
                    | sublime.HIDE_ON_CHARACTER_EVENT
                ),
                location=point,
                max_width=1024,
            )

    def show_texture_hover_popup(self, view, point, texture_name, full_texture_path):
        args = {"path": full_texture_path}
        open_texture_url = sublime.command_url("open_victoria_texture ", args)
        folder_args = {"path": full_texture_path, "folder": True}
        open_folder_url = sublime.command_url("open_victoria_texture ", folder_args)
        in_sublime_args = {"path": full_texture_path, "mode": "in_sublime"}
        inline_args = {"path": full_texture_path, "point": point}
        open_in_sublime_url = sublime.command_url(
            "open_victoria_texture ", in_sublime_args
        )
        open_inline_url = sublime.command_url("v3_show_texture ", inline_args)
        hoverBody = """
            <body id=\"vic-body\">
                <style>%s</style>
                <h1>Open Texture</h1>
                <div></div>
                <a href="%s" title="Open folder containing the texture.">Open Folder</a>
                <br>
                <a href="%s" title="Open %s in the default program">Open in default program</a>
                <br>
                <a href="%s" title="Open %s in sublime">Open in sublime</a>
                <br>
                <a href="%s" title="Show %s at current selection">Show Inline</a>
            </body>
        """ % (
            css.default,
            open_folder_url,
            open_texture_url,
            texture_name,
            open_in_sublime_url,
            texture_name,
            open_inline_url,
            texture_name,
        )

        view.show_popup(
            hoverBody,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=802,
        )

    def show_video_hover_popup(self, view, point, word):
        args = {"play": True}
        browse_and_play_url = sublime.command_url("browse_bink_videos", args)
        hoverBody = """
            <body id=\"vic-body\">
                <style>%s</style>
                <h1>Bink Video</h1>
                <span>•</span><a href="subl:play_bink_video" title="Note: Rad Game Tools Bink video player required.">Play %s.bk2</a>
                <br><div></div>
                <span>•</span><a href="subl:browse_bink_videos" title="Browse videos for a video to replace current video path.">Browse and Replace</a>&nbsp;
                <br>
                <span>•</span><a href="%s" title="Browse videos for a video to replace current video path and then play the new video.">Browse, Replace, and Play</a>&nbsp;
            </body>
        """ % (
            css.default,
            word,
            browse_and_play_url,
        )

        view.show_popup(
            hoverBody,
            flags=(
                sublime.HIDE_ON_MOUSE_MOVE_AWAY
                | sublime.COOPERATE_WITH_AUTO_COMPLETE
                | sublime.HIDE_ON_CHARACTER_EVENT
            ),
            location=point,
            max_width=802,
        )


# Global so I don't have to deal with passing through the hrefs, should probably just pass them as args.


class GotoScriptObjectDefinitionCommand(sublime_plugin.WindowCommand):
    def run(self, path, line):
        if os.path.exists(path):
            file_path = "{}:{}:{}".format(path, line, 0)
            self.open_location(self.window, file_path)

    def open_location(self, window, location):
        flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP
        window.open_file(location, flags)


class GotoScriptObjectDefinitionRightCommand(sublime_plugin.WindowCommand):
    def run(self, path, line):
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
