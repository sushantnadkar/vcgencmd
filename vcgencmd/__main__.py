from .vcgencmd import Vcgencmd
import sys


def main():
	out = Vcgencmd().version()
	print(out)

if __name__ == "__main__":
	sys.exit(main())
