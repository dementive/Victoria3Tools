from .IfDefUtils import IfDefMatchListener
from .IntrinsicHover import IntrinsicHoverListener
from .OpenIncludedFile import HeaderHoverListener, OpenPdxShaderHeaderCommand
from .DocsHover import ScriptHoverListener
from .ScopeFinder import SimpleScopeMatchListener
from .LocalizeFile import LocalizeCurrentFileCommand
import os, imp

def reload_package(package):
	assert(hasattr(package, "__package__"))
	fn = package.__file__
	fn_dir = os.path.dirname(fn) + os.sep
	module_visit = {fn}
	del fn
	imp.reload(package)

def plugin_loaded():
	reload_package(IfDefUtils)
	reload_package(IntrinsicHover)
	reload_package(OpenIncludedFile)
	reload_package(DocsHover)
	reload_package(ScopeFinder)
	reload_package(LocalizeFile)

def plugin_unloaded():
	reload_package(IfDefUtils)
	reload_package(IntrinsicHover)
	reload_package(OpenIncludedFile)
	reload_package(DocsHover)
	reload_package(ScopeFinder)
	reload_package(LocalizeFile)
