import os
import sys
import subprocess
import shutil

# Assuming sublime is imported correctly elsewhere in your code
import sublime

# Clear modules cache if package is reloaded
prefix = __package__ + ".src"  # Don't clear the base package
for module_name in [
    module_name for module_name in sys.modules if module_name.startswith(prefix)
]:
    del sys.modules[module_name]
del prefix


def jomini_repo_exists(destination_dir):
    return os.path.exists(os.path.join(destination_dir, "JominiTools"))


def clone_jomini_repo(destination_dir):
    temp_dir = os.path.join(destination_dir, "a.tmp")
    subprocess.run(
        [
            "git",
            "clone",
            "--no-checkout",
            "--no-hardlinks",
            "https://github.com/dementive/JominiTools",
            temp_dir,
        ],
        check=True,
    )
    subprocess.run(["mv", os.path.join(temp_dir, ".git"), destination_dir], check=True)

    shutil.rmtree(temp_dir)
    subprocess.run(["git", "-C", destination_dir, "unstage", "all"], check=True)


if not jomini_repo_exists(sublime.packages_path()):
    jomini_repo_path = os.path.join(sublime.packages_path(), "JominiTools")
    if not os.path.exists(jomini_repo_path):
        os.makedirs(jomini_repo_path)
    clone_jomini_repo(jomini_repo_path)
else:
    from JominiTools.src.plugin_manager import PluginManager

    jomini_repository_url = "https://github.com/dementive/JominiTools"
    plugin_repository_url = "https://github.com/dementive/Victoria3Tools"

    jomini_repository_path = os.path.join(sublime.packages_path(), "JominiTools")
    plugin_repository_path = os.path.join(sublime.packages_path(), "Victoria3Tools")

    jomini_tools_manager = PluginManager(jomini_repository_path, jomini_repository_url)
    victoria_tools_manager = PluginManager(
        plugin_repository_path, plugin_repository_url
    )

    sublime.set_timeout_async(lambda: jomini_tools_manager.auto_update_plugin(), 0)
    sublime.set_timeout_async(lambda: victoria_tools_manager.auto_update_plugin(), 0)

from .src import *
