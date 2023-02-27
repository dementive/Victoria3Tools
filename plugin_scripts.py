import sublime, sublime_plugin
import os, re, webbrowser, threading
from collections import deque
from .jomini import GameObjectBase
from .Utilities.game_data import GameData

# ----------------------------------
# -          Plugin Setup          -
# ----------------------------------
settings = None
v3_files_path = None
v3_mod_files = None


# Setup Paths for Objects, get set on plugin_loaded
# This is the unified paths with all mod paths + base game path at the end
file_paths = []

# Victoria 3 Game Object Class implementations
class V3AiStrategy(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\ai_strategies")

class V3BuildingGroup(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\building_groups")

class V3Building(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\building")

class V3CharacterTrait(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\character_traits")

class V3Culture(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\cultures")

class V3Decree(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\decrees")

class V3DiplomaticAction(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\diplomatic_actions")

class V3DiplomaticPlay(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\diplomatic_plays")

class V3GameRules(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\game_rules")

class V3Goods(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\goods")

class V3GovernmentType(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\government_types")

class V3Ideology(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\ideologies")

class V3Institutions(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\institutions")

class V3Ideology(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\ideologies")

class V3InterestGroupTrait(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\interest_group_traits")

class V3InterestGroup(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\interest_groups")

class V3JournalEntry(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\journal_entries")

class V3LawGroup(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\law_groups")

class V3Law(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\laws")

class V3Modifier(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\modifiers")

class V3OpinionModifier(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\opinion_modifiers")

class V3Party(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\parties")

class V3PopNeed(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\pop_needs")

class V3PopType(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\pop_types")

class V3ProductionMethodGroup(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\production_method_groups")

class V3ProductionMethod(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\production_methods")

class V3Religion(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\religions")

class V3ScriptValue(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\script_values")

class V3ScriptedEffect(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\scripted_effects")

class V3ScriptedModifier(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\scripted_modifiers")

class V3ScriptedTrigger(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\scripted_triggers")

class V3StateTrait(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\state_traits")

class V3StrategicRegion(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\strategic_regions")

class V3SubjectType(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\subject_types")

class V3Technology(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\technology")

class V3Terrain(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "common\\terrain")

class V3StateRegion(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "map_data\\state_regions")

class V3Event(GameObjectBase):
	def __init__(self, paths):
		super().__init__(paths)
		self.get_data(file_paths, "events")

# Game Data class
GameData = GameData()

# Global Object Variables that get set on plugin_loaded
ai_strats = bgs = buildings = char_traits = cultures = mods = decrees = diplo_actions = diplo_plays = ""
game_rules = goods = gov_types = ideologies = institutions = ig_traits = igs = jes = law_groups = laws = ""
op_mods = parties = pop_needs = pop_types = pm_groups = pms = religions = state_traits = strategic_regions = "" 
subject_types = technologies = terrains = state_regions = events = ""

# Function to fill all global game objects that get set in non-blocking async function on plugin_loaded
# Setting all the objects can be slow and doing it on every hover (when they are actually used) is even slower, 
# so loading it all in on plugin init makes popups actually responsive

def load_game_objects():
	#import time # Use time to optimize thread count when adding new objects
	#t0 = time.time()

	def load_first():
		global ai_strats, bgs, buildings, char_traits, cultures, decrees, diplo_actions, diplo_plays
		ai_strats = V3AiStrategy(file_paths)
		bgs = V3BuildingGroup(file_paths)
		buildings = V3Building(file_paths)
		char_traits = V3CharacterTrait(file_paths)
		cultures = V3Culture(file_paths)
		decrees = V3Decree(file_paths)
		diplo_actions = V3DiplomaticAction(file_paths)
		diplo_plays = V3DiplomaticPlay(file_paths)

	def load_second():
		global mods, game_rules, goods, gov_types, ideologies, institutions, ig_traits, igs
		mods = V3Modifier(file_paths)
		game_rules = V3GameRules(file_paths)
		goods = V3Goods(file_paths)
		gov_types = V3GovernmentType(file_paths)
		ideologies = V3Ideology(file_paths)
		institutions = V3Institutions(file_paths)
		ig_traits = V3InterestGroupTrait(file_paths)
		igs = V3InterestGroup(file_paths)

	def load_third():
		global jes, law_groups, laws, op_mods, parties, pop_needs, pop_types, pm_groups
		jes = V3JournalEntry(file_paths)
		law_groups = V3LawGroup(file_paths)
		laws = V3Law(file_paths)
		op_mods = V3OpinionModifier(file_paths)
		parties = V3Party(file_paths)
		pop_needs = V3PopNeed(file_paths)
		pop_types = V3PopType(file_paths)
		pm_groups = V3ProductionMethodGroup(file_paths)

	def load_fourth():
		global pms, religions, script_values, scripted_effects, scripted_modifiers, scripted_triggers, state_traits, strategic_regions
		pms = V3ProductionMethod(file_paths)
		religions = V3Religion(file_paths)
		script_values = V3ScriptValue(file_paths)
		scripted_effects = V3ScriptedEffect(file_paths)
		scripted_modifiers = V3ScriptedModifier(file_paths)
		scripted_triggers = V3ScriptedTrigger(file_paths)
		state_traits = V3StateTrait(file_paths)
		strategic_regions = V3StrategicRegion(file_paths)

	def load_fifth():
		global subject_types, technologies, terrains, state_regions, events
		subject_types = V3SubjectType(file_paths)
		technologies = V3Technology(file_paths)
		terrains = V3Terrain(file_paths)
		state_regions = V3StateRegion(file_paths)
		events = V3Event(file_paths)

	thread1 = threading.Thread(target=load_first); thread2 = threading.Thread(target=load_second)
	thread3 = threading.Thread(target=load_third); thread4 = threading.Thread(target=load_fourth)
	thread5 = threading.Thread(target=load_fifth)
	thread1.start(); thread2.start(); thread3.start(); thread4.start(); thread5.start();
	thread1.join(); thread2.join(); thread3.join(); thread4.join(); thread5.join();

	#t1 = time.time()
	#print("Time taken to load Victoria 3 objects: {:.3f} seconds".format(t1-t0))

def plugin_loaded():
	global settings, v3_files_path, v3_mod_files, file_paths
	settings = sublime.load_settings("Victoria Syntax.sublime-settings")
	v3_files_path = settings.get("Victoria3FilesPath")
	v3_mod_files = settings.get("PathsToModFiles")
	out_file_paths = v3_mod_files
	out_file_paths.append(v3_files_path)
	file_paths = out_file_paths
	sublime.set_timeout_async(lambda: get_mod_data(), 0)
	sublime.set_timeout_async(lambda: load_game_objects(), 0)
	sublime.set_timeout_async(lambda: write_data_to_syntax(), 0)

class V3ReloadPluginCommand(sublime_plugin.WindowCommand):
	def run(self):
		plugin_loaded()

def get_mod_data():
	for mod in v3_mod_files:
		# Populate GameData.EventVideos list from gfx files
		if os.path.exists(mod + "\\gfx\\event_pictures"):			
			for file in [x for x in os.scandir(mod + "\\gfx\\event_pictures") if x.name.endswith(".bk2")]:
				path = file.path
				path = path.split("game\\")[1].replace("\\", "/")
				GameData.EventVideos.append(path)

def write_data_to_syntax():
	fake_syntax_path = sublime.packages_path() + "\\Victoria3Tools\\Vic3 Script\\VictoriaScript.fake-sublime-syntax"
	real_syntax_path = sublime.packages_path() + "\\Victoria3Tools\\Vic3 Script\\VictoriaScript.sublime-syntax"
	with open(fake_syntax_path, "r") as file:
	    lines = file.read()

	# Append all other matches to auto-generated-content section
	lines += write_syntax(scripted_triggers.keys(), "Scripted Triggers", "string.scripted.trigger")
	lines += write_syntax(scripted_effects.keys(), "Scripted Effects", "keyword.scripted.effect")
	lines += write_syntax(script_values.keys(), "Scripted Values", "storage.type.script.value")

	# All GameObjects get entity.name scope
	lines += write_syntax(ai_strats.keys(), "Ai Strategies", "entity.name.ai.strat")
	lines += write_syntax(bgs.keys(), "Building Groups", "entity.name.bg")
	lines += write_syntax(buildings.keys(), "Buildings", "entity.name.building")
	lines += write_syntax(char_traits.keys(), "Character Traits", "entity.name.character.trait")
	lines += write_syntax(cultures.keys(), "Cultures", "entity.name.culture")
	lines += write_syntax(mods.keys(), "Modifiers", "entity.name.modifier")
	lines += write_syntax(decrees.keys(), "Decrees", "entity.name.decree")
	lines += write_syntax(diplo_actions.keys(), "Diplomatic Actions", "entity.name.diplo.action")
	lines += write_syntax(diplo_plays.keys(), "Diplomatic Plays", "entity.name.diplo.play")
	lines += write_syntax(game_rules.keys(), "Game Rules", "entity.name.game.rule")
	lines += write_syntax(goods.keys(), "Trade Goods", "entity.name.trade.good")
	lines += write_syntax(gov_types.keys(), "Gov Types", "entity.name.gov.type")
	lines += write_syntax(ideologies.keys(), "Ideologies", "entity.name.ideology")
	lines += write_syntax(institutions.keys(), "Institutions", "entity.name.institution")
	lines += write_syntax(ig_traits.keys(), "Ig Traits", "entity.name.ig.trait")
	lines += write_syntax(igs.keys(), "Interest Groups", "entity.name.interest.group")
	lines += write_syntax(jes.keys(), "Journal Entries", "entity.name.journal.entry")
	lines += write_syntax(law_groups.keys(), "Law Groups", "entity.name.law.group")
	lines += write_syntax(laws.keys(), "Laws", "entity.name.law")
	lines += write_syntax(op_mods.keys(), "Opinion Modifiers", "entity.name.op.mod")
	lines += write_syntax(parties.keys(), "Parties", "entity.name.party")
	lines += write_syntax(pop_needs.keys(), "Pop Needs", "entity.name.pop.need")
	lines += write_syntax(pop_types.keys(), "Pop Types", "entity.name.pop.type")
	lines += write_syntax(pm_groups.keys(), "Production Method Groups", "entity.name.pm.groups")
	lines += write_syntax(pms.keys(), "Production Methods", "entity.name.pm")
	lines += write_syntax(religions.keys(), "Religions", "entity.name.religion")
	lines += write_syntax(state_traits.keys(), "State Traits", "entity.name.state.trait")
	lines += write_syntax(strategic_regions.keys(), "Strategic Regions", "entity.name.strategic.region")
	lines += write_syntax(subject_types.keys(), "Subject Types", "entity.name.subject.type")
	lines += write_syntax(technologies.keys(), "Technologies", "entity.name.tech")
	lines += write_syntax(terrains.keys(), "Terrains", "entity.name.terrain")
	lines += write_syntax(state_regions.keys(), "State Regions", "entity.name.state.region")
	
	# Dont highlight event ids, only show popups
	#lines += write_syntax(events.keys(), "Events", "entity.name.event")

	with open(real_syntax_path, "w", encoding="utf-8") as file:
	    file.write(lines)

def write_syntax(li, header, scope):
	string = ""
	count = 0
	string += f"\n    # Generated {header}\n    - match: \\b(?i)("
	for i in li:
		count += 1
		# Count is needed to split because columns are waaay too long for syntax regex
		if count == 0:
			string = f")(?-i)\\b\n      scope: {scope}\n"
			string += f"    # Generated {header}\n    - match: \\b(?i)({i}|"
		elif count == 75:
			string += f")(?-i)\\b\n      scope: {scope}\n"
			string += f"    # Generated {header}\n    - match: \\b(?i)({i}|"
			count = 1
		else:
			string += f"{i}|"
	string += f")(?-i)\\b\n      scope: {scope}"
	return string

# css for non-documentation popups
css_basic_style = """
	body {
		font-family: system;
		margin: 0;
		padding: 0.35rem;
		background-color: rgb(25, 25, 25);
	}
	p {
		font-size: 1.0rem;
		margin-top: 5;
		margin-bottom: 5;
	}
	h1 {
		font-size: 1.2rem;
		margin: 0;
		padding-bottom: 0.05rem;
	}
	a {
		font-size: 1.0rem;
	}
	span {
		padding-right: 0.3rem;
	}
	div {
		padding: 0.1rem;
	}
"""

# ----------------------------------
# -     Text & Window Commands     -
# ----------------------------------

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
					loced = key.replace("_", " ")
					key = "\n" + key + ":0 \"" + loced + "\""
				else:
					loced = key.replace("_", " ")
					key = "\n" + key + ":0 \"" + loced + "\""
					key = key.replace("\t","")
				out_list.append(key)

		return out_list

class FolderHandler(sublime_plugin.TextCommand):

    def input_description(self):
        return "Fold Level"

    def input(self, args):
        if 'level' not in args:
            return FoldingInputHandler()

    def run(self, edit, level):
        if level != "Unfold All":
            self.view.run_command("fold_by_level", {"level": int(level)})
        else:
            self.view.run_command("unfold_all")

class FoldingInputHandler(sublime_plugin.ListInputHandler):

    def name(self):
        return 'level'

    def list_items(self):
        keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "Unfold All"]
        return keys

# ----------------------------------
# -            Validator           -
# ----------------------------------

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
		if settings.get("ScriptValidator") == False:
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
		window.focus_view(panel)
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

# ----------------------------------
# -        Scope Status Bar        -
# ----------------------------------

recently_set_scope_status = False

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
		global recently_set_scope_status

		if recently_set_scope_status:
			return

		if not view:
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

		self.show_status(selection[0].a, ai_regions, "ai control", view)
		recently_set_scope_status = True
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
		global recently_set_scope_status
		recently_set_scope_status = False


# ----------------------------------
# -     Shader Intrinsic Hover     -
# ----------------------------------

def OpenMSDNLink(text):
	openStyle = 2
	openStyleSetting = settings.get("IntrinsicHoverLinkOpenStyle", "new_tab")
	if openStyleSetting == "same_window":
		openStyle = 0
	elif openStyleSetting == "new_window":
		openStyle = 1

	webbrowser.open(text, openStyle)


class IntrinsicHoverListener(sublime_plugin.EventListener):
	def on_hover(sef, view, point, hover_zone):
		if settings.get("IntrinsicHoverEnabled", True) == False:
			return
		if not view:
			return
		try:
			if view.syntax().name != "PdxShader":
				return
		except AttributeError:
			return

		scopesStr = view.scope_name(point)
		scopeList = scopesStr.split(' ')
		for scope in scopeList:
			if scope == "keyword.function.intrinsic.hlsl":
				posWord = view.word(point)
				intrinsicWord = view.substr(posWord)
				if intrinsicWord in GameData.IntrinsicList:
					url, desc = GameData.IntrinsicList[intrinsicWord]
					hoverBody = """
						<body id=show-intrinsic>
							<style>
								body {
									font-family: system;
								}
								p {
									font-size: 1.0rem;
									margin: 0;
								}
							</style>
							<p>%s</p>
							<br>
							<a href="%s">MSDN Link</a>
						</body>
					""" % (desc, url)

					view.show_popup(hoverBody, flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY, location=point, max_width=1024, on_navigate=lambda x: OpenMSDNLink(x))
					return

# ----------------------------------
# -    Open Included Shader File   -
# ----------------------------------

pos = -1
posa = -1
posb = -1
out_point = -1
out_view = ""
file = ""

class OpenPdxShaderHeaderCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# Command for href
		global out_point, out_view
		if self.check_scope(out_view, out_point):
			self.open_file(out_view)

	def check_scope(self, view, point):
		global pos, posa, posb, file

		scopesStr = view.scope_name(point)
		scopeList = scopesStr.split(' ')
		if scopeList[1] == "string.quoted.double.include.hlsl":
			posLine = view.line(point)
			posa = posLine.a + 2
			posb = posLine.b - 1
			pos = 1
			file = view.substr(sublime.Region(posa, posb))
			return True
		else:
			self.pos = -1
			return False

	def open_file(self, view):
		global pos, file
		if pos != -1:
			scopeRegion = view.extract_scope(pos)
			originalFilePath = file.replace("/", "\\")
			# Search order is from absolute path of launching file, list order of user paths, finally Unity project paths.
			basePath = ""
			curFile = view.file_name()
			if curFile != None:
				basePath = view.file_name().rsplit('\\', 1)[0] + '\\'
			paths = [ basePath ]

			self.settingsBasePaths = settings.get("OpenHeaderBasePaths", [])
			settingsIncludePaths = settings.get("OpenHeaderIncludePaths", [])
			settingsPaths = []
			for index in range(0, len(settingsIncludePaths)):
				newSettingsPath = re.sub("(\$base_path)(\[)(\d+)(\])", self.path_replace, settingsIncludePaths[index])
				paths.append(newSettingsPath)

			# Try to find paths expected relative to a Unity project's root folder.
			assetDir, embeddedPackagePaths, cachedPackagePaths = self.get_unity_paths(basePath)
			if assetDir:
				paths.append(assetDir)

			for path in paths:
				newPath = os.path.normpath(path + "\\" + originalFilePath)
				fileExists = os.path.isfile(newPath)
				if fileExists:
					self.open_or_switch_to(newPath)
					return

			targetPathParts = originalFilePath.split("\\")
			if len(targetPathParts) >= 3 and targetPathParts[0].lower() == "packages":
				packageName = targetPathParts[1]
				targetRelative = "\\".join(targetPathParts[2:])
				packagePaths = embeddedPackagePaths + cachedPackagePaths
				embeddedPackagePaths.extend(packagePaths)

				for packagePath in packagePaths:
					if os.path.basename(packagePath).split("@")[0] == packageName:
						targetFile = os.path.normpath(os.path.join(packagePath, targetRelative))
						if os.path.isfile(targetFile):
							self.open_or_switch_to(targetFile)
							return

				lastLength = -1
				currentDir = basePath
				while len(currentDir) != lastLength:
					lastLength = len(currentDir)
					currentDir = os.path.dirname(currentDir)
					targetFile = os.path.normpath(currentDir + "\\" + packageName + "\\" + targetRelative)
					if os.path.isfile(targetFile):
						self.open_or_switch_to(targetFile)
						return

	def path_replace(self, match_object):
		# Given the pattern of (\$base_path)(\[)(\d+)(\]), \d+ is group 3
		index = int(match_object.group(3))
		if index < len(self.settingsBasePaths):
			return self.settingsBasePaths[index]
		return "ERRORSTRING"

	def open_or_switch_to(self, targetFile):
		fileView = sublime.active_window().find_open_file(targetFile)
		if fileView == None:
			fileView = sublime.active_window().open_file(targetFile)
		sublime.active_window().focus_view(fileView)

	def get_unity_paths(self, basePath):
		lastLength = -1
		currentDir = basePath
		while len(currentDir) != lastLength:
			lastLength = len(currentDir)
			currentDir = os.path.dirname(currentDir)
			assetsDir = os.path.normpath(currentDir + "\\Assets")
			packagesDir = os.path.normpath(currentDir + "\\Packages")
			packageCacheDir = os.path.normpath(currentDir + "\\Library\\PackageCache")

			# If both Assets and Packages folders exist then assume it is the project's root, but don't rely on
			# Library/PackageCache folder existing in case it hasn't been generated yet.
			if os.path.isdir(assetsDir) and os.path.isdir(packagesDir):
				embeddedPackagePaths = [packagesDir + "\\" + p for p in next(os.walk(packagesDir))[1]]
				cachedPackagePaths = []
				if os.path.isdir(packageCacheDir):
					cachedPackagePaths = [packageCacheDir + "\\" + p for p in next(os.walk(packageCacheDir))[1]]
				return (assetsDir, embeddedPackagePaths, cachedPackagePaths)

		return (None, [], [])

class HeaderHoverListener(sublime_plugin.EventListener):

	def on_hover(self, view, point, hover_zone):
		global out_point, out_view
		if settings.get("OpenHeaderEnabled") == False:
			return

		try:
			if view.syntax().name != "PdxShader":
				return
		except AttributeError:
			return

		out_point = point
		out_view = view
		scopesStr = view.scope_name(point)
		scopeList = scopesStr.split(' ')
		if scopeList[1] == "string.quoted.double.include.hlsl":
			self.show_hover_popup(view, point)

	def show_hover_popup(self, view, point):

		posLine = view.line(point)
		posa = posLine.a + 2
		posb = posLine.b - 1
		file = view.substr(sublime.Region(posa, posb))
		hoverBody = """
			<body id="vic-body">
				<style>%s</style>
				<h1>Header File</h1>
				<a href="subl:open_pdx_shader_header" title="If file does not open add path to package settings">Open %s</a>
			</body>
		""" %(css_basic_style, file)

		view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY
						|sublime.COOPERATE_WITH_AUTO_COMPLETE |sublime.HIDE_ON_CHARACTER_EVENT),
						location=point, max_width=502)

# ----------------------------------
# -          If Def Utils          -
# ----------------------------------

PreprocessorBlockListScanDown = {
	"if",
	"ifdef",
	"ifndef"
}

PreprocessorBlockListScanUp = {
	"endif"
}

PreprocessorBlockListScanBoth = {
	"elif",
	"else"
}

class IfDefMatchListener(sublime_plugin.EventListener):
	def on_hover(sef, view, point, hover_zone):
		if settings.get("IfDefMatchEnabled", True) == False:
			return
		if not view:
			return

		try:
			if view.syntax().name != "PdxShader":
				return
		except AttributeError:
			return

		def on_navigate(href):
			view.window().open_file(
				href,
				sublime.ENCODED_POSITION | sublime.FORCE_GROUP)

		def do_hover(view, point, startSection, endSection, seperator):
			hoverBody = """
				<body id=show-ifdefmatch>
					<style>
						body {
							font-family: system;
						}
						h1 {
							font-size: 1.1rem;
							font-weight: bold;
							margin: 0 0 0.25em 0;
						}
						p {
							font-size: 1.0rem;
							margin: 0;
						}
					</style>
					%s
					%s
					%s
				</body>
			""" % (startSection, seperator, endSection)

			view.show_popup(hoverBody, flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY, location=point, max_width=1024, on_navigate=on_navigate)

		def FormatLocation(file, row, col):
			return "%s:%d:%d" % (file, row + 1, col)

		def FormatHover(category, href, hrefText):
			return "<h1>%s</h1><p><a href=\"%s\">%s</a></p>" % (category, href, hrefText)

		def ScanDown(view, point):
			stackSize = 0
			offsetToNextLine = view.full_line(point).size()
			viewLength = view.size()
			while (point + offsetToNextLine <= viewLength):
				newLine = view.full_line(point + offsetToNextLine)
				trimmedNewLineStart = view.find_by_class(newLine.begin(), True, sublime.CLASS_WORD_START)
				newLineScopesStr = view.scope_name(trimmedNewLineStart)
				newLineScopeList = newLineScopesStr.split(' ')
				for newScope in newLineScopeList:
					if newScope == "keyword.control.preprocessor.hlsl":
						newLineWord = view.substr(newLine).lstrip()
						newLineWordForMatch = newLineWord.lstrip("#")
						newLineMatchArray = newLineWordForMatch.split()
						if (len(newLineMatchArray) != 0):
							newLineWordForMatch = newLineMatchArray[0]
						else:
							break
						if newLineWordForMatch in PreprocessorBlockListScanDown:
							stackSize += 1
						elif newLineWordForMatch in PreprocessorBlockListScanUp:
							if stackSize == 0:
								row, col = view.rowcol(newLine.begin())
								return FormatHover("Block End:", FormatLocation(view.file_name(), row, col), newLineWord.rstrip())
							else:
								stackSize -= 1
						break
				offsetToNextLine += newLine.size()

		def ScanUp(view, point):
			stackSize = 0
			row, col = view.rowcol(point)
			offsetToNextLine = col + 1
			while (point - offsetToNextLine > 0):
				newLine = view.full_line(point - offsetToNextLine)
				trimmedNewLineStart = view.find_by_class(newLine.begin(), True, sublime.CLASS_WORD_START)
				newLineScopesStr = view.scope_name(trimmedNewLineStart)
				newLineScopeList = newLineScopesStr.split(' ')
				for newScope in newLineScopeList:
					if newScope == "keyword.control.preprocessor.hlsl":
						newLineWord = view.substr(newLine).lstrip()
						newLineWordForMatch = newLineWord.lstrip("#")
						newLineMatchArray = newLineWordForMatch.split()
						if (len(newLineMatchArray) != 0):
							newLineWordForMatch = newLineMatchArray[0]
						else:
							break
						if newLineWordForMatch in PreprocessorBlockListScanUp:
							stackSize += 1
						elif newLineWordForMatch in PreprocessorBlockListScanDown:
							if stackSize == 0:
								row, col = view.rowcol(newLine.begin())
								return FormatHover("Block Start:", FormatLocation(view.file_name(), row, col), newLineWord.rstrip())
							else:
								stackSize -= 1
						break
				offsetToNextLine += newLine.size()

		startSection = ""
		endSection = ""
		seperator = ""
		scopesStr = view.scope_name(point)
		scopeList = scopesStr.split(' ')
		for scope in scopeList:
			if scope == "keyword.control.preprocessor.hlsl":
				posWord = view.word(point)
				ifdefWord = view.substr(posWord)
				if ifdefWord in PreprocessorBlockListScanDown:
					endSection = ScanDown(view, point)
					break
				elif ifdefWord in PreprocessorBlockListScanUp:
					startSection = ScanUp(view, point)
					break
				elif ifdefWord in PreprocessorBlockListScanBoth:
					endSection = ScanDown(view, point)
					startSection = ScanUp(view, point)
					seperator = "<br>"
					break
		if (len(startSection) != 0) or (len(endSection) != 0):
			do_hover(view, point, startSection, endSection, seperator)


# ----------------------------------
# -           Hover Docs           -
# ----------------------------------

def show_hover_docs(view, point, scope, collection):
	style = settings.get("DocsPopupStyle")
	if style == "dark":
		style = """
					body {
						font-family: system;
						margin: 0;
						padding: 0.35rem;
						border: 0.2rem solid rgb(46, 46, 46);
						background-color: rgb(5, 5, 5);
					}
					p {
						font-size: 1.0rem;
						margin: 0;
					}
				"""
	elif style == "none":
		style = """
					body {
						font-family: system;
					}
					p {
						font-size: 1.0rem;
						margin: 0;
					}
				"""
	elif style == "dynamic":
		if scope == "keyword.effect":
			style = """
						body {
							font-family: system;
							margin: 0;
							padding: 0.35rem;
							border: 0.15rem solid rgb(128, 26, 0);
							background-color: rgb(10, 10, 10);
						}
						p {
							font-size: 1.0rem;
							margin: 0;
						}
					"""
		elif scope == "string.trigger":
			style = """
						body {
							font-family: system;
							margin: 0;
							padding: 0.35rem;
							border: 0.15rem solid rgb(123, 123, 0);
							background-color: rgb(10, 10, 10);
						}
						p {
							font-size: 1.0rem;
							margin: 0;
						}
					"""
		elif scope == "storage.type.scope":
			style = """
						body {
							font-family: system;
							margin: 0;
							padding: 0.35rem;
							border: 0.15rem solid rgb(0, 122, 153);
							background-color: rgb(10, 10, 10);
						}
						p {
							font-size: 1.0rem;
							margin: 0;
						}
					"""
	item = view.substr(view.word(point))
	if item in collection:
		desc = collection[item]
		hoverBody = """
			<body id="vic-body">
				<style>%s</style>
				<p>%s</p>
			</body>
		""" %(style, desc)

		view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY |sublime.COOPERATE_WITH_AUTO_COMPLETE |sublime.HIDE_ON_CHARACTER_EVENT),
						location=point, max_width=1024)
		return

class ScriptHoverListener(sublime_plugin.EventListener):

	def on_hover(self, view, point, hover_zone):

		if not view:
			return

		try:
			if view.syntax().name == "Victoria Script" or view.syntax().name == "Victoria Gui":
				pass
			else:
				return
		except AttributeError:
			return

		if view.syntax().name == "Victoria Script":
			if settings.get("DocsHoverEnabled") == True:
				if view.match_selector(point, "keyword.effect"):
					show_hover_docs(view, point, "keyword.effect", GameData.EffectsList)

				if view.match_selector(point, "string.trigger"):
					GameData.TriggersList.update(GameData.CustomTriggersList)
					show_hover_docs(view, point, "string.trigger", GameData.TriggersList)

				if view.match_selector(point, "storage.type.scope"):
					GameData.ScopesList.update(GameData.CustomScopesList)
					show_hover_docs(view, point, "storage.type.scope", GameData.ScopesList)

				# Do everything that requires fetching GameObjects in non-blocking thread
				sublime.set_timeout_async(lambda: self.do_hover_async(view, point), 0)

			# Event Videos
			if settings.get("BinkVideoHover") == True:
				posLine = view.line(point)
				posa = posLine.a + 1
				posb = posLine.b - 1
				video_raw_start = view.find("video = ", posLine.a)
				word_position_b = posLine.b - 6
				video_region = sublime.Region(video_raw_start.b, posb)
				video_file = view.substr(video_region).replace("\"", "").replace("video = ", "").replace(" ", "").replace("\t", "")
				global video_point, video_file_path
				if video_file in GameData.EventVideos:
					video_file_path = v3_files_path + "\\" + video_file
					if not os.path.exists(video_file_path):
						# Check mod paths if it's not vanilla
						for mod in v3_mod_files:
							mod_path = mod + "\\" + video_file
							if os.path.exists(mod_path):
								video_file_path = mod_path
					video_name = view.substr(view.word(word_position_b))
					video_point = point
					if video_region.__contains__(point):
						self.show_video_hover_popup(view, point, video_name)
				else:
					video_point = None

			# Event Sound
			if settings.get("EventSoundPopup") == True:
				posLine = view.line(point)
				if "event:/SFX/Events" in view.substr(posLine):
					sound_raw_start = view.find("event:", posLine.a)
					global sound_region
					sound_region = sublime.Region(sound_raw_start.a, posLine.b - 1)
					sound_string = view.substr(sound_region).replace("\"", "")
					if sound_string in GameData.EventSoundsList and sound_region.__contains__(point):
						self.show_event_sound_hover_popup(view, point)
				else:
					global show_sound_menu
					show_sound_menu = False

		# Texture popups can happen for both script and gui files
		if settings.get("TextureOpenPopup") == True:
			posLine = view.line(point)
			if ".dds" in view.substr(posLine):
				texture_raw_start = view.find("gfx", posLine.a)
				texture_raw_end = view.find(".dds", posLine.a)
				texture_raw_region = sublime.Region(texture_raw_start.a, texture_raw_end.b)
				texture_raw_path = view.substr(texture_raw_region)
				full_texture_path = v3_files_path + "\\" + texture_raw_path
				if not os.path.exists(full_texture_path):
					# Check mod paths if it's not vanilla
					for mod in v3_mod_files:
						if os.path.exists(mod):
							if mod.endswith("mod"):
								# if it is the path to the mod directory, get all directories in it
								for directory in [ f.path for f in os.scandir(mod) if f.is_dir() ]:
									mod_path = directory + "\\" + texture_raw_path
									if os.path.exists(mod_path): full_texture_path = mod_path
							else:
								mod_path = mod + "\\" + texture_raw_path
								if os.path.exists(mod_path): full_texture_path = mod_path
				full_texture_path = full_texture_path.replace("/", "\\")
				# The path exists and the point in the view is inside of the path
				if texture_raw_region.__contains__(point):
					texture_name = view.substr(view.word(texture_raw_end.a - 1))
					self.show_texture_hover_popup(view, point, texture_name, full_texture_path)

	def do_hover_async(self, view, point):
		word_region = view.word(point)
		word = view.substr(word_region)

		# Fix hovered word for event ids so something like "cold.100" will work 
		if view.substr(word_region.b) == ".":
			word += "."
			word += view.substr(view.word(word_region.b + 1))
		if view.substr(word_region.a-1) == ".":
			word = view.substr(view.word(word_region.a - 1)) + "." + word

		# Check if currently hovered word is equal to any game object and show goto definition popup if found	
		if ai_strats.contains(word):
			self.show_popup_default(view, point, word, ai_strats.access(word), "Ai Strategies")

		if bgs.contains(word):
			self.show_popup_default(view, point, word, bgs.access(word), "Building Group")

		if buildings.contains(word):
			self.show_popup_default(view, point, word, buildings.access(word), "Building")

		if char_traits.contains(word):
			self.show_popup_default(view, point, word, char_traits.access(word), "Character Trait")

		if cultures.contains(word):
			self.show_popup_default(view, point, word, cultures.access(word), "Culture")

		if decrees.contains(word):
			self.show_popup_default(view, point, word, decrees.access(word), "Decree")

		if diplo_actions.contains(word):
			self.show_popup_default(view, point, word, diplo_actions.access(word), "Diplomatic Action")

		if diplo_plays.contains(word):
			self.show_popup_default(view, point, word, diplo_plays.access(word), "Diplomatic Play")

		if game_rules.contains(word):
			self.show_popup_default(view, point, word, game_rules.access(word), "Game Rule")

		if goods.contains(word):
			self.show_popup_default(view, point, word, goods.access(word), "Trade Good")

		if gov_types.contains(word):
			self.show_popup_default(view, point, word, gov_types.access(word), "Government Type")
		
		if ideologies.contains(word):
			self.show_popup_default(view, point, word, ideologies.access(word), "Ideology")

		if institutions.contains(word):
			self.show_popup_default(view, point, word, institutions.access(word), "Institution")

		if ig_traits.contains(word):
			self.show_popup_default(view, point, word, ig_traits.access(word), "Interest Group Traits")

		if igs.contains(word):
			self.show_popup_default(view, point, word, igs.access(word), "Interest Group")

		if jes.contains(word):
			self.show_popup_default(view, point, word, jes.access(word), "Journal Entry")
		
		if law_groups.contains(word):
			self.show_popup_default(view, point, word, law_groups.access(word), "Law Group")

		if laws.contains(word):
			self.show_popup_default(view, point, word, laws.access(word), "Law")

		if mods.contains(word):
			self.show_popup_default(view, point, word, mods.access(word), "Modifier")

		if op_mods.contains(word):
			self.show_popup_default(view, point, word, op_mods.access(word), "Opinion Modifier")

		if parties.contains(word):
			self.show_popup_default(view, point, word, parties.access(word), "Party")
		
		if pop_needs.contains(word):
			self.show_popup_default(view, point, word, pop_needs.access(word), "Pop Need")

		if pop_types.contains(word):
			self.show_popup_default(view, point, word, pop_types.access(word), "Pop Type")

		if pm_groups.contains(word):
			self.show_popup_default(view, point, word, pm_groups.access(word), "Production Method Group")
		
		if pms.contains(word):
			self.show_popup_default(view, point, word, pms.access(word), "Production Method")

		if religions.contains(word):
			self.show_popup_default(view, point, word, religions.access(word), "Religion")

		if script_values.contains(word):
			self.show_popup_default(view, point, word, script_values.access(word), "Script Value")

		if scripted_effects.contains(word):
			self.show_popup_default(view, point, word, scripted_effects.access(word), "Scripted Effect")

		if scripted_modifiers.contains(word):
			self.show_popup_default(view, point, word, scripted_modifiers.access(word), "Scripted Modifer")

		if scripted_triggers.contains(word):
			self.show_popup_default(view, point, word, scripted_triggers.access(word), "Scripted Trigger")
		
		if state_traits.contains(word):
			self.show_popup_default(view, point, word, state_traits.access(word), "State Trait")

		if strategic_regions.contains(word):
			self.show_popup_default(view, point, word, strategic_regions.access(word), "Strategic Region")

		if subject_types.contains(word):
			self.show_popup_default(view, point, word, subject_types.access(word), "Subject Types")

		if technologies.contains(word):
			self.show_popup_default(view, point, word, technologies.access(word), "Technology")

		if terrains.contains(word):
			self.show_popup_default(view, point, word, terrains.access(word), "Terrain")

		if state_regions.contains(word):
			self.show_popup_default(view, point, word, state_regions.access(word), "State Region")

		if events.contains(word):
			self.show_popup_default(view, point, word, events.access(word), "Events")
		
	def show_popup_default(self, view, point, word, PdxObject, header):
		goto_args = { "path": PdxObject.path, "line": PdxObject.line}
		goto_url = sublime.command_url("goto_script_object_definition", goto_args)
		hoverBody = """
			<body id="vic-body">
				<style>%s</style>
				<h1>%s</h1>
				<p>Name: <span id="name">%s</span></p>
				<a href="%s" title="Open %s and goto line %d">Goto Definition</a>
			</body>
		""" %(css_basic_style, header, word, goto_url, PdxObject.path.rpartition("\\")[2], PdxObject.line)

		view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY |sublime.COOPERATE_WITH_AUTO_COMPLETE |sublime.HIDE_ON_CHARACTER_EVENT),
						location=point, max_width=1024)

	def show_texture_hover_popup(self, view, point, texture_name, full_texture_path):
		args = { "path": full_texture_path }
		open_texture_url = sublime.command_url("open_pdx_texture ", args)
		folder_args = { "path": full_texture_path, "folder": True}
		open_folder_url = sublime.command_url("open_pdx_texture ", folder_args)
		hoverBody = """
			<body id=\"vic-body\">
				<style>%s</style>
				<h1>Open Texture</h1>
				<div></div>
				<a href="%s" title="Open folder containing the texture.">Open Folder</a>
				<br>
				<a href="%s" title="Open texture with the default program.">Open %s.dds</a>
			</body>
		""" %(css_basic_style, open_folder_url, open_texture_url, texture_name)

		view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY
						|sublime.COOPERATE_WITH_AUTO_COMPLETE |sublime.HIDE_ON_CHARACTER_EVENT),
						location=point, max_width=802)

	def show_event_sound_hover_popup(self, view, point):
		global show_sound_menu
		show_sound_menu = True
		browse_url = sublime.command_url("browse_event_sound")
		hoverBody = """
			<body id=\"vic-body\">
				<style>%s</style>
				<h1>Event Sound</h1>
				<div></div>
				<a href="%s" title="Replace current event sound with a new one...">Browse event audio</a>
			</body>
		""" %(css_basic_style, browse_url)

		view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY
						|sublime.COOPERATE_WITH_AUTO_COMPLETE |sublime.HIDE_ON_CHARACTER_EVENT),
						location=point, max_width=802)

	def show_video_hover_popup(self, view, point, word):
		args = { "play": True }
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
		""" %(css_basic_style, word, browse_and_play_url)

		view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY
						|sublime.COOPERATE_WITH_AUTO_COMPLETE |sublime.HIDE_ON_CHARACTER_EVENT),
						location=point, max_width=802)

#Global so I don't have to deal with passing through the hrefs, should probably just pass them as args.
video_file_path = False
video_point = None
edit_obj = None # Used to pass edit object to on_done
show_sound_menu = False
sound_region = False

class GotoScriptObjectDefinitionCommand(sublime_plugin.WindowCommand):
	def run(self, path, line):
		file_path = "{}:{}:{}".format(path, line, 0)
		view = self.window.open_file(file_path, sublime.ENCODED_POSITION)

class OpenPdxTextureCommand(sublime_plugin.WindowCommand):
	def run(self, path, folder=False):
		if folder:
			end = path.rfind("\\")
			path = path[0:end:]
			os.startfile(path)
		else:
			os.startfile(path)

class PlayBinkVideoCommand(sublime_plugin.WindowCommand):
	def run(self):
		global video_file_path
		if video_file_path:
			os.startfile(video_file_path)

class BrowseEventSoundCommand(sublime_plugin.TextCommand):

	def input_description(self):
		return "Select Sound"

	def input(self, args):
		if 'sound' not in args:
			return SoundInputHandler()

	def run(self, edit, sound):
		global sound_region
		sound = "event:/SFX/Events/" + sound
		self.view.replace(edit, sound_region, sound)

	def is_visible(self):
		# Won't show in the command pallete normally but will still be avilable for commands
		global show_sound_menu
		if show_sound_menu: return True
		else: return False

class BrowseBinkVideosCommand(sublime_plugin.TextCommand):

	def run(self, edit, video, play=False):
		global edit_obj
		edit_obj = edit
		if video:
			if play:
				self.on_done(video, play=True)
			else:
				self.on_done(video)

	def input_description(self):
		return "Select Video"

	def input(self, args):
		if 'video' not in args:
			return VideoInputHandler()

	def on_done(self, video, play=False):
		global video_point, edit_obj
		video = "gfx/event_pictures/" + video
		video_path = v3_files_path + "\\" + video
		if not os.path.exists(video_path):
			# Check mod paths if it's not vanilla
			for mod in v3_mod_files:
				mod_path = mod + "\\" + video
				if os.path.exists(mod_path):
					video_path = mod_path

		# If opened with command pallete it will just show the video, not try to replace text.
		if video_point is None:
			os.startfile(video_path)
			return
		view = self.view
		posLine = view.line(video_point)
		posa = posLine.a + 1
		posb = posLine.b - 1
		word_position_b = posLine.b - 6
		video_file = view.substr(sublime.Region(posa, posb)).replace("\"", "").replace("video = ", "").replace(" ", "").replace("\t", "")
		actual_video_region = view.find(video_file, posa)
		view.replace(edit_obj, actual_video_region, video)
		video_point = None
		edit_obj = None
		video_file_path = False
		if play:
			os.startfile(video_path)

class VideoInputHandler(sublime_plugin.ListInputHandler):

	def name(self):
		return 'video'

	def list_items(self):
		keys = []
		for x in GameData.EventVideos: keys.append(x.replace("gfx/event_pictures/", ""))
		return keys

class SoundInputHandler(sublime_plugin.ListInputHandler):

	def name(self):
		return 'sound'

	def list_items(self):
		keys = []
		for x in GameData.EventSoundsList: keys.append(x.replace("event:/SFX/Events/", ""))
		return sorted(keys)
