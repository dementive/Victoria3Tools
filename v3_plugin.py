import sublime
import sublime_plugin
import os
import re
import webbrowser
import threading
import subprocess
import time
from collections import deque
from .jomini import GameObjectBase, PdxScriptObjectType, PdxScriptObject
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

# Gui Game Class implementations


class GuiType(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("gui")

	def get_pdx_object_list(self, path: str) -> PdxScriptObjectType:
		obj_list = list()
		for dirpath, dirnames, filenames in os.walk(path):
			for filename in [f for f in filenames if f.endswith(".gui")]:
				if filename in self.ignored_files:
					continue
				file_path = os.path.join(dirpath, filename)
				if self.included_files:
					if filename not in self.included_files:
						continue
				with open(file_path, "r", encoding='utf-8-sig') as file:
					for i, line in enumerate(file):
						if self.should_read(line):
							found_item = re.search("type\s([A-Za-z_][A-Za-z_0-9]*)\s?=", line)
							if found_item and found_item.groups()[0]:
								found_item = found_item.groups()[0]
								obj_list.append(PdxScriptObject(found_item, file_path, i + 1))
		return PdxScriptObjectType(obj_list)

	def should_read(self, x: str) -> bool:
		# Check if a line should be read
		return re.search("type\s[A-Za-z_][A-Za-z_0-9]*\s?=", x)


class GuiTemplate(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("gui")

	def get_pdx_object_list(self, path: str) -> PdxScriptObjectType:
		obj_list = list()
		for dirpath, dirnames, filenames in os.walk(path):
			for filename in [f for f in filenames if f.endswith(".gui")]:
				if filename in self.ignored_files:
					continue
				file_path = os.path.join(dirpath, filename)
				if self.included_files:
					if filename not in self.included_files:
						continue
				with open(file_path, "r", encoding='utf-8-sig') as file:
					for i, line in enumerate(file):
						if self.should_read(line):
							found_item = re.search("template\s([A-Za-z_][A-Za-z_0-9]*)", line)
							if found_item and found_item.groups()[0]:
								found_item = found_item.groups()[0]
								obj_list.append(PdxScriptObject(found_item, file_path, i + 1))
		return PdxScriptObjectType(obj_list)

	def should_read(self, x: str) -> bool:
		# Check if a line should be read
		return re.search("template\s[A-Za-z_][A-Za-z_0-9]*", x)

# Victoria 3 Game Object Class implementations


class V3AiStrategy(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\ai_strategies")


class V3BuildingGroup(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\building_groups")


class V3Building(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\building")


class V3CharacterTrait(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\character_traits")


class V3Culture(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\cultures")


class V3Decree(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\decrees")


class V3DiplomaticAction(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\diplomatic_actions")


class V3DiplomaticPlay(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\diplomatic_plays")


class V3GameRules(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\game_rules")


class V3Goods(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\goods")


class V3GovernmentType(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\government_types")


class V3Ideology(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\ideologies")


class V3Institutions(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\institutions")


class V3Ideology(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\ideologies")


class V3InterestGroupTrait(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\interest_group_traits")


class V3InterestGroup(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\interest_groups")


class V3JournalEntry(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\journal_entries")


class V3LawGroup(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\law_groups")


class V3Law(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\laws")


class V3Modifier(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\modifiers")


class V3Party(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\parties")


class V3PopNeed(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\pop_needs")


class V3PopType(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\pop_types")


class V3ProductionMethodGroup(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\production_method_groups")


class V3ProductionMethod(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\production_methods")


class V3Religion(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\religions")


class V3ScriptValue(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\script_values")


class V3ScriptedEffect(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\scripted_effects")


class V3ScriptedModifier(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\scripted_modifiers")


class V3ScriptedTrigger(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\scripted_triggers")


class V3StateTrait(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\state_traits")


class V3StrategicRegion(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\strategic_regions")


class V3SubjectType(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\subject_types")


class V3Technology(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\technology")


class V3Terrain(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("common\\terrain")


class V3StateRegion(GameObjectBase):
	def __init__(self):
		super().__init__(file_paths)
		self.get_data("map_data\\state_regions")


# Game Data class
GameData = GameData()

# Gui globals

gui_types = gui_templates = ""

# Global Object Variables that get set on plugin_loaded
ai_strats = bgs = buildings = char_traits = cultures = mods = decrees = diplo_actions = diplo_plays = ""
game_rules = goods = gov_types = ideologies = institutions = ig_traits = igs = jes = law_groups = laws = ""
parties = pop_needs = pop_types = pm_groups = pms = religions = state_traits = strategic_regions = ""
subject_types = technologies = terrains = state_regions = ""
script_values = scripted_effects = scripted_modifiers = scripted_triggers = ""
# Function to fill all global game objects that get set in non-blocking async function on plugin_loaded
# Setting all the objects can be slow and doing it on every hover (when they are actually used) is even slower,
# so loading it all in on plugin init makes popups actually responsive


def load_game_objects():
	t0 = time.time()

	def load_first():
		global ai_strats, bgs, buildings, char_traits, cultures, decrees, diplo_actions, diplo_plays
		ai_strats = V3AiStrategy()
		bgs = V3BuildingGroup()
		buildings = V3Building()
		for i in [x for x in buildings.keys() if "bg_" in x]:
			buildings.remove(i)
		char_traits = V3CharacterTrait()
		cultures = V3Culture()
		decrees = V3Decree()
		diplo_actions = V3DiplomaticAction()
		diplo_plays = V3DiplomaticPlay()

	def load_second():
		global mods, game_rules, goods, gov_types, ideologies, institutions, ig_traits, igs
		mods = V3Modifier()
		game_rules = V3GameRules()
		goods = V3Goods()
		gov_types = V3GovernmentType()
		ideologies = V3Ideology()
		institutions = V3Institutions()
		ig_traits = V3InterestGroupTrait()
		igs = V3InterestGroup()

	def load_third():
		global jes, law_groups, laws, parties, pop_needs, pop_types, pm_groups
		jes = V3JournalEntry()
		law_groups = V3LawGroup()
		laws = V3Law()
		parties = V3Party()
		pop_needs = V3PopNeed()
		pop_types = V3PopType()
		pm_groups = V3ProductionMethodGroup()

	def load_fourth():
		global pms, religions, script_values, scripted_effects, scripted_modifiers, scripted_triggers
		pms = V3ProductionMethod()
		religions = V3Religion()
		script_values = V3ScriptValue()
		scripted_effects = V3ScriptedEffect()
		scripted_modifiers = V3ScriptedModifier()
		scripted_triggers = V3ScriptedTrigger()

	def load_fifth():
		global state_traits, strategic_regions, subject_types, technologies, terrains, state_regions
		state_traits = V3StateTrait()
		strategic_regions = V3StrategicRegion()
		subject_types = V3SubjectType()
		technologies = V3Technology()
		terrains = V3Terrain()
		state_regions = V3StateRegion()

	thread1 = threading.Thread(target=load_first)
	thread2 = threading.Thread(target=load_second)
	thread3 = threading.Thread(target=load_third)
	thread4 = threading.Thread(target=load_fourth)
	thread5 = threading.Thread(target=load_fifth)
	thread1.start()
	thread2.start()
	thread3.start()
	thread4.start()
	thread5.start()
	thread1.join()
	thread2.join()
	thread3.join()
	thread4.join()
	thread5.join()

	# Write syntax data after creating objects so they actually exist when writing
	sublime.set_timeout_async(lambda: write_data_to_syntax(), 0)

	# Load gui objects after script objects
	sublime.set_timeout_async(lambda: load_gui_objects(), 0)

	t1 = time.time()
	print("Time taken to load Victoria 3 objects: {:.3f} seconds".format(t1 - t0))


def load_gui_objects():
	# t0 = time.time()

	def load_first():
		global gui_types
		gui_types = GuiType()

	def load_second():
		global gui_templates
		gui_templates = GuiTemplate()
		gui_templates.remove("inside")
		gui_templates.remove("you")
		gui_templates.remove("can")
		gui_templates.remove("but")
		gui_templates.remove("on")
		gui_templates.remove("within")
		gui_templates.remove("names")

	thread1 = threading.Thread(target=load_first)
	thread2 = threading.Thread(target=load_second)
	thread1.start()
	thread2.start()

	# t1 = time.time()
	# print("Time taken to load pdx GUI objects: {:.3f} seconds".format(t1 - t0))


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

# KIND_ID_AMBIGUOUS - transparent
# KIND_ID_KEYWORD - red
# KIND_ID_TYPE - purple
# KIND_ID_FUNCTION - red
# KIND_ID_NAMESPACE - light blue
# KIND_ID_NAVIGATION - yellow
# KIND_ID_MARKUP - orange
# KIND_ID_VARIABLE - light greenish blue
# KIND_ID_SNIPPET - green
KIND_EFFECT = (sublime.KIND_ID_FUNCTION, "E", "Effect")
KIND_TRIGGER = (sublime.KIND_ID_NAVIGATION, "T", "Trigger")
KIND_AI_STRAT = (sublime.KIND_ID_MARKUP, "A", "Ai Strategy")
KIND_BUILDING = (sublime.KIND_ID_VARIABLE, "B", "Building")
KIND_BUILDING_GROUP = (sublime.KIND_ID_VARIABLE, "B", "Building Group")
KIND_CHAR_TRAIT = (sublime.KIND_ID_VARIABLE, "C", "Character Trait")
KIND_CULTURE = (sublime.KIND_ID_NAMESPACE, "C", "Culture")
KIND_DECREE = (sublime.KIND_ID_MARKUP, "D", "Decree")
KIND_DIPLO_ACTION = (sublime.KIND_ID_SNIPPET, "D", "Diplomatic Action")
KIND_DIPLO_PLAY = (sublime.KIND_ID_SNIPPET, "D", "Diplomatic Play")

FIND_SIMPLE_DECLARATION_RE = "\s?=\s?(\")?"
FIND_ERROR_RE = "\s?=\s?\"?([A-Za-z_][A-Za-z_0-9]*)\"?"
FIND_SCOPE_RE = ":\"?([A-Za-z_][A-Za-z_0-9]*)\"?"


class V3CompletionsEventListener(sublime_plugin.EventListener):

	def __init__(self):
		self.trigger_field = False
		self.effect_field = False
		self.modifier_field = False
		self.mtth_field = False
		self.trigger_views = []
		self.effect_views = []
		self.modfier_views = []
		self.mtth_views = []

		self.show_ai = False
		self.show_b = False
		self.show_bg = False
		self.show_c_traits = False
		self.show_ai_views = []
		self.show_b_views = []
		self.show_bg_views = []
		self.show_c_traits_views = []

		self.culture = False
		self.culture_views = []
		self.decree = False
		self.decree_views = []
		self.diplo_action = False
		self.diplo_action_views = []
		self.diplo_play = False
		self.diplo_play_views = []

		self.error_words = []

	def on_deactivated_async(self, view):
		"""
				Remove field states when view loses focus
				if cursor was in a field in the old view but not the new view the completions will still be accurate
				save the id of the view so it can be readded when it regains focus
		"""
		vid = view.id()
		if self.trigger_field:
			self.trigger_field = False
			self.trigger_views.append(vid)
		if self.effect_field:
			self.effect_field = False
			self.effect_views.append(vid)
		if self.modifier_field:
			self.modifier_field = False
			self.modfier_views.append(vid)
		if self.mtth_field:
			self.mtth_field = False
			self.mtth_views.append(vid)
		if self.show_ai:
			self.show_ai = False
			self.show_ai_views.append(vid)
		if self.show_b:
			self.show_b = False
			self.show_b_views.append(vid)
		if self.show_bg:
			self.show_bg = False
			self.show_bg_views.append(vid)
		if self.show_c_traits:
			self.show_c_traits = False
			self.show_c_traits_views.append(vid)
		if self.culture:
			self.culture = False
			self.culture_views.append(vid)
		if self.decree:
			self.decree = False
			self.decree_views.append(vid)

		if self.diplo_action:
			self.diplo_action = False
			self.diplo_action_views.append(vid)
		if self.diplo_play:
			self.diplo_play = False
			self.diplo_play_views.append(vid)

	def on_activated_async(self, view):
		vid = view.id()
		if vid in self.trigger_views:
			self.trigger_field = True
			self.trigger_views.remove(vid)
		if vid in self.effect_views:
			self.effect_field = True
			self.effect_views.remove(vid)
		if vid in self.modfier_views:
			self.modifier_field = True
			self.modfier_views.remove(vid)
		if vid in self.mtth_views:
			self.mtth_field = True
			self.mtth_views.remove(vid)
		if self.show_ai_views:
			self.show_ai = True
			self.show_ai_views.remove(vid)
		if self.show_b_views:
			self.show_b = True
			self.show_b_views.remove(vid)
		if self.show_bg_views:
			self.show_bg = True
			self.show_bg_views.remove(vid)
		if self.show_c_traits_views:
			self.show_c_traits = True
			self.show_c_traits_views.remove(vid)

		if self.culture_views:
			self.culture = True
			self.culture_views.remove(vid)
		if self.decree_views:
			self.decree = True
			self.decree_views.remove(vid)

		if self.diplo_action_views:
			self.diplo_action = True
			self.diplo_action_views.remove(vid)
		if self.diplo_play_views:
			self.diplo_play = True
			self.diplo_play_views.remove(vid)

	def on_query_completions(self, view, prefix, locations):

		if not view:
			return None

		try:
			if view.syntax().name != "Victoria Script" and view.syntax().name != "PdxPython":
				return None
		except AttributeError:
			return None

		fname = view.file_name()

		if self.show_ai:
			self.show_ai = False
			ai = ai_strats.keys()
			ai = sorted(ai)
			return sublime.CompletionList(
				[
					sublime.CompletionItem(
						trigger=key,
						completion_format=sublime.COMPLETION_FORMAT_TEXT,
						kind=KIND_AI_STRAT,
						details=" "
					)
					# Calling sorted() twice makes it so completions are ordered by
					# 1. the number of times they appear in the current buffer
					# 2. if they dont appear they show up alphabetically
					for key in sorted(ai)
				],
				flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS
			)
		if self.show_b:
			self.show_b = False
			b = buildings.keys()
			b = sorted(b)
			return sublime.CompletionList(
				[
					sublime.CompletionItem(
						trigger=key,
						completion_format=sublime.COMPLETION_FORMAT_TEXT,
						kind=KIND_BUILDING,
						details=" "
					)
					for key in sorted(b)
				],
				flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS
			)
		if self.show_bg:
			self.show_bg = False
			bg = bgs.keys()
			bg = sorted(bg)
			return sublime.CompletionList(
				[
					sublime.CompletionItem(
						trigger=key,
						completion_format=sublime.COMPLETION_FORMAT_TEXT,
						kind=KIND_BUILDING_GROUP,
						details=" "
					)
					for key in sorted(bg)
				],
				flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS
			)
		if self.show_c_traits:
			self.show_c_traits = False
			ct = char_traits.keys()
			ct = sorted(ct)
			return sublime.CompletionList(
				[
					sublime.CompletionItem(
						trigger=key,
						completion_format=sublime.COMPLETION_FORMAT_TEXT,
						kind=KIND_CHAR_TRAIT,
						details=" "
					)
					for key in sorted(ct)
				],
				flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS
			)
		if self.culture:
			self.culture = False
			cu = cultures.keys()
			cu = sorted(cu)
			return sublime.CompletionList(
				[
					sublime.CompletionItem(
						trigger=key,
						completion_format=sublime.COMPLETION_FORMAT_TEXT,
						kind=KIND_CULTURE,
						details=" "
					)
					for key in sorted(cu)
				],
				flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS
			)
		if self.decree:
			self.decree = False
			de = decrees.keys()
			de = sorted(de)
			return sublime.CompletionList(
				[
					sublime.CompletionItem(
						trigger=key,
						completion_format=sublime.COMPLETION_FORMAT_TEXT,
						kind=KIND_DECREE,
						details=" "
					)
					for key in sorted(de)
				],
				flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS
			)
		if self.diplo_action:
			self.diplo_action = False
			da = diplo_actions.keys()
			da = sorted(da)
			return sublime.CompletionList(
				[
					sublime.CompletionItem(
						trigger=key,
						completion_format=sublime.COMPLETION_FORMAT_TEXT,
						kind=KIND_DIPLO_ACTION,
						details=" "
					)
					for key in sorted(da)
				],
				flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS
			)
		if self.diplo_play:
			self.diplo_play = False
			dp = diplo_plays.keys()
			dp = sorted(dp)
			return sublime.CompletionList(
				[
					sublime.CompletionItem(
						trigger=key,
						completion_format=sublime.COMPLETION_FORMAT_TEXT,
						kind=KIND_DIPLO_PLAY,
						details=" "
					)
					for key in sorted(dp)
				],
				flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS
			)
		else:
			if "script_values" in fname:
				e_list = []
				for i in GameData.EffectsList:
					e_list.append(sublime.CompletionItem(
						trigger=i,
						completion_format=sublime.COMPLETION_FORMAT_TEXT,
						kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
						details=GameData.EffectsList[i].split("<br>")[0]
					))
				t_list = []
				for i in GameData.TriggersList:
					t_list.append(sublime.CompletionItem(
						trigger=i,
						completion_format=sublime.COMPLETION_FORMAT_TEXT,
						kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
						details=GameData.TriggersList[i].split("<br>")[0]
					))
				return sublime.CompletionList(e_list + t_list)
			if self.trigger_field or self.mtth_field or "scripted_triggers" in fname or "scripted_modifiers" in fname:
				return sublime.CompletionList(
					[
						sublime.CompletionItem(
							trigger=key,
							completion_format=sublime.COMPLETION_FORMAT_TEXT,
							kind=(sublime.KIND_ID_NAVIGATION, "T", "Trigger"),
							details=GameData.TriggersList[key].split("<br>")[0]
						)
						for key in sorted(GameData.TriggersList)
					]
				)
			if self.effect_field or "scripted_effects" in fname:
				return sublime.CompletionList(
					[
						sublime.CompletionItem(
							trigger=key,
							completion_format=sublime.COMPLETION_FORMAT_TEXT,
							kind=(sublime.KIND_ID_FUNCTION, "E", "Effect"),
							details=GameData.EffectsList[key].split("<br>")[0]
						)
						for key in sorted(GameData.EffectsList)
					]
				)
			if self.modifier_field or re.search("common\\\s?(modifiers|traits|buildings|governor_policies)", fname):
				return sublime.CompletionList(
					[
						sublime.CompletionItem(
							trigger=key,
							completion_format=sublime.COMPLETION_FORMAT_TEXT,
							kind=(sublime.KIND_ID_MARKUP, "M", "Modifier"),
							details=GameData.ModifersList[key],
							annotation=GameData.ModifersList[key].replace("Category: ", "")
						)
						for key in sorted(GameData.ModifersList)
					],
					flags=sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS
				)
		return None

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

	def simple_scope_match(self, view):
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

		start_modifier_brackets = view.find_by_selector("meta.modifier.bracket")
		modifier_regions = []
		for br in start_modifier_brackets:
			modifier_regions.append(sublime.Region(br.a, self.getIndex(view_str, br.a)))

		selection = view.sel()
		if not selection[0].empty():
			return

		self.show_status(selection[0].a, trigger_regions, "trigger", view)

		# Have to account for trigger fields inside of effect fields, definetly a better way to do this.
		for block in effect_regions:
			if block.a <= selection[0].a <= block.b:
				view.set_status("effect", "Effect Field")
				self.effect_field = True
				for block in trigger_regions:
					if block.a <= selection[0].a <= block.b:
						view.erase_status("effect")
						self.effect_field = False
						view.set_status("trigger", "Trigger Field")
						self.trigger_field = True
						break
					else:
						view.erase_status("trigger")
						self.trigger_field = False
				break
			else:
				view.erase_status("effect")
				self.effect_field = False

		self.show_status(selection[0].a, modifier_regions, "modifier", view)

		self.show_status(selection[0].a, ai_regions, "mean time to happen", view)

	def show_status(self, selection, regions, status, view):
		for block in regions:
			if block.a <= selection <= block.b:
				view.set_status(status, status.title() + " Field")
				if status == "trigger":
					self.trigger_field = True
				elif status == "effect":
					self.effect_field = True
				elif status == "modifier":
					self.modifier_field = True
				elif status == "mean time to happen":
					self.mtth_field = True
				break
			else:
				view.erase_status(status)
				if status == "trigger":
					self.trigger_field = False
				elif status == "effect":
					self.effect_field = False
				elif status == "modifier":
					self.modifier_field = False
				elif status == "mean time to happen":
					self.mtth_field = False

	def reset_shown(self):
		# self.trigger_field = False
		# self.effect_field = False
		# self.modifier_field = False
		# self.mtth_field = False
		self.show_ai = False
		self.show_b = False
		self.show_bg = False
		self.show_c_traits = False
		self.culture = False
		self.decree = False
		self.diplo_action = False
		self.diplo_play = False

	def check_for_simple_completions(self, view, point):
		"""
						Check if the current cursor position should trigger a autocompletion item
						this is for simple declarations like: remove_building = CursorHere
		"""
		self.reset_shown()

		if view.substr(point) == "=":
			return

		line = view.substr(view.line(point))

		for i in self.error_words:
			if i in line:
				view.erase_regions(i)
				self.error_words.remove(i)

		ai_list = ["has_strategy", "set_strategy"]
		b_list = [
			"start_building_construction", "remove_building",
			"start_building_construction", "activate_building", "deactivate_building",
			"start_privately_funded_building_construction", "building", "building_type",
			"has_building", "is_building_type", "pop_employment_building", "has_active_building",
			"set_available_for_autonomous_investment", "unset_available_for_autonomous_investment",
			"start_privately_funded_building_construction"
		]
		bg_list = [
			"force_resource_depletion", "force_resource_discovery", "pop_employment_building_group",
			"is_building_group", "has_potential_resource", "building_group"
		]
		char_traits_list = ["add_trait", "remove_trait", "has_trait"]
		culture_list = [
			"has_culture_graphics", "country_has_primary_culture",
			"has_pop_culture", "is_homeland", "add_homeland", "remove_homeland", "culture"
		]
		decree_list = ["has_decree"]
		diplo_action_list = ["is_diplomatic_action_type"]
		diplo_play_list = ["is_diplomatic_play_type"]
		# Ai Strats
		for i in ai_list:
			# Error checking if I end up wanting it
			# match = re.search(f"{i}{FIND_ERROR_RE}", line)
			# if match and match.groups()[0] not in keys:
			# 	word = match.groups()[0]
			# 	error_region = sublime.Region((line.rfind(word) + view.line(point).a), (line.rfind(word) + len(word)) + view.line(point).a)
			# 	view.add_regions(view.substr(error_region), [error_region], "invalid", "", sublime.PERSISTENT | sublime.DRAW_SOLID_UNDERLINE |sublime.DRAW_NO_OUTLINE )
			# 	self.error_words.append(view.substr(error_region))
			r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
			if r:
				y = 0
				idx = line.index(i) + view.line(point).a + len(i) + 2
				if r.groups()[0] == "\"":
					y = 2  # move over another position if quote is present
				# Check if current point is in one of 3 positions: ={1nospace}{2space}{3quote}
				if idx == point or idx + y == point or idx + 1 == point:
					#
					# if len([x for x in ai_strats.keys() if x in line]) == 0:
					self.show_ai = True
					view.run_command("auto_complete")
					break
		# Buildings
		for i in b_list:
			r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
			if r:
				y = 0
				idx = line.index(i) + view.line(point).a + len(i) + 2
				if r.groups()[0] == "\"":
					y = 2
				if idx == point or idx + y == point or idx + 1 == point:
					self.show_b = True
					view.run_command("auto_complete")
					break
		# Building Scopes
		if "b:" in line:
			idx = line.index("b:") + view.line(point).a + 2  # add the length of "b:" so index is at the end where completion should happen
			if idx == point:
				self.show_b = True
				view.run_command("auto_complete")
		# Building Groups
		for i in bg_list:
			r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
			if r:
				y = 0
				idx = line.index(i) + view.line(point).a + len(i) + 2
				if r.groups()[0] == "\"":
					y = 2
				if idx == point or idx + y == point or idx + 1 == point:
					self.show_bg = True
					view.run_command("auto_complete")
					break
		# Character Traits
		for i in char_traits_list:
			r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
			if r:
				y = 0
				idx = line.index(i) + view.line(point).a + len(i) + 2
				if r.groups()[0] == "\"":
					y = 2
				if idx == point or idx + y == point or idx + 1 == point:
					self.show_c_traits = True
					view.run_command("auto_complete")
					break
		# Culture Scopes
		if "cu:" in line:
			idx = line.index("cu:") + view.line(point).a + 3
			if idx == point:
				self.culture = True
				view.run_command("auto_complete")
		# Cultures
		for i in culture_list:
			r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
			if r:
				y = 0
				idx = line.index(i) + view.line(point).a + len(i) + 2
				if r.groups()[0] == "\"":
					y = 2
				if idx == point or idx + y == point or idx + 1 == point:
					self.culture = True
					view.run_command("auto_complete")
					break
		# Decree Scopes
		if "decree_cost:" in line:
			idx = line.index("decree_cost:") + view.line(point).a + 12
			if idx == point:
				self.decree = True
				view.run_command("auto_complete")
		# Decrees
		for i in decree_list:
			r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
			if r:
				y = 0
				idx = line.index(i) + view.line(point).a + len(i) + 2
				if r.groups()[0] == "\"":
					y = 2
				if idx == point or idx + y == point or idx + 1 == point:
					self.decree = True
					view.run_command("auto_complete")
					break
		# Diplo Actions
		for i in diplo_action_list:
			r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
			if r:
				y = 0
				idx = line.index(i) + view.line(point).a + len(i) + 2
				if r.groups()[0] == "\"":
					y = 2
				if idx == point or idx + y == point or idx + 1 == point:
					self.diplo_action = True
					view.run_command("auto_complete")
					break
		# Diplo Plays
		for i in diplo_play_list:
			r = re.search(f"{i}{FIND_SIMPLE_DECLARATION_RE}", line)
			if r:
				y = 0
				idx = line.index(i) + view.line(point).a + len(i) + 2
				if r.groups()[0] == "\"":
					y = 2
				if idx == point or idx + y == point or idx + 1 == point:
					self.diplo_play = True
					view.run_command("auto_complete")
					break

	def check_for_complex_completions(self, view, point):
		view_str = view.substr(sublime.Region(0, view.size()))

		start_bg_brackets = view.find_by_selector("meta.bg.bracket")
		start_da_brackets = view.find_by_selector("meta.da.bracket")
		start_dp_brackets = view.find_by_selector("meta.dp.bracket")

		for br in start_bg_brackets:
			print(start_bg_brackets)
			i = sublime.Region(br.a, self.getIndex(view_str, br.a))
			s = view.substr(i)
			if "type = " in s:
				fpoint = (s.index("type = ") + 7) + i.a  # add 7 = amount of chars in "type = ", so cursor ends up at end of statement
				if fpoint == point:
					self.show_bg = True
					view.run_command("auto_complete")

		for br in start_da_brackets:
			i = sublime.Region(br.a, self.getIndex(view_str, br.a))
			s = view.substr(i)
			if "type = " in s:
				fpoint = (view.substr(i).index("type = ") + 7) + i.a
				if fpoint == point:
					self.diplo_action = True
					view.run_command("auto_complete")

		for br in start_dp_brackets:
			i = sublime.Region(br.a, self.getIndex(view_str, br.a))
			s = view.substr(i)
			if "type = " in s:
				fpoint = (view.substr(i).index("type = ") + 7) + i.a
				if fpoint == point:
					self.diplo_play = True
					view.run_command("auto_complete")

	def on_selection_modified(self, view):

		if not view:
			return

		try:
			if view.syntax().name != "Victoria Script" and view.syntax().name != "PdxPython":
				return
		except AttributeError:
			return

		self.simple_scope_match(view)
		# Only do when there is 1 selections, doens't make sense with multiple selections
		if len(view.sel()) == 1:
			self.check_for_simple_completions(view, view.sel()[0].a)
			self.check_for_complex_completions(view, view.sel()[0].a)

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
					key = key.replace("\t", "")
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
					panel.add_regions("bad_encoding", [sublime.Region(27, 27 + len(old_encoding))], "underline.bad", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE))
					panel.add_regions("encoding", [sublime.Region(len(panel) - 30, len(panel) - 16)], "underline.good", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE))
					panel.set_read_only(True)

				if utf8_paths is not None and not old_encoding == "UTF-8":
					# is not utf-8 and should be
					self.view.set_encoding("UTF-8")
					error_message = f"EncodingError: Encoding is {old_encoding}, files in {utf8_paths.group()} should be UTF-8, resave to fix."

					panel = self.create_error_panel()
					panel.set_read_only(False)
					panel.run_command("append", {"characters": error_message})
					# bad encoding
					panel.add_regions("bad_encoding", [sublime.Region(27, 27 + len(old_encoding))], "underline.bad", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE))
					# new good encoding
					panel.add_regions("encoding", [sublime.Region(len(panel) - 21, len(panel) - 16)], "underline.good", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE))
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
		panel.add_regions("line_num", [sublime.Region(len(panel) - line_a, len(panel))], "region.redish", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE))
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
		panel.add_regions("line_num", [sublime.Region(len(panel) - line_a, len(panel))], "region.redish", flags=(sublime.DRAW_SOLID_UNDERLINE | sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE))
		panel.set_read_only(True)

	def create_error_panel(self):
		window = sublime.active_window()
		panel = window.create_output_panel("error", unlisted=True)
		panel.assign_syntax("scope:text.error")
		panel.settings().set("color_scheme", "ErrorPanel.hidden-color-scheme")
		panel.settings().set('gutter', False)
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

	return False  # file is all good

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
			paths = [basePath]

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
		""" % (css_basic_style, file)

		view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY |
										  sublime.COOPERATE_WITH_AUTO_COMPLETE | sublime.HIDE_ON_CHARACTER_EVENT),
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
		""" % (style, desc)

		view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY | sublime.COOPERATE_WITH_AUTO_COMPLETE | sublime.HIDE_ON_CHARACTER_EVENT),
						location=point, max_width=1024)
		return


class ScriptHoverListener(sublime_plugin.EventListener):

	def on_hover(self, view, point, hover_zone):

		if not view:
			return

		try:
			if view.syntax().name == "Victoria Script" or view.syntax().name == "PdxPython" or view.syntax().name == "Victoria Gui":
				pass
			else:
				return
		except AttributeError:
			return

		if view.syntax().name == "Victoria Gui":
			sublime.set_timeout_async(lambda: self.do_gui_hover_async(view, point), 0)

		if view.syntax().name == "Victoria Script" or view.syntax().name == "PdxPython":
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
		if view.syntax().name == "Victoria Script" or view.syntax().name == "Victoria Gui" or view.syntax().name == "PdxPython":
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
									for directory in [f.path for f in os.scandir(mod) if f.is_dir()]:
										mod_path = directory + "\\" + texture_raw_path
										if os.path.exists(mod_path):
											full_texture_path = mod_path
								else:
									mod_path = mod + "\\" + texture_raw_path
									if os.path.exists(mod_path):
										full_texture_path = mod_path
					full_texture_path = full_texture_path.replace("/", "\\")
					# The path exists and the point in the view is inside of the path
					if texture_raw_region.__contains__(point):
						texture_name = view.substr(view.word(texture_raw_end.a - 1))
						self.show_texture_hover_popup(view, point, texture_name, full_texture_path)

	def do_gui_hover_async(self, view, point):
		word = view.substr(view.word(point))

		if view.match_selector(point, "comment.line"):
			return

		if gui_templates.contains(word):
			self.show_gui_popup(view, point, word, gui_templates.access(word), "Gui Template")

		if gui_types.contains(word):
			self.show_gui_popup(view, point, word, gui_types.access(word), "Gui Type")

	def do_hover_async(self, view, point):
		word_region = view.word(point)
		word = view.substr(word_region)
		fname = view.file_name()
		current_line_num = view.rowcol(point)[0] + 1

		if view.match_selector(point, "comment.line"):
			return

		if view.match_selector(point, "entity.name.function.scope.declaration"):
			self.show_popup_default(view, point, word, PdxScriptObject(word, fname, current_line_num), "Scope Declaration")

		if view.match_selector(point, "entity.name.function.var.declaration"):
			self.show_popup_default(view, point, word, PdxScriptObject(word, fname, current_line_num), "Variable Declaration")

		if view.match_selector(point, "variable.parameter.scope.usage") or view.match_selector(point, "variable.parameter.remove.var") or view.match_selector(point, "variable.parameter.trigger.usage") or view.match_selector(point, "variable.parameter.variable.usage"):
			if view.match_selector(point, "variable.parameter.scope.usage"):
				self.show_popup_default(view, point, word, PdxScriptObject(word, fname, current_line_num), "Saved Scope")
			else:
				self.show_popup_default(view, point, word, PdxScriptObject(word, fname, current_line_num), "Saved Variable")

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

	def show_gui_popup(self, view, point, word, PdxObject, header):
		word_line_num = view.rowcol(point)[0] + 1
		word_file = view.file_name().rpartition("\\")[2]
		definition = ""

		if word_line_num != PdxObject.line:
			definition = f"<p><b>Definition of&nbsp;&nbsp;</b><tt class=\"variable\">{PdxObject.key}</tt></p>"
			goto_args = {"path": PdxObject.path, "line": PdxObject.line}
			goto_url = sublime.command_url("goto_script_object_definition", goto_args)
			definition += """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;"""%(goto_url, PdxObject.path.rpartition("\\")[2], PdxObject.line, PdxObject.path.rpartition("\\")[2], PdxObject.line)
			goto_right_args = {"path": PdxObject.path, "line": PdxObject.line}
			goto_right_url = sublime.command_url("goto_script_object_definition_right", goto_right_args)
			definition += """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""%(goto_right_url)

		references = []
		ref = ""
		for win in sublime.windows():
			for i in [v for v in win.views() if v and v.file_name()]:
				if i.file_name().endswith(".gui"):
					view_region = sublime.Region(0, i.size())
					view_str = i.substr(view_region)
					for j, line in enumerate(view_str.splitlines()):
						definition_found = False
						if PdxObject.key in line:
							filename = i.file_name().rpartition("\\")[2]
							line_num = j + 1
							if word_line_num == line_num and word_file == filename:
								# Don't do current word
								continue
							elif line_num == PdxObject.line and i.file_name() == PdxObject.path:
								# Don't do definition
								continue
							if not definition_found:
								references.append(f"{i.file_name()}|{line_num}")

		if references:
			ref = f"<p><b>References to&nbsp;&nbsp;</b><tt class=\"variable\">{PdxObject.key}</tt></p>"
			for j, i in enumerate(references):
				if j > 10:
					break
				fname = i.split("|")[0]
				shortname = fname.rpartition("\\")[2]
				line = i.split("|")[1]
				goto_args = { "path": fname, "line": line}
				goto_url = sublime.command_url("goto_script_object_definition", goto_args)
				ref += """<a href="%s" title="Open %s and goto line %s">%s:%s</a>&nbsp;"""%(goto_url, shortname, line, shortname, line)
				goto_right_args = {"path": fname, "line": line}
				goto_right_url = sublime.command_url("goto_script_object_definition_right", goto_right_args)
				ref += """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""%(goto_right_url)

		link = definition + ref
		if link:
			hoverBody = """
				<body id="vic-body">
					<style>%s</style>
					<h1>%s</h1>
					%s
				</body>
			""" %(css_basic_style, header, link)

			view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY |sublime.COOPERATE_WITH_AUTO_COMPLETE |sublime.HIDE_ON_CHARACTER_EVENT),
							location=point, max_width=1024)

	def show_popup_default(self, view, point, word, PdxObject, header):

		word_line_num = view.rowcol(point)[0] + 1
		word_file = view.file_name().rpartition("\\")[2]
		definition = ""
		definitions = []

		if header == "Saved Scope" or header == "Saved Variable":
			for win in sublime.windows():
				for i in [v for v in win.views() if v and v.file_name()]:
					if i.file_name().endswith(".txt") or i.file_name().endswith(".py"):
						variables = [x for x in i.find_by_selector("entity.name.function.var.declaration") if i.substr(x) == PdxObject.key]
						variables.extend([x for x in i.find_by_selector("entity.name.function.scope.declaration") if i.substr(x) == PdxObject.key])
						for r in variables:
							line = i.rowcol(r.a)[0] + 1
							path = i.file_name()
							if line == word_line_num and path == PdxObject.path:
								continue
							else:
								definitions.append(PdxScriptObject(PdxObject.key, path, line))

			if len(definitions) == 1:
				definition = f"<p><b>Definition of&nbsp;&nbsp;</b><tt class=\"variable\">{PdxObject.key}</tt></p>"
			elif len(definitions) > 1:
				definition = f"<p><b>Definitions of&nbsp;&nbsp;</b><tt class=\"variable\">{PdxObject.key}</tt></p>"
			for obj in definitions:
				goto_args = {"path": obj.path, "line": obj.line}
				goto_url = sublime.command_url("goto_script_object_definition", goto_args)
				definition += """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;"""%(goto_url, obj.path.rpartition("\\")[2], obj.line, obj.path.rpartition("\\")[2], obj.line)
				goto_right_args = {"path": obj.path, "line": obj.line}
				goto_right_url = sublime.command_url("goto_script_object_definition_right", goto_right_args)
				definition += """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""%(goto_right_url)
		else:
			if word_line_num != PdxObject.line and view.file_name() != PdxObject.path:
				definition = f"<p><b>Definition of&nbsp;&nbsp;</b><tt class=\"variable\">{PdxObject.key}</tt></p>"

				goto_args = {"path": PdxObject.path, "line": PdxObject.line}
				goto_url = sublime.command_url("goto_script_object_definition", goto_args)
				definition += """<a href="%s" title="Open %s and goto line %d">%s:%d</a>&nbsp;"""%(goto_url, PdxObject.path.rpartition("\\")[2], PdxObject.line, PdxObject.path.rpartition("\\")[2], PdxObject.line)
				goto_right_args = {"path": PdxObject.path, "line": PdxObject.line}
				goto_right_url = sublime.command_url("goto_script_object_definition_right", goto_right_args)
				definition += """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""%(goto_right_url)

		references = []
		ref = ""
		for win in sublime.windows():
			for i in [v for v in win.views() if v and v.file_name()]:
				if i.file_name().endswith(".txt") or i.file_name().endswith(".py"):
					view_region = sublime.Region(0, i.size())
					view_str = i.substr(view_region)
					for j, line in enumerate(view_str.splitlines()):
						definition_found = False
						if PdxObject.key in line:
							filename = i.file_name().rpartition("\\")[2]
							line_num = j+1
							if definitions:
								# Don't do definitions for scopes and variables
								for obj in definitions:
									if obj.line == line_num and obj.path == i.file_name():
										definition_found = True
							if word_line_num == line_num and word_file == filename:
								# Don't do current word
								continue
							elif line_num == PdxObject.line and i.file_name() == PdxObject.path:
								# Don't do definition
								continue
							if not definition_found:
								references.append(f"{i.file_name()}|{line_num}")
		if references:
			ref = f"<p><b>References to&nbsp;&nbsp;</b><tt class=\"variable\">{PdxObject.key}</tt></p>"
			for i in references:
				fname = i.split("|")[0]
				shortname = fname.rpartition("\\")[2]
				line = i.split("|")[1]
				goto_args = { "path": fname, "line": line}
				goto_url = sublime.command_url("goto_script_object_definition", goto_args)
				ref += """<a href="%s" title="Open %s and goto line %s">%s:%s</a>&nbsp;"""%(goto_url, shortname, line, shortname, line)
				goto_right_args = {"path": fname, "line": line}
				goto_right_url = sublime.command_url("goto_script_object_definition_right", goto_right_args)
				ref += """<a class="icon" href="%s"title="Open Tab to Right of Current Selection">◨</a>&nbsp;<br>"""%(goto_right_url)

		link = definition + ref
		if link:
			hoverBody = """
				<body id="vic-body">
					<style>%s</style>
					<h1>%s</h1>
					%s
				</body>
			""" %(css_basic_style, header, link)

			view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY |sublime.COOPERATE_WITH_AUTO_COMPLETE |sublime.HIDE_ON_CHARACTER_EVENT),
							location=point, max_width=1024)

	def show_texture_hover_popup(self, view, point, texture_name, full_texture_path):
		args = { "path": full_texture_path }
		open_texture_url = sublime.command_url("open_victoria_texture ", args)
		folder_args = { "path": full_texture_path, "folder": True}
		open_folder_url = sublime.command_url("open_victoria_texture ", folder_args)
		in_sublime_args = { "path": full_texture_path, "mode": "in_sublime"}
		open_in_sublime_url = sublime.command_url("open_victoria_texture ", in_sublime_args)
		hoverBody = """
			<body id=\"vic-body\">
				<style>%s</style>
				<h1>Open Texture</h1>
				<div></div>
				<a href="%s" title="Open folder containing the texture.">Open Folder</a>
				<br>
				<a href="%s" title="Open %s.dds in the default program">Open in default program</a>
				<br>
				<a href="%s" title="Convert %s.dds to PNG and open in sublime">Open in sublime</a>
			</body>
		""" %(css_basic_style, open_folder_url, open_texture_url, texture_name, open_in_sublime_url, texture_name)

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
		""" % (css_basic_style, browse_url)

		view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY |
										  sublime.COOPERATE_WITH_AUTO_COMPLETE | sublime.HIDE_ON_CHARACTER_EVENT),
						location=point, max_width=802)

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
		""" % (css_basic_style, word, browse_and_play_url)

		view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY | sublime.COOPERATE_WITH_AUTO_COMPLETE | sublime.HIDE_ON_CHARACTER_EVENT), location=point, max_width=802)


# Global so I don't have to deal with passing through the hrefs, should probably just pass them as args.
video_file_path = False
video_point = None
edit_obj = None  # Used to pass edit object to on_done
show_sound_menu = False
sound_region = False


class GotoScriptObjectDefinitionCommand(sublime_plugin.WindowCommand):
	def run(self, path, line):
		if os.path.exists(path):
			file_path = "{}:{}:{}".format(path, line, 0)
			self.open_location(self.window, file_path)

	def open_location(self, window, l):
		flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP
		view = window.open_file(l, flags)


class GotoScriptObjectDefinitionRightCommand(sublime_plugin.WindowCommand):
	def run(self, path, line):
		if os.path.exists(path):
			file_path = "{}:{}:{}".format(path, line, 0)
			self.open_location(self.window, file_path, side_by_side=True, clear_to_right=True)

	def open_location(self, window, l, side_by_side=False, replace=False, clear_to_right=False):
		flags = sublime.ENCODED_POSITION | sublime.FORCE_GROUP

		if side_by_side:
			flags |= sublime.ADD_TO_SELECTION | sublime.SEMI_TRANSIENT
			if clear_to_right:
				flags |= sublime.CLEAR_TO_RIGHT

		elif replace:
			flags |= sublime.REPLACE_MRU | sublime.SEMI_TRANSIENT
		view = window.open_file(l, flags)


class OpenVictoriaTextureCommand(sublime_plugin.WindowCommand):
	def run(self, path, folder=False, mode="default_program"):
		if folder:
			end = path.rfind("\\")
			path = path[0:end:]
			os.startfile(path)
		else:
			if mode == "default_program":
				os.startfile(path)
			elif mode == "in_sublime":
				simple_path = path.rpartition("\\")[2].replace(".dds", ".png")
				output_file = sublime.packages_path() + "\\Victoria3Tools\\Convert DDS\\cache\\" + simple_path
				exe_path = sublime.packages_path() + "\\Victoria3Tools\\Convert DDS\\src\\ConvertDDS.exe"

				if not os.path.exists(output_file):
					# Run dds to png converter
					subprocess.call([exe_path, path, output_file])
					sublime.active_window().open_file(output_file)
				else:
					# File is already in cache, don't need to convert
					sublime.active_window().open_file(output_file)


class V3ClearImageCacheCommand(sublime_plugin.WindowCommand):
	def run(self):
		dir_name = sublime.packages_path() + "\\Victoria3Tools\\Convert DDS\\cache\\"
		ld = os.listdir(dir_name)
		for item in ld:
			if item.endswith(".png"):
				os.remove(os.path.join(dir_name, item))
		sublime.status_message("Cleared Image Cache")


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
		if show_sound_menu:
			return True
		else:
			return False


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
		for x in GameData.EventVideos:
			keys.append(x.replace("gfx/event_pictures/", ""))
		return keys


class SoundInputHandler(sublime_plugin.ListInputHandler):

	def name(self):
		return 'sound'

	def list_items(self):
		keys = []
		for x in GameData.EventSoundsList:
			keys.append(x.replace("event:/SFX/Events/", ""))
		return sorted(keys)
