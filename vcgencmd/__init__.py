from .vcgencmd import *

try:
	subprocess.check_output("vcgencmd")
except Exception:
	raise ImportError("\"vcgencmd\" command not found")
