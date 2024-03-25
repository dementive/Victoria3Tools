"""
Representation of a Tiger json object and a way to display the output as a string with the same look as the actual tiger output.
"""


class Location:
    def __init__(self, column, origin, fullpath, length, line, linenr, path, tag=None):
        self.column = column
        self.origin = origin  # Renamed to avoid conflict with 'from' keyword
        self.fullpath = fullpath
        self.length = length
        self.line = line
        self.linenr = linenr
        self.path = path
        self.tag = tag


class TigerJsonObject:
    def __init__(self, confidence, info, key, locations, message, severity):
        self.confidence = confidence
        self.info = info
        self.key = key
        locations_list = list()
        for i in locations:
            locations_list.append(
                Location(
                    i["column"],
                    i["from"],
                    i["fullpath"],
                    i["length"],
                    i["line"],
                    i["linenr"],
                    i["path"],
                    i["tag"],
                )
            )
        self.locations = locations_list
        self.message = message
        self.severity = severity
        self._max_line_num_length = 0

    def display(self):
        """
        Displays the object in the same way that tiger outputs it in ACSCII
        This code sucks, as you can see, but it works perfectly so don't touch it unless something is broke.
        Example:
            warning(duplicate-item): gui type is redefined by another gui type
                --> [MOD] gui/shared/Bloodlines_templates.gui
             451 |     type cpt_button_large = margin_widget {
                 |          ^^^^^^^^^^^^^^^^
                --> [Vic3] gui/shared/gui_base.gui
            5293 |     type cpt_button_large = margin_widget {
                 |          ^^^^^^^^^^^^^^^^ <-- the other gui type is here
        """
        out_str = f"{self.severity}({self.key}): {self.message}\n"
        self._max_line_num_length = max(
            len(str(location.linenr)) for location in self.locations
        )

        previous_paths = list()
        for i, location in enumerate(self.locations):
            line_num_padding = " "
            low_num_padding = ""
            low_num_arrow_padding = ""
            arrows = ""
            line_len = len(str(location.linenr))

            # The initial padding is dependent on the line number with the longest length
            if line_len < self._max_line_num_length:
                for j in range(self._max_line_num_length - line_len):
                    low_num_padding += " "
            if low_num_padding:
                low_num_arrow_padding = " "

            for j in range(line_len):
                line_num_padding += " "

            if location.column:
                location.column -= 1
                column_padding = " " * location.column

                if location.length:
                    arrows = "^" * location.length

                line = location.line.replace("\t", " ")
                tag = f"<-- {location.tag}" if location.tag else ""
                added_arrow = "--> " if i < 1 else "--> "

                if location.fullpath not in previous_paths:
                    out_str += f"{line_num_padding}{low_num_arrow_padding}{added_arrow}[{location.origin}] {location.path}\n"
                previous_paths.append(location.fullpath)
                # NOTE: There is an invisible chararcter here on both sides of "⁭{line}⁭"⁭
                # This is used in Tiger.sublime-syntax to indicate where the embedding for script lines starts and ends
                # Without it there isn't a good way to indicate where the embedding needs to end due to limitations with the 'escape' keyword of sublime-syntaxes
                out_str += f"{low_num_padding}{location.linenr} |⁭{line}⁭\n"
                out_str += f"{low_num_padding}{line_num_padding}|{column_padding}{arrows} {tag}\n"

                if i + 1 == len(self.locations):
                    if self.info:
                        out_str += f"{line_num_padding}= Info: {self.info}\n"
                    out_str += "\n"
            else:
                # If no column exists than it is just a "Info" message
                added_arrow = "--> " if i < 1 else "--> "

                if location.path not in previous_paths:
                    out_str += f" {added_arrow}[{location.origin}] {location.path}\n"
                    if i + 1 == len(self.locations) and self.info:
                        out_str += f"  = Info: {self.info}\n"

                if not location.line:
                    out_str += "⁭\n"

        return out_str
