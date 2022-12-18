import sublime
import sublime_plugin

import os
import re

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

			self.settingsBasePaths = sublime.load_settings("Victoria Syntax.sublime-settings").get("OpenHeaderBasePaths", [])
			settingsIncludePaths = sublime.load_settings("Victoria Syntax.sublime-settings").get("OpenHeaderIncludePaths", [])
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
		if sublime.load_settings("Victoria Syntax.sublime-settings").get("OpenHeaderEnabled") == False:
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

		style = """
					body {
						font-family: system;
						margin: 0;
						padding: 0.35rem;
						background-color: rgb(25, 25, 25);
					}
					p {
						font-size: 1.0rem;
						margin: 5;
					}
					h1 {
						font-size: 1.2rem;
						margin: 0;
					}
					a {
						margin: 5;
						font-size: 1.0rem;
					}
				"""
		hoverBody = """
			<body id="vic-body">
				<style>%s</style>
				<h1>Header File</h1>
				<a href="subl:open_pdx_shader_header" title="If file does not open add path to package settings">Open %s</a>
			</body>
		""" %(style, file)

		view.show_popup(hoverBody, flags=(sublime.HIDE_ON_MOUSE_MOVE_AWAY 
		                |sublime.COOPERATE_WITH_AUTO_COMPLETE |sublime.HIDE_ON_CHARACTER_EVENT),
						location=point, max_width=502)

