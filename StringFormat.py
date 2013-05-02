#Regex library for string parsing
import re

#Dictionary to identify unicode characters
from htmlentitydefs import name2codepoint

class StringFormat:
	#Removes excess newline characters
	def formatLines(self, text):
	    return re.sub('\n\n\n(\n*)', '\n\n', text)

	#Handles character decoding for ampersand codes
	#Can be found at wiki.python.org
	def unescape(self, text):
	    return re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), text)