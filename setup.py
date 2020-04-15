import sys
try:
	from setuptools import setup, find_packages
except:
	print("please install setuptools using pip:")
	print("    <pip> install setuptools")
	sys.exit(-1)

with open("README.md", "r") as f:
	long_description = f.read()

setup(
	name = "vcgencmd",
	version = "0.1.0",
	description = "Python binding for RaspberryPi vcgencmd command-line tool",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Sushant Nadkar",
	license = "The MIT License (MIT)",
	url = "https://github.com/sushantnadkar/vcgencmd.git",
	packages = find_packages(),
	scripts = [],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	],
)
