import sublime, sublime_plugin, re
from collections import deque

class LocalizeCurrentFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window = sublime.active_window()
		view = window.active_view()
		view_region = sublime.Region(0, view.size())
		view_str = view.substr(view_region)
		loc_list = self.localize_tokens(view_str)

		# Insert into new view
		window.run_command('new_file')
		loc_view = window.active_view()
		loc_view.set_name("Localization")
		for i in loc_list:
			loc_view.insert(edit, len(loc_view), i)

	def localize_tokens(self, file_contents):
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

class FoldAllObjectsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = sublime.active_window().active_view()
		view_region = sublime.Region(0, view.size())
		view_str = view.substr(view_region)

		loc_list = self.find_obj_regions(view_str, view)
		for i in loc_list:
			if view.is_folded(i):
				view.unfold(i)
			else:
				view.fold(i)

	def find_obj_regions(self, string, view):
		# Return a list of regions from top level objects
		li = []
		start = -1
		open_count = -1
		close_count = 0
		end = 0
		found = False
		for index, char in enumerate(string):
			if char == '{' and found == False:
				start = index
				open_count += 2
				found = True

			elif char == '{':
				open_count += 1

			if char == '}':
				close_count += 1
				
			if close_count == open_count:
				end = index
				open_count = -1
				close_count = 0
				found = False
				li.append((start + 1, end - 1))

		for index, region in enumerate(li):
			li[index] = sublime.Region(li[index][0], li[index][1])

		return li
