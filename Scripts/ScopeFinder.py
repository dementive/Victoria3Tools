import sublime
import sublime_plugin
from collections import deque

recently_saved = False

# Finds the current scope like effect = {} or trigger = {}
class SimpleScopeMatchListener(sublime_plugin.EventListener):

	# Get the index of a closing bracket in a string given the starting brackets index
	def getIndex(self, string, index):
		if string[index] != '{':
			return -1
		d = deque()
		for k in range(index, len(string)):
			if string[k] == '}':
				d.popleft()
			elif string[k] == '{':
				d.append(string[index])
			if not d:
				return k + 1
		return -1

	def on_selection_modified_async(self, view):
		global recently_saved

		if recently_saved:
		    return

		if view:
			return

		try:
			if view.syntax().name != "Victoria Script":
				return
		except AttributeError:
			return
		
		view_region = sublime.Region(0, view.size())
		view_str = view.substr(view_region)

		# Get the starting bracket index from the syntax scopes
		start_trigger_brackets = view.find_by_selector("meta.trigger.bracket")
		trigger_regions = []
		for br in start_trigger_brackets:
			trigger_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

		start_effect_brackets = view.find_by_selector("meta.effect.bracket")
		effect_regions = []
		for br in start_effect_brackets:
			effect_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

		# start_mod_brackets = view.find_by_selector("meta.modifier.bracket")
		# mod_regions = []
		# for br in start_mod_brackets:
		# 	mod_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

		# start_value_brackets = view.find_by_selector("meta.value.bracket")
		# value_regions = []
		# for br in start_value_brackets:
		# 	value_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

		start_ai_brackets = view.find_by_selector("meta.ai.bracket")
		ai_regions = []
		for br in start_ai_brackets:
			ai_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

		selection = view.sel()
		if not selection[0].empty():
			return

		self.show_status(selection[0].a, trigger_regions, "trigger", view)

		# Have to account for trigger fields inside of effect fields, definetly a better way to do this.
		for block in effect_regions:
			if block.a <= selection[0].a <= block.b:
				view.set_status("effect", "Effect Field")
				for block in trigger_regions:
					if block.a <= selection[0].a <= block.b:
						view.erase_status("effect")
						view.set_status("trigger", "Trigger Field")
						break
					else:
						view.erase_status("trigger")
				break
			else:
				view.erase_status("effect")

		#self.show_status(selection[0].a, mod_regions, "modifier", view)
		#self.show_status(selection[0].a, value_regions, "value", view)
		self.show_status(selection[0].a, ai_regions, "ai control", view)
		recently_saved = True
		# 1 second delay so its not annoying when typing
		sublime.set_timeout(lambda: self.set_recent(), 1000)


	def show_status(self, selection, regions, status, view):
		for block in regions:
			if block.a <= selection <= block.b:
				view.set_status(status, status.title() + " Field")
				break
			else:
				view.erase_status(status)

	def set_recent(self):
	    global recently_saved
	    recently_saved = False