from .vcgencmd import Vcgencmd
from pprint import pprint

vgc = Vcgencmd()
out = vgc.get_throttled()
pprint(out)


