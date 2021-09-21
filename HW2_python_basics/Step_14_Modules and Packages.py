"""
In this exercise, you will need to print an alphabetically sorted list of all functions in the re module, which contain the word find.
"""

import re

find_members = [i for i in dir(re) if "find" in i]
print(sorted(find_members))
