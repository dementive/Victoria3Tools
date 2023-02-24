import os, re
exclusion_keys = {
    "#",
    "@",
    "modifier",
    "character_modifier",
    "if",
    "else",
    "elseif",
    "else_if",
    "\n",
    "can_have",
    "can_keep",
    "can_pass",
    "on_pass",
    "on_revoke",
    "should_start_with",
    "graphical_cultures",
    "pass_cost",
    "desc",
    "compatibility",
    "name",
    "opposites",
    "triggered_opinion",
    "icon",
    "random_list",
    "limit",
    "random"
}

svalue_exclusion_keys = {
	"value",
	"multiply",
	"min",
	"max",
	"add",
	"divide"
}

def get_event_sound(file_path):
	# break into lines, then check every line for "event:/SFX/Events" and append to set if it does.
	event_sounds = set()
	with open(file_path, "r") as fh:
		try:
			string = fh.read()
		except UnicodeDecodeError:
			return
	for line in string.splitlines():
		x = re.search("event:/SFX/Events.*\"", line)
		if x:
			event_sounds.add(x.group().replace("\"", ""))
	return event_sounds

def should_read(x,level=0):
    y = x.split("#")[0]
    z = y.split("=")[0]
    return ("= {" in y and z.count("\t")+z.count("    ") == level and not z.strip() in exclusion_keys)

def get_scripted_effects(file_path, should_read):
	scripted_effects = set()
	with open(file_path,"r",encoding='utf-8-sig') as objfile:
	    for line in (y for y in objfile.readlines() if should_read(y)):
	        scripted_effects.add(line.split("=").pop(0).replace(" ", "").replace("\t", ""))
	return scripted_effects	   


def get_scripted_triggers(file_path, should_read):
	scripted_triggers = set()
	with open(file_path,"r",encoding='utf-8-sig') as objfile:
	    for line in (y for y in objfile.readlines() if should_read(y)):
	        scripted_triggers.add(line.split("=").pop(0).replace(" ", "").replace("\t", ""))
	return scripted_triggers

def get_script_values(file_path, should_read):
	script_values = set()
	with open(file_path,"r",encoding='utf-8-sig') as objfile:
	    for line in (y for y in objfile.readlines() if should_read(y)):
	        script_values.add(line.split("=").pop(0).replace(" ", "").replace("\t", ""))
	return script_values

def get_simple_values(file_path):
	simple_script_values = dict()
	with open(file_path, "r") as fh:
		try:
			string = fh.read()
		except UnicodeDecodeError:
			return
	for line in string.splitlines():
		x = re.search("([A-Za-z_][A-Za-z_0-9]*)\s?=\s?(-?[0-9]+\.?[0-9]*)", line)
		if x and x[1] not in svalue_exclusion_keys:
			simple_script_values[x[1]] = x[2]
	return simple_script_values

# def get_event_scripted_effects(file_path):
# 	# Get all scripted_effects declared in an event file.
# 	# EX:
# 	# scripted_effect conflict_building = {
# 	# 	always = yes
# 	# }
# 	scripted_effects = set()
# 	with open(file_path, "r") as fh:
# 		try:
# 			string = fh.read()
# 		except UnicodeDecodeError:
# 			return
# 	for line in string.splitlines():
# 		x = re.search("(scripted_effect)\s+([A-Za-z_][A-Za-z_0-9]*)", line)
# 		if x:
# 			scripted_effects.add(x[2])
# 	return simple_script_values

def get_game_data():
	lamb = lambda x: should_read(x)
	event_sounds = set()
	scripted_effects = set()
	scripted_triggers = set()
	script_values = set()
	simple_script_values = dict()
	EventVideos = list()
	for dirpath, dirnames, filenames in os.walk("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Victoria 3\\game"):
		for filename in [f for f in filenames if f.endswith(".txt")]:
			file_path = os.path.join(dirpath, filename)
			if "events" in file_path:
				res = get_event_sound(file_path)
				if res: event_sounds.update(res)
			if "scripted_effects" in file_path:
				scripted_effects.update(get_scripted_effects(file_path, lamb))
			if "scripted_triggers" in file_path:
				scripted_triggers.update(get_scripted_triggers(file_path, lamb))
			if "script_values" in file_path:
				script_values.update(get_script_values(file_path, lamb))
				simple_script_values.update(get_simple_values(file_path))
		

	for file in os.scandir("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Victoria 3\\game" + "\\gfx\\event_pictures"):
		if file.name.endswith(".bk2"):
			path = file.path
			path = path.split("game\\")[1].replace("\\", "/")
			EventVideos.append(path)

	event_sounds = tuple(event_sounds)
	event_sounds = sorted(event_sounds)

	print("EventSoundsList = [")
	for i, j in enumerate(sorted(event_sounds)):
		if i == len(event_sounds) - 1:
			# No comma at the end
			print(f"\t\"{j}\"")
		else:
			print(f"\t\"{j}\",")
	print("]")

	print("ScriptedEffectsList = [")
	for i, j in enumerate(sorted(scripted_effects)):
		if i == len(scripted_effects) - 1:
			print(f"\t\"{j}\"")
		else:
			print(f"\t\"{j}\",")
	print("]")

	print("ScriptedTriggersList = [")
	for i, j in enumerate(sorted(scripted_triggers)):
		if i == len(scripted_triggers) - 1:
			print(f"\t\"{j}\"")
		else:
			print(f"\t\"{j}\",")
	print("]")


	print("SimpleScriptValuesDict = {")
	count = 0
	for (i, j) in zip(simple_script_values.keys(), simple_script_values.values()):
		count += 1
		if count == len(simple_script_values.keys()):
			print(f"\t\"{i}\": {j}")
		else:
			print(f"\t\"{i}\": {j},")
	print("}")

	print("ScriptValuesList = [")
	for i, j in enumerate(sorted(script_values)):
		if i == len(script_values) - 1:
			print(f"\t\"{j}\"")
		else:
			print(f"\t\"{j}\",")
	print("]")
	print("EventVideos = [")
	for i, j in enumerate(sorted(EventVideos)):
		if i == len(EventVideos) - 1:
			print(f"\t\"{j}\"")
		else:
			print(f"\t\"{j}\",")
	print("]")

#get_game_data()

class ModData:
	""" Class to hold all mod data from the base game """
	def __init__(self, modpath):
		self.scripted_triggers = set()
		self.scripted_effects = set()
		self.script_values = set()
		self.simple_script_values = dict()
		self.get_mod_data(modpath)

	def get_mod_data(self, modpath):
		lamb = lambda x: should_read(x)
		for dirpath, dirnames, filenames in os.walk(modpath):
			for filename in [f for f in filenames if f.endswith(".txt")]:
				file_path = os.path.join(dirpath, filename)
				if "scripted_effects" in file_path:
					self.scripted_effects.update(get_scripted_effects(file_path, lamb))
				if "scripted_triggers" in file_path:
					self.scripted_triggers.update(get_scripted_triggers(file_path, lamb))
				if "script_values" in file_path:
					self.script_values.update(get_script_values(file_path, lamb))
					self.simple_script_values.update(get_simple_values(file_path))
