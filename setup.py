import sys
try:
	from setuptools import setup
except:
	print("please install setuptools using pip:")
	print("    <pip> install setuptools")
	sys.exit(-1)

with open("README.md", "r") as f:
	long_description = f.read()

setup(
	name = "Vcgencmd",
	version = "0.1",
	description = "Native Python binding for RaspberryPi vcgencmd command-line tool",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Sushant Nadkar",
	license = "The MIT License (MIT)",
	url = "https://github.com/sushantnadkar/vcgencmd.git",
	packages = setuptools.find_packages(),
	scripts = [],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: The MIT License (MIT)",
	],
)
