import sublime, sublime_plugin, re

def localize_tokens(file_contents):
	out_list = []
	file_contents = file_contents.replace("desc = {", "").replace("custom_tooltip = {", "")
	out = re.sub("(#).*", "", file_contents)
	out = out.replace(" ", "")
	out = re.findall("(title|desc|name|custom_tooltip|text|flavor)\s?=\s?(.+)", out)

	for i in out:
		key = i[1].replace("\"", "")
		# Exclude modifiers and variables
		if key.endswith("_mod") or key.endswith("_var") or key.endswith("_cooldown"):
			pass
		else:
			if (not key.endswith("tt") and not key.endswith("ttt") and key.endswith(".t") or key.endswith("title")):
				key = "\n" + key + ":0 \"\"\n"
			else:
				key = key + ":0 \"\"\n"
				key = key.replace("\t","")
			out_list.append(key)

	return out_list

class LocalizeCurrentFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window = sublime.active_window()
		view = window.active_view()
		view_region = sublime.Region(0, view.size())
		view_str = view.substr(view_region)
		loc_list = localize_tokens(view_str)

		# Insert into new view
		window.run_command('new_file')
		loc_view = window.active_view()
		loc_view.set_name("Localization")
		for i in loc_list:
			loc_view.insert(edit, len(loc_view), i)
