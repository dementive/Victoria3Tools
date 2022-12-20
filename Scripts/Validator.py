import sublime, sublime_plugin
import re

class ValidatorOnSaveListener(sublime_plugin.EventListener):

    def __init__(self):
        self.view = None
        self.view_str = None

    def on_post_save_async(self, view):
        
        if view is None:
            return
        try:
            if view.syntax().name != "Victoria Script":
                return
        except AttributeError:
            return

        self.view = view
        self.view_str = view.substr(sublime.Region(0, view.size()))

        self.bracket_check()
        self.quote_check()
        self.encoding_check()

    def encoding_check(self):
        # Check that the current filepath is in a folder that should use UTF-8 with BOM
        # If it should be UTF-8 with BOM and it is not create error panel
        path = self.view.file_name()
        # Coat of arms is the only files that are only UTF-8 not UTF-8 with BOM
        utf8_paths = re.search(r"(common\\coat_of_arms)", path)
        bom_paths = re.search(r"(events|common|music|localization)", path)
        with open(path, "r+b") as fp:
            old_encoding = self.view.encoding()
            if not old_encoding == "UTF-8 with BOM":
                if bom_paths is not None and utf8_paths is None:
                    # is not bom and should be
                    self.view.set_encoding("UTF-8 with BOM")
                    error_message = f"EncodingError: Encoding is {old_encoding}, files in {bom_paths.group()} should be UTF-8 with BOM, resave to fix."

                    panel = self.create_error_panel()
                    panel.set_read_only(False)
                    panel.run_command("append", {"characters": error_message})
                    panel.add_regions("bad_encoding", [sublime.Region(27, 27 + len(old_encoding))], "underline.bad", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE  ))
                    panel.add_regions("encoding", [sublime.Region(len(panel) - 30, len(panel) - 16)], "underline.good", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE  ))
                    panel.set_read_only(True)
                    
                if utf8_paths is not None and not old_encoding == "UTF-8":
                    # is not utf-8 and should be
                    self.view.set_encoding("UTF-8")
                    error_message = f"EncodingError: Encoding is {old_encoding}, files in {utf8_paths.group()} should be UTF-8, resave to fix."

                    panel = self.create_error_panel()
                    panel.set_read_only(False)
                    panel.run_command("append", {"characters": error_message})
                    # bad encoding
                    panel.add_regions("bad_encoding", [sublime.Region(27, 27 + len(old_encoding))], "underline.bad", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE  ))
                    # new good encoding
                    panel.add_regions("encoding", [sublime.Region(len(panel) - 21, len(panel) - 16)], "underline.good", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE  ))
                    panel.set_read_only(True)

    def bracket_check(self):
        # Check for mismatched brackets and shows an error message at the line of the error
        check = checker(self.view_str)
        if not check:
            return

        self.view.show(check)
        line = self.view.rowcol(check)
        line_num = line[0]
        line_a = int(len(str(line_num)))
        error_message = f"BracketError: There is a mismatched bracket near line {line_num}"

        panel = self.create_error_panel()
        panel.set_read_only(False)
        panel.run_command("append", {"characters": error_message})
        panel.add_regions("line_num", [sublime.Region(len(panel) - line_a, len(panel))], "region.redish", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE  ))
        panel.set_read_only(True)

    def quote_check(self):
        # Check for mismatched quotes and shows an error message at the line of the error
        lines = self.view_str.splitlines()

        total_quote_count = 0
        potential_errors = []
        for index, line in enumerate(lines, start=1):
            count = line.count("\"")
            total_quote_count += count
            if count == 2 or count == 0:
                continue
            if count % 2 == 1:
                # add line number to potential errors, will show first potential error if total count is not even
                potential_errors.append(index)


        # NOTE: If quotes on separate lines is actually allowed change the 'or' to an 'and'
        try:
            if total_quote_count % 2 == 1 or potential_errors[0] is not None:
                line_num = potential_errors[0]
        except IndexError:
            return

        self.view.run_command("goto_line", {"line": line_num})
        line_a = int(len(str(line_num)))
        error_message = f"QuoteError: There is an extra quotation near line {line_num}"

        panel = self.create_error_panel()
        panel.set_read_only(False)
        panel.run_command("append", {"characters": error_message})
        panel.add_regions("line_num", [sublime.Region(len(panel) - line_a, len(panel))], "region.redish", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE  ))
        panel.set_read_only(True)

    def create_error_panel(self):
        window = sublime.active_window()
        panel = window.create_output_panel("error", unlisted=True)
        panel.assign_syntax("scope:text.error")
        panel.settings().set("color_scheme", "ErrorPanel.hidden-color-scheme")
        panel.settings().set('gutter',False)
        window.run_command("show_panel", {"panel": "output.error"})
        return panel

class Bracket:
    def __init__(self, bracket_type, position):
        self.bracket_type = bracket_type
        self.position = position

    def match(self, char):
        if self.bracket_type == '[' and char == ']':
            return True
        if self.bracket_type == '{' and char == '}':
            return True
        if self.bracket_type == '(' and char == ')':
            return True
        return False

def checker(text):
    stack = []
    for index, char in enumerate(text, start=1):

        if char in ("[", "(", "{"):
            stack.append(Bracket(char, index))

        elif char in ("]", ")", "}"):
            if not stack:
                return index

            top = stack.pop()
            if not top.match(char):
                return index
    if stack:
        top = stack.pop()
        return top.position

    return False # file is all good
