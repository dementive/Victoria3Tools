import os
from json import dumps

"""
	All of this code is not game specific, any Jomini based paradox game can use this to parse game files and create GameObjects.
	Conflicts between the base game with mods and conflicts between mods and other mods are automatically resolved when GameObjects are created

	A GameObject is something in the game folder that is associated with...the game
	for example: buildings, cultures, trade goods, traits, states, regions, etc...

	Example GameObject implementation:
	# file_paths is a list of directories to mods and the base game with the base game as the last element
	file_paths = ["full_mod_path_1", "full_mod_path_2", "base_game_path"]
	class V3Building(GameObjectBase):
		def __init__(self):
			super().__init__(file_paths, level=1, ignored_files=["test.txt"])
			self.get_data("common\\building")

	buildings = V3Building(file_paths)
	buildings.print()

	Note that creating game objects is IO bound so using threading to create several objects will greatly increase the speed

	GameObjects (V3Building for example) are basically PdxScriptObjectTypes, and PdxScriptObjectTypes are basically a list of PdxScriptObjects
	PdxScriptObjects are everything that needs to be known about a game object

	Several init options are available when making a new GameObject:
		1. level - integer that determines the level files should be parsed at, level=0 is no tabs in, level=1 is 1 tab in, etc...
		2. ignored_files - list of filenames that should not be parsed
		3. included_files - list of filenames that should be parsed, if this is defined only files in this list will be parsed

	When inheriting from GameObjectBase the following methods are available:
		• length() - Return the length of the list of PdxScriptObjects -> int
		• print() - Print a breakdown of all the PdxScriptObjects, showing the key, path and line number -> None
		• contains(key) - Check if a PdxScriptObjectType contains a specific string or PdxScriptObject -> bool
		• keys() - Return a list of keys of all the PdxScriptObjects -> list[str]
		• access(key) - Return a PdxScriptObject given a string or a PdxScriptObject, returns False if not found -> PdxScriptObject
		• sort() - Sort the list of PdxScriptObjects by their key -> None
		• remove() - Remove a PdxScriptObject or string -> None
		• clear() - Remove all PdxScriptObjects from the list  -> None
		• add() - Add a new PdxScriptObject to the object -> None
		• to_dict() - Return a dictionary of PdxScriptObjects -> dict
		• to_json() - Return a json formatted string of PdxScriptObjects -> str

	To implement custom parsing for a GameObject:
		1. override the get_pdx_object_list() function
		2. Fill self.main with data in another way, all that should have to be changed is the should_read(line) part
		3. If more information than key, path, and line number are needed:
		4. implement a new PdxScriptObject class that has more attributes but keeps the same methods as PdxScriptObject
		5. Make sure self.main is filled with the new attributes when parsing
		6. Change PdxScriptObject() to your new class name in get_pdx_object_list()
"""


class PdxScriptObject:
	"""
		Class to hold everything that needs to be known about a GameObject
		3 things are saved for default objects
		1. The objects key
		2. The path to the file the key is found in
		3. The line number the key is found at
	"""

	def __init__(self, key, path, line):
		self.key = key
		self.path = path
		self.line = line

	# Override operators so they compare using self.key only
	# Can be used to compare PdxScriptObjects or to compare self.key to another string
	def __eq__(self, other):
		if isinstance(other, PdxScriptObject):
			return (self.key == other.key)
		elif isinstance(other, str):
			return (self.key == other)
		else:
			return False

	def __lt__(self, other):
		if isinstance(other, PdxScriptObject):
			return (self.key < other.key)
		elif isinstance(other, str):
			return (self.key < other)
		else:
			return False

	def __gt__(self, other):
		if isinstance(other, PdxScriptObject):
			return (self.key > other.key)
		elif isinstance(other, str):
			return (self.key > other)
		else:
			return False


class PdxScriptObjectType:
	"""
		Class to hold a list of PdxScriptObject types (or similar types)
	"""

	def __init__(self, obj_list):
		self.objects = obj_list

	def __iadd__(self, other):
		"""
			Override += operator so 2 PdxScriptObjectTypes can be added together
			If a key is already defined the key get overriden by the new key
		"""
		for j in other.objects:
			if j in self.objects:
				# Replace the object in self.objects with the object in other.objects
				self.objects[self.objects.index(j)].path = j.path
				self.objects[self.objects.index(j)].line = j.line
			else:
				# Append a new object if there are no conflicts
				self.objects.append(j)
		return self


class GameObjectBase:
	"""
		Base Class that all GameObject classes should inherit
		paths is a list of paths mod directories, load order of mods will depend on their order in the paths list
		vanilla_path is the path to the vanilla game folder.
	"""

	def __init__(self, paths=[], vanilla_path="", level=0, ignored_files=[], included_files=[]):
		self.paths = paths
		self.vanilla_path = vanilla_path
		self.main = PdxScriptObjectType([PdxScriptObject(" ", "", 0)])
		self.level = level  # How many tabs in should the file be parsed?
		self.ignored_files = ignored_files
		self.included_files = included_files
		self.start = 0
		self.end = 0
		# Keys that should not be added to objects when parsing
		self.exclusion_keys = {
			"#", "@", "modifier", "character_modifier", "if", "else", "elseif", "else_if", "\n", "can_have",
			"can_keep", "can_pass", "on_pass", "on_revoke", "should_start_with", "graphical_cultures", "pass_cost",
			"desc", "compatibility", "name", "opposites", "triggered_opinion", "icon", "random_list", "limit", "random",
			"potential", "abort", "chance", "on_potential", "on_start", "on_abort", "on_completion", "requires", "highlight",
			"allow", "bypass", "ai_chance", "trigger", "family", "male_names", "female_names", "stability", "raise_legion",
			"alternative_limit", "hidden_effect", "OR", "or", "prevented_by", "trigger_event", "current_ruler", "value", "bg", "custom_tooltip"
		}

	# Utility Functions shared between all GameObjects

	def print(self) -> None:
		""" Print a breakdown of all the PdxScriptObjects in the PdxScriptObjectType """
		for i in self.main.objects:
			print(f"Key: {i.key} -- File: {i.path} -- Line: {i.line}")

	def add(self, obj) -> None:
		"""
			Add a new PdxScriptObject to the object list
			Make a new PdxScriptObjectType so potential conflicts with the new object are resolved when inserted
		"""
		self.main += PdxScriptObjectType([obj])

	def remove(self, key) -> None:
		""" Remove the specified PdxScriptObject or string"""
		if key in self.main.objects:
			self.main.objects.remove(key)

	def clear(self) -> None:
		""" Clear all objects from the list """
		for key in self.keys():
			self.main.objects.remove(key)

	def sort(self) -> None:
		"""
			Sort PdxScriptObjects by key
		"""
		self.main.objects = sorted(self.main.objects)

	def length(self) -> int:
		""" Return the length of the object list """
		return len(self.main.objects)

	def contains(self, key) -> bool:
		""" Check if the PdxScriptObjectType contains a specified PdxScriptObject or a string"""
		return True if key in self.main.objects else False

	def keys(self) -> list:
		""" Return a list of the keys in the object"""
		keys = []
		for i in self.main.objects:
			keys.append(i.key)
		return keys

	def access(self, key):
		"""
			Return the PdxScriptObject (or similar type) with the specified key
			return false if the key is not found
		"""
		if self.contains(key):
			return self.main.objects[self.main.objects.index(key)]
		else:
			return False

	def to_dict(self) -> dict:
		"""
			Return a dictionary with the keys being the keys of the PdxScriptObject and the value being a list of the file and line
		"""
		d = dict()
		for i in self.main.objects:
			d[i.key] = [i.path, i.line]
		return d

	def to_json(self) -> str:
		"""
			Return a json formatted string of PdxScriptObjects
		"""
		return dumps(self.to_dict())

	# Iterator methods so objects can be used in for loops
	def __iter__(self):
		return self

	def __next__(self):
		if self.start > self.end:
			# Reset and stop iteration so it can be looped over again like a normal list
			self.start = 0
			self.end = self.length() - 1
			raise StopIteration
		current = self.main.objects[self.start]
		self.start += 1
		return current

	# Class Functions needed to initialize data, don't need to be use anything below this after initilization of class
	def get_data(self, objpath: str) -> None:
		# Fill collections with vanilla data

		# Split the objpath using the Windows path separator
		objpath_parts = objpath.split('\\')
		# Create a platform-independent path using os.path.join()
		objpath = os.path.join(*objpath_parts)
		
		for dirpath, dirnames, filenames in os.walk(self.vanilla_path):
			if objpath in dirpath:
				self.main += self.get_pdx_object_list(dirpath)
		self.remove(" ")
		# Fill collections with mod data
		for path in self.paths:
			for dirpath, dirnames, filenames in os.walk(path):
				if objpath in dirpath:
					self.main += self.get_pdx_object_list(dirpath)

		# Remove vanilla objects when mod file overrides vanilla file but the mod file doens't include that object

		#
		# TODO this does not work and I can't figure out how to make it work right now but it's pretty important so need to figure it out
		#

		vanilla_files = set()
		mod_files = set()

		for i in self.main.objects:
			if self.vanilla_path in i.path:
				vanilla_files.add(i.path.rpartition("\\")[2])
			else:
				mod_files.add(i.path.rpartition("\\")[2])

		conflicting_files = (x for x in vanilla_files if x in mod_files)
		if sum(1 for _ in conflicting_files) > 0:
			to_remove = (x for x in self.main.objects if x.key == "" or (self.vanilla_path in i.path and i.path.rpartition("\\")[2] in conflicting_files))
			for i in to_remove:
				self.main.objects.remove(i)

		# Set Iterator position
		self.end = self.length() - 1

	# Override this function for custom parsing of GameObjects
	def get_pdx_object_list(self, path: str) -> PdxScriptObjectType:
		"""
			Return a PdxScriptObjectType
			path = path to directory with GameObjects in it
		"""
		obj_list = list()
		for dirpath, dirnames, filenames in os.walk(path):
			for filename in [f for f in filenames if f.endswith(".txt")]:
				if filename in self.ignored_files:
					continue
				if self.included_files and filename not in self.included_files:
					continue
				file_path = os.path.join(dirpath, filename)
				with open(file_path, "r", encoding='utf-8-sig') as file:
					for i, line in enumerate(file):
						if self.should_read(line):
							found_item = line.split("=").pop(0).replace(" ", "").replace("\t", "")
							if found_item:
								obj_list.append(PdxScriptObject(found_item, file_path, i + 1))
		return PdxScriptObjectType(obj_list)

	def should_read(self, x: str) -> bool:
		# Check if a line should be read
		y = x.split("#")[0]
		z = y.split("=")[0]
		# The long set is exclusion keys to not read when looking for top level keys
		if "= {" in y and z.count("\t") + z.count("    ") == self.level and not z.strip() in self.exclusion_keys:
			return True
		w = y.find("=")
		if w != -1 and self.level == 0:
			w = y[0:w].rstrip()
			if "\t" not in w and " " not in w:
				return True

		return False


def dict_to_game_object(objects: dict) -> GameObjectBase:
	"""
		Create a GameObject from a dictionary that was created from a GameObjects to_dict or to_json method
		Making game objects like this can be considerably faster 
		because it allows you to skip all the file IO and just load from a cache of stored game objects
	"""
	obj_list = list()
	for i in objects:
		obj_list.append(PdxScriptObject(i, objects[i][0], objects[i][1]))
	game_object = GameObjectBase()
	game_object.main = PdxScriptObjectType(obj_list)
	return game_object
