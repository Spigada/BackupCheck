''' Python 3
	cheat sheet '''

	# humansize.py
	SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
				1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}

	def aprx_size(size, a_kb_is_1024_bytes=True):	# define function with 2
													# arguments, 2nd has default
		'''Convert a filesize to human-readable form 	(docstring)
		
		Keyword arguments:
		size -- file size in bytes
		a_kb_is_1024_bytes -- if True (default), use multiples of 1024
							  if False, use multiples of 1000
		Returns: string'''		# all functions return a value, even if it is None (null)
		
		if size < 0:
			raise ValueError('number must be non-negative')	# throw an exception
			
		multiple = 1024 if a_kb_is_1024_bytes else 1000		# x = (var ? 1024 : 1000);
		for suffix in SUFFIXES[multiple]:					# foreach (s in SUFF)
			size /= multiple
			if size < multiple:								# note: no ( )
				return '{0:.1f} {1}'.format(size, suffix)	# string formatting
		raise ValueError('number too large')

	if __name__ == '__main__':					# main entry point if called as function
		print(aprx_size(1000000000000, False))
		print(aprx_size(1000000000000))
		print(aprx_size(a_kb_is_1024_bytes=False, size=4000))	# named args
		print(aprx_size(size=4000, False))		# SyntaxError: non-keyword arg after keyword arg
			
	''' multiline comments also act like qq/.../ in Perl5 '''

	>>> import sys			# make all functions/attributes of sys module available
	>>> sys.path			# list of directories to search, in order
	>>> sys
	>>> sys.path.insert(0, '/path/to/code')	# insert path at front, lasts until python stops running
	>>> import humansize
	>>> print(humansize.aprx_size(4096, True))		# 4.0 KiB
	>>> print(humansize.aprx_size.__doc__)			# prints the docstring

	''' Everything in Python is an object, in that it can be assigned to a variable
	or passed to a function. Can have attributes and/or methods. EVERYTHING in
	Python is an object... string, list, function, module, class, instance '''

	try:
		import chardet as cd
	except ImportError:
		chardet = None

	if chardet:
		# chardet.something
	else:
		# continue without chardet

''' DATATYPES - not declared, determined by initial assignment.
	- Boolean	(True or False)
	- Numbers	(integers, floats, fractions, complex numbers)
	- Strings	(sequence of Unicode characters)
	- Bytes, Byte Arrays (ie. jpg file)
	- Lists		(ordered sequences of values)
	- Tuples	(ordered, immutable seqs of values)
	- Sets		(unordered bags of values)
	- Dictionaries (unordered bags of key-value pairs)
	- module, function, class, method, file, compiled code... '''

	>>> type(1)					# <class 'int'>
	>>> isinstance(1, int)		# True
	>>> 1 + 1					# 2
	>>> 1 + 1.0					# 2.0
	>>> int(-2.5)				# -2    negative numbers truncated towards 0
	>>> 11 / 2		>>> 11 // 2		# 5.5		# 5		float div, int div
	>>> 11.0 // 2	>>> -11 // 2	# 5.0		# -6	
	>>> 11 ** 2		>>> 11 % 2		# 121		# 1 

	>>> import fractions		>>> x = fractions.Fraction(2, 6)
	>>> x			# Fraction(1, 3)
	>>> x * 4		# Fraction(4, 3)
	>>> import math
	>>> math.pi		# 3.1415926535897931
	>>> math.sin(math.pi / 2)		# 1.0
	>>> math.tan(math.pi / 4)		# 0.99999999999999989	not exactly precise
	# for numeric matrix/multi-dimensional arrays, check out NumPy at www.numpy.org

	def is_it_true(anything):
		if anything:
			print("True")
		else:
			print("False")

	>>> is_it_true(1)		>>> is_it_true(-1)	# True		# True
	>>> is_it_true(0)							# False
	>>> is_it_true(0.1)		>>> is_it_true(0.0)	# True		# False (be careful)
	>>> is_it_true(fractions.Fraction(1, 2))	# True
	>>> is_it_true(fractions.Fraction(0, 1))	# False
	>>> is_it_true([])	>>> is_it_true([False])	# F, T. Lists are true unless empty
	>>> is_it_true(None)	>>> is_it_true(not None)	# False		# True
	>>> pass	# empty statement, {}, nop

''' [ LISTS ] - ordered sets of items '''

	>>> a_list = ['a', 'b', 'grim', 'z', 'example']
	>>> a_list[0]		>>> a_list[4]		# 'a'			# 'exam'
	>>> a_list[-1]		>>> a_list[-3]		# 'exam'		# 'grim'
	''' slicing a list -- list from first index up to but not including second '''
	>>> a_list[1:3]		>>> a_list[1:-1]	# ['b', 'grim']	# ['b', 'grim', 'z']
	>>> a_list[0:3]		>>> a_list[:3]		# ['a', 'b', 'grim']
	>>> a_list[3:]		>>> a_list[:]		# ['z', 'exam']	# *copy* of whole list
	''' adding to list '''
	>>> a_list = ['a']	>>> a_list = a_list + [2.0, 3]		# ['a', 2.0, 3]
	>>> a_list.append(True)					# ['a', 2.0, 3, True]
	>>> a_list.extend(['four', '&'])		# ['a', 2.0, 3, True, 'four', '&']
	>>> a_list.insert(0, '&')				# ['&', 'a', 2.0, 3, True, 'four', '&']
	>>> a_list = ['a', 'b', 'c']		>>> a_list.extend(['d', 'e', 'f'])
	>>> a_list.append(['g', 'h', 'i'])		# ['a','b','c','d','e','f',['g','h','i']]
	''' searching a list '''
	>>> a_list = ['a', 'b', 'new', 'grim', 'new']
	>>> a_list.count('new')					# 2
	>>> 'new' in a_list		>>> 'c' in a_list	# True		# False
	>>> a_list.index('new')	>>> a_list.index('c')	# 2		# *exception*
	''' removing from list '''
	>>> del a_list[1]		>>> a_list.remove('new')	# ['a', 'grim', 'new']
	>>> a_list.remove('new')>>> a_list.remove('new')	# ['a', 'grim']	# *exception*
	>>> a_list.pop()		>>> a_list.pop(0)		# Perl pop() and shift()

''' ( TUPLES ) - immutable list, faster than lists, can be used as dict keys '''

	>>> a_tuple = ('a', 'b', 'grim', 'z', 'example')
	>>> 'z' in a_tuple		>>> a_tuple[1:3]	# True		# ('b', 'grim')
	>>> a_tuple.index('grim')					# 2
	>>> list(a_tuple)		>>> tuple(a_list)	# thawing/freezing
	>>> type((False))		>>> type((False,))	# bool, tuple	comma = 1 item tuple
	''' assigning multiple values at once '''
	>>> v = ('a', 2, True)	>>> (x, y, z) = v	# x=a, y=2, z=True
	>>> (MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)	# MON=0, TUE=1, SUN=6

''' { SETS } - unordered bag of unique values '''

	>>> a_set = {2, 5}		>>> a_set = set(a_list)		>>> 5 in a_set
	>>> a_set = set()		>>> what_am_i = {}	# empty set		# empty dictionary
	>>> a_set.add(7)		>>> len(a_set)		# {2, 7, 5}		# 3
	>>> a_set.update(items...)		# adds multiple items to set
	>>> a_set.remove(7)		>>> a_set.discard(7)	# same, but remove will exception
	>>> a_set.pop()		# same as for list, but which one popped is arbitrary
	>>> a_set | b_set	>>> a_set.union(b_set)					# a or b
	>>> a_set & b_set	>>> a_set.intersection(b_set)			# a and b
	>>> a_set - b_set	>>> a_set.difference(b_set)				# a but not b
	>>> a_set ^ b_set	>>> a_set.symmetric_difference(b_set)	# a xor b
	>>> a_set.issubset(b_set)	>>> a_set.issuperset(b_set)

''' { DICTS: DICTIONARIES } - unordered set of key-value pairs '''

	>>> a_dict = {'server': 'db.example.com', 'database': 'mysql'}
	>>> a_dict['database']		# mysql
	>>> a_dict['user'] = 'mark'	>>> a_dict['User'] = 'jane'		# case-sensitive

	SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
				1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}
	>>> len(SUFFIXES)			>>> SUFFIXES[1024][2]	# 2		# 'GiB'

''' NONE '''

	None is Python's null value. It is not the same as False, 0, empty string
	>>> type(None)		# <class 'NoneType'>
	>>> x = None	>>> y = None	>>> x == y			# True

''' FUNCTIONS '''
	def multiparam(foo, *args, **kwargs):
		print("-- I got", foo)
		for arg in args:
			print(arg)
		print("-" * 20)
		for kw in sorted(kwargs.keys()):
			print(kw, ":", kwargs[kw])
	>>> multiparam('cheese', 'smells good', 'on pizza', cust='John', boss='Sam', wild='Max')
	-- I got cheese
	smells good
	on pizza
	--------------------
	boss : Sam
	cust : John
	wild : Max
	
''' BETTER WAYS TO DO THINGS '''
	# iterating over an array
	for i in range(len(fruits)):	# bad
	for fruit in fruits:		for i, fruit in enumerate(fruits):	# good
	
	# extracting unique elements from list
	uniques = list(set(a_list))
	aonly = [item for item in a_list if item not in b_list]
	aonly = list(set(a_list) - set(b_list))
	
	# travering a dict
	for key in mydict.keys():
		value = mydict[key]		# bad
	for key, value in mydict.items():	# good, use .iteritems() for large dicts
	
	# merging dicts
	merged = {}
	for k, v in a_dict.items():
		merged[k] = value		# bad
	merged = a_dict.copy();		merged.update(b_dict)	# good
	

''' OS - files and directories '''
	>>> import os	>>> print(os.getcwd())		# C:\Python31
	>>> os.chdir('/Users/path')		>>> print(os.getcwd())	# C:\Users\path
	>>> print(os.path.join('Users/path', 'humansize.py'))	# /Users/path/humansize.py
	>>> pathname = os.path.join(os.path.expanduser('~'), 'code', humansize.py)
	# c:\Users\John\code\humansize.py
	>>> (dirname, filename) = os.path.split(pathname)
	>>> (basename, extension) = os.path.splitext(filename)	# ('humansize', '.py')
	>>> metadata = os.stat('file.xml')
	>>> metadata.st_mtime		# 1247520344.9537716	modified time (sec since epoch)
	>>> import time
	>>> time.localtime(metadata.st_mtime)	# time.struct_time for 2009-7-13,17:25:44
	>>> metadata.st_size		# 3070		size in bytes
	>>> print(os.path.realpath('file.xml'))	# c:\Users\John\code\file.xml
	''' GLOB - shell-like wildcards '''
	>>> import glob		>>> glob.glob('new/*.xml')	# ['new/a.xml', 'new/b.xml', ...]

''' LIST COMPREHENSIONS - map a list into another list by applying
		a function to each of the elements of the list '''
	>>> a_list = [1, 9, 8, 4]				# [1, 9, 8, 4]
	>>> [elem * 2 for elem in a_list]		# [2, 18, 16, 8], a_list unchanged
	>>> a_list = [elem * 2 for elem in a_list]	# now a_list has changed
	>>> [os.path.realpath(f) for f in glob.glob('*.xml')]	# can use any expression
	>>> [f for f in glob.glob('*.py') if os.stat(f).st_size > 6000]	# filtered

	''' DICTIONARY COMPREHENSIONS '''
	>>> mdata = [(f, os.stat(f)) for f in glob.glob('*.py')]	# list comprehension
	>>> mdata[0]		# ('abc.py', nt.stat_result(st_iud=0, st_size=2509, ...))
	>>> mdata_dict = {f:os.stat(f) for f in glob.glob('*.py')}	# dict comprehension
	>>> mdata_dict['abc.py'].st_size		# 2509
	>>> h_dict = {os.path.splitext(f)[0]:humansize.approximate_size(meta.st_size) \
	...           for f, meta in mdata_dict.items() if meta.st_size > 6000}
	>>> list(h_dict.keys())		>>> h_dict['bigfile']	# ['big', 'huge']	# 6.5KiB
	''' neat trick - swap keys and values (if values are immutable) '''
	>>> a_dict = {'a': 1, 'b':2, 'c': 3}
	>>> {value:key for key, value in a_dict.items()}	# {1: 'a', 2: 'b', 3: 'c'}

	''' SET COMPREHENSIONS '''
	>>> a_set = set(range(10))		# {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	>>> {x ** 2 for x in a_set}		# {0, 2, 4, 6, 8,10,12,14,16,18}
	>>> {x for x in a_set if x % 2 == 0}	# {0, 8, 2, 4, 6}
	>>> {2**x for x in range(10)}	# {32, 1, 2, 4, 8, 64, 128, 256, 16, 512}


''' STRINGS - bytes are bytes, characters are an abstraction '''

	>>> s = '深入 Python'	>>> len(s)		# 9, strings can be defined with ' or "
	>>> s[0]				>>> s + ' 3'	# '深'		# '深入 Python 3'
	>>> (user, pwd) = ('Bob', 'secret')
	>>> "{0}'s password is {1}".format(user, pwd)	# "Bob's password is secret"
	>>> suff = humansize.SUFFIXES[1000]		# ['KB','MB','GB', ...]
	>>> '1000{0[0]} = 1{0[1]}'.format(suff)	# 1000KB = 1MB		# {0[1]} = suff[1]
	>>> import sys, humansize
	>>> '1MB = 1000{0.modules[humansize].SUFFIXES[1000][0]}'.format(sys)
	# sys.modules is a dictionary where the keys are the imports as strings
	# {0.modules[humansize]} is = sys.modules['humansize'], there are no '' in ref
	''' FORMAT SPECIFIERS '''
	>>> '{0:.1f} GB'.format(698.24)		# 698.2 GB		fixed point 1 decimal place

	''' OTHER STRING METHODS '''
	>>> s = '''Finished files re-
	... quire science.'''		# splitlines on carriage returns
	>>> s.splitlines()			# ['Finished files re-', 'quire science.']
	>>> s.lower()	>>> s.upper()	>>> s.count('e')	# lower/uppercase	# 6
	>>> query = 'user=grim&pwd=secret&db=masterDB'
	>>> a_list = query.split('&')
	>>> lists = [v.split('=', 1) for v in a_list if '=' in v]
	>>> a_dict = dict(lists)	# {'user': 'grim', 'pwd': 'secret', 'db': 'masterDB'}
	# for URL query params use urllib.parse.parse_qs() instead

''' SLICING A STRING - just like a list '''
	>>> a_string = 'My alphabet starts where yours ends.'
	>>> a_string[3:11]	>>> a_string[26:-3]	# 'alphabet'	# 'ours en'
	>>> a_string[:18]	>>> a_string[18:]	# 'My alphabet starts'	# ' where yours ends.'

''' STRINGS VS BYTES - OMG '''
	# An immutable sequence of numbers betwen 0 and 255 is called a bytes object
	>>> by = b'abcd\x65'	>>> type(by)	# b'abcde'		# <class 'bytes'>
	>>> by += b'\xff'		>>> len(by)		# b'abcde\xff'	# 6
	>>> by[0]		>>> by[0] = 102			# 97	# exception, bytes is immutable
	>>> barr = bytearray(by)				# bytearray(b'abcde\xff')
	>>> barr[0] = 102						# bytearray(b'fbcde\xff')
	>>> s = 'abcde'			>>> by + s		# exception - can't mix bytes and strings
	>>> s.count(by[3])	# exception - can't convert bytes to string
	>>> s.count(by[3].decode('ascii'))		# 1		# by.decode returns string
	>>> s = '深入 Python'	>>> len(s)		# 9		# s.encode returns bytes
	>>> s.encode('utf-8')		# b'\xe6\xb7\xb1\xe5\x85\xa5 Python'	13 bytes
	>>> s.encode('gb18030')		# b'\xc9\xee\xc8\xeb Python'			11 bytes
	>>> by = s.encode('big5')	# b'\xb2`\xa4J Python'					11 bytes
	>>> r_trip = by.decode('big5')	>>> r_trip == s		# '深入 Python'	# True
	''' DEFAULT ENCODING for python3 files is UTF-8. Use this at top to change: '''
	#!/usr/bin/python3
	# -*- coding: windows-1252 -*-

''' REGULAR EXPRESSIONS - spoiler: just like Perl '''
	>>> import re	>>> re.sub('ROAD$', 'RD.', '100 N. BROAD ROAD')		# s/ROAD$/RD./
	>>> s = '100 BROAD ROAD APT. 3'		>>> re.sub('\\bROAD\\b', 'RD.', s)
	>>> re.sub(r'\bROAD\b', 'RD.', s)	# same as above, r'' is raw string
	>>> roman_numeral_pattern = '''
		^                   # beginning of string
		M{0,3}              # thousands - 0 to 3 Ms
		(CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 Cs),
							#            or 500-800 (D, followed by 0 to 3 Cs)
		(XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 Xs),
							#        or 50-80 (L, followed by 0 to 3 Xs)
		(IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 Is),
							#        or 5-8 (V, followed by 0 to 3 Is)
		$                   # end of string
		'''
	>>> re.search(roman_numeral_pattern, 'MCMLXXXIX', re.VERBOSE)		# verbose pattern mode
	>>> phonePattern = re.compile(r'\D*(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')
	>>> phonePattern.search('800-555-1212').groups()	# ('800', '555', '1212', '')

''' GENERATORS '''
	def plural(noun):
		if re.search('[sxz]$', noun):
			return re.sub('$', 'es', noun)
		elif re.search('[^aeioudgkprt]h$', noun):
			return re.sub('$', 'es', noun)
		elif re.search('[^aeiou]y$', noun):
			return re.sub('y$', 'ies', noun)
		else:
			return noun + 's'

	def match_sxz(noun):						def apply_sxz(noun):
		return re.search('[sxz]$', noun)			return re.sub('$', 'es', noun)
	def match_h(noun):							def apply_h(noun):
		return re.search('[^aeioudgkprt]h$', noun)	return re.sub('$', 'es', noun)
	def match_y(noun):							def apply_y(noun):
		return re.search('[^aeiou]y$', noun)		return re.sub('y$', 'ies', noun)
	def match_default(noun):					def apply_default(noun):
		return True									return noun + 's'
	rules = ((match_sxz, apply_sxz), (match_h, apply_h),	# tuples of functions
				(match_y, apply_y), (match_default, apply_default))
	def plural(noun):
		for matches_rule, apply_rule in rules:
			if matches_rule(noun):
				return apply_rule(noun)

	# this function builds other functions dynamically
	def build_match_and_apply_functions(pattern, search, replace):
		def matches_rule(word):
			return re.search(pattern, word)
		def apply_rule(word):
			return re.sub(search, replace, word)
		return (matches_rule, apply_rule)
	patterns = (('[sxz]$', '$', 'es'), ('[^aeioudgkprt]h$', '$', 'es'),
				('[^aeiou]y$', 'y$', 'ies'), ('$', '$', 's'))	# tuples of strings
	rules = [build_match_and_apply_functions(pattern, search, replace)
			for (pattern, search, replace) in patterns]	# tuples of funcs, as above
			
	pluralRules.txt
	[sxz]$            $  es
	[^aeioudgkprt]h$  $  es
	[^aeiou]y$       y$  ies
	$                 $  s
	--------------------
	rules = []
	with open('pluralRules.txt', encoding='utf-8') as pattern_file:
		for line in pattern_file:
			pattern, search, replace = line.split(None, 3)	# on whitespace 3 times
			rules.append(build_match_and_apply_functions(pattern, search, replace))
			

	def rules(rules_filename):
		with open('pluralRules.txt', encoding='utf-8') as pattern_file:
			for line in pattern_file:
				pattern, search, replace = line.split(None, 3)
				yield build_match_and_apply_functions(pattern, search, replace)

	def plural(noun, rules_filename='pluralRules.txt'):
		for matches_rule, apply_rule in rules(rules_filename):
			if matches_rule(noun):
				return apply_rule(noun)
		raise ValueError('no matching rule for {0}'.format(noun))
		
	>>> def make_counter(x):
	...		print('entering')
	...		while True:
	...			yield x						# yield pauses a function, next() resumes
	...			print('incr x')
	...			x = x + 1
	...
	>>> counter = make_counter(2)	>>> counter	# <generator object at 0x11435123>
	>>> next(counter)							# entering		# 2
	>>> next(counter)		>>> next(counter)	# incr x	# 3		# incr x	# 4

	def fib(max):
		a, b = 0, 1
		while a < max:
			yield a
			a, b = b, a + b
			
	>>> for n in fib(20):
	...		print(n, end=' ')		# 0 1 1 2 3 5 8 13
	>>> list(fib(20))				# [0, 1, 1, 2, 3, 5, 8, 13]

''' ITERATORS - from scratch '''
	class Fib:
		''' Iterator that yields numbers in the Fibonacci sequence '''
		def __init__(self, max):	# similar to a constructor, 
			self.max = max			# instance variable
		def __iter__(self):		# An iterator is just a class that defines __iter__()
			self.a = 0			# 1st param of all methods is self, but don't use when calling.
			self.b = 1			# Can call iter(fib) or is called magically, eg. for loop.
			return self			# Returns any object that implements __next__(), usually self
		def __next__(self):
			fib = self.a
			if fib > self.max:
				raise StopIteration		# not an error, but a normal condition to signal finish
			self.a, self.b = self.b, self.a + self.b
			return fib			# do not use yield here, that's only for generators

	>>> fib = fibonacci.Fib(20)	>>> fib		# <fibonacci.Fib object at 0x00DB8810>
	>>> fib.__class__		>>> fib.__doc__	# <class 'fibonacci.Fib'>	# prints the docstring
	>>> for n in Fib(20):			# this is exactly the same as the generator version above
	...		print(n, end=' ')		# 0 1 1 2 3 5 8 13
	>>> list(fib(20))				# [0, 1, 1, 2, 3, 5, 8, 13]

	class LazyRules:
		rules_filename = 'rules.txt'		# class variable (static, kind of)
		def __init__(self):
			self.pattern_file = open(self.rules_filename, encoding='utf-8')
			self.cache = []					# open file but don't read it yet
		def __iter__(self):
			self.cache_index = 0
			return self
		def __next__(self):
			self.cache_index += 1
			if len(self.cache) >= self.cache_index:
				return self.cache[self.cache_index - 1]
			if self.pattern_file.closed:
				raise StopIteration
			line = self.pattern_file.readline()
			if not line:
				self.pattern_file.close()
				raise StopIteration
			pattern, search, replace = line.split(None, 3)
			funcs = build_match_and_apply_functions(pattern, search, replace)
			self.cache.append(funcs)
			return funcs
			
	rules = LazyRules()		# happens once, on import

	>>> import plural6
	>>> r1 = plural6.LazyRules()	>>> r2 = plural6.LazyRules()
	>>> r1.rules_filename			>>> r2.rules_filename		# both 'rules.txt'
	>>> r2.rules_filename = 'override.txt'		# r1 is 'rules.txt'		# r2 is 'override.txt'
	>>> r2.__class__.rules_filename				# 'rules.txt' (class attribute hasn't changed)
	>>> r2.__class__.rules_filename = 'papaya.txt'	# now r1 is papaya	# r2 is override still

''' GENERATOR EXPRESSIONS '''
	>>> unique_characters = {'E', 'D', 'M', 'O', 'N', 'S', 'R', 'Y'}
	# generator expressions look like list comprehensions but using () instead of []
	>>> gen = (ord(c) for c in unique_characters)	>>> gen		# <generator object <genexpr> at 0x00DB8810>
	>>> next(gen)		>>> next(gen)		# 69, 68	# generator expressions return iterator
	>>> tuple(ord(c) for c in unique_characters)		# (69, 68, 77, 79, 78, 83, 82, 89)
	# casting a genexpr into a tuple, list, or set iterates thru all the values and returns all
	def ord_map(a_string):
		for c in a_string:
			yield ord(c)				# this generator function is functionally
	gen = ord_map(unique_characters)	# equivalent to the genexpr above

''' ITERTOOLS - iterators on steroids '''
	def solve(puzzle):		# solves alphametics puzzles
		words = re.findall('[A-Z]+', puzzle.upper())	# list of all regex found in string
		unique_characters = set(''.join(words))
		assert len(unique_characters) <= 10, 'Too many letters'
		first_letters = {word[0] for word in words}	# generator expression. More efficient
		n = len(first_letters)						# than list comprehensions on cpu+ram
		sorted_characters = ''.join(first_letters) + ''.join(unique_characters - first_letters)
		characters = tuple(ord(c) for c in sorted_characters)
		digits = tuple(ord(c) for c in '0123456789')
		zero = digits[0]			# permutations(valuelist, len) returns an iterator for it
		for guess in itertools.permutations(digits, len(characters)):
			if zero not in guess[:n]:
				equation = puzzle.translate(dict(zip(characters, guess)))	# tr///
				if eval(equation):
					return equation

	if __name__ == '__main__':
		import sys
		for puzzle in sys.argv[1:]:
			print(puzzle)
			solution = solve(puzzle)		# ~/$ python3 alphametics.py "SEND + MORE == MONEY"
			if solution:					# SEND + MORE == MONEY
				print(solution)				# 9567 + 1085 == 10652

	''' MORE ITERTOOLS '''
	>>> import itertools	>>> list(itertools.product('ABC', '123'))	# Cartesian product
	# [('A', '1'), ('A', '2'), ('A', '3'), ('B', '1'), ('B', '2'), etc]
	>>> list(itertools.combinations('ABC', 2))	# [('A', 'B'), ('A', 'C'), ('B', 'C')]

	>>> names = list(open('people.txt', encoding='utf-8'))	# idiom returns list of all lines
	>>> names		# ['Dora\n', 'Ethan\n', 'Wesley\n', 'John\n', 'Anne\n']
	>>> names = [name.rstrip() for name in names]	# removes newline at end of each item
	>>> names = sorted(names)			# ['Anne', 'Dora', 'Ethan', 'John', 'Wesley']
	>>> names = sorted(names, key=len)	# ['Anne', 'Dora', 'John', 'Ethan', 'Wesley'] by len()
	>>> groups = itertools.groupby(names, len)	# groupby works on pre-sorted sequences returns
	>>> groups			# <itertools.groupby object at ...>			each group in an iterator
	>>> list(groups)	# [(4, <itertools._grouper object at>), (5, <itertools._grouper object at>)]
	>>> groups = itertools.groupby(names, len)	# start over, list() exhausted iterator
	>>> for name_length, name_iter in groups:
	...		print('Names with {0:d} letters:'.format(name_length))
	...		for name in name_iter:	# 'Names with 4 letters:\nAnne\nDora\nJohn\n'
	...			print(name)			# 'Names with 5 letters:\nEthan\n ...with 6:\nWesley\n'

	>>> list(range(0, 3))	>>> list(range(10, 13))			# [0, 1, 2]		# [10, 11, 12]
	>>> list(itertools.chain(range(0,3), range(10, 13)))	# [0, 1, 2, 10, 11, 12]
	>>> list(zip(range(0,3), range(10, 13)))		# [(0, 10), (1, 11), (2, 12)]
	>>> list(zip(range(0,3), range(10, 14)))		# same
	>>> list(itertools.zip_longest(range(0,3), range(10, 14)))	# [... (2, 12), (None, 13)]

	>>> eval('1 + 1 == 2')		>>> eval ('1 + 1 == 3')		# True		# False
	>>> eval('"A" + "B"')		>>> eval('"AAAAA".count("A")')	# 'AB'	# 5
	>>> eval('"MARK".translate({65: 79})')	>>> eval('["*"] * 3')	# 'MORK'	# ['*', '*', '*']
	>>> x = 5 		>>> eval("pow(x, 2)")	# 25
	''' eval() is EVIL '''
	>>> import subprocess	>>> eval("subprocess.getoutput('ls ~')")	# string = output of command 'ls ~'
	>>> eval("subprocess.getoutput('rm /some/random/file')")			# eval() is EVIL
	''' eval() is EVIL - without an import even '''
	>>> eval("__import__('subprocess').getoutput('rm -rf ~')")	# buhbye all files 

	>>> x = 5	>>> eval("x * 5", {}, {})	# exception - x not defined
	>>> eval("x * 5", {"x": x}, {})			# 25	the last 2 params are global and local namespaces
	>>> import math		>>> eval("math.sqrt(x)", {"x": x}, {})	# exception - math not defined
	>>> eval("pow(5, 2)", {}, {})			# 25	built-in functions are always in scope
	>>> eval("__import__('math').sqrt(5)", {}, {})	# 2.236...
	''' This one is safe, nuking the builtins means import is undefined '''
	>>> eval("__import__('subprocess').getoutput('rm -rf /')", {"__builtins__": None}, {})

''' UNIT TESTS - Write a test that fails and then code until it passes '''
	# romantest.py
	import roman1, unittest		# import your program and unittest

	class KnownValues(unittest.TestCase):	# unit tests subclass TestCase 
		known_values = ( (1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V'), (6, 'VI'), (7, 'VII'),
			(8, 'VIII'), (9, 'IX'), (10, 'X'), (50, 'L'), (100, 'C'), (500, 'D'), (1000, 'M'),
			(31, 'XXXI'), (148, 'CXLVIII'), (294, 'CCXCIV'), (312, 'CCCXII'), (421, 'CDXXI'),
			(528, 'DXXVIII'), (621, 'DCXXI'), (782, 'DCCLXXXII'), (870, 'DCCCLXX'), (941, 'CMXLI'),
			(1043, 'MXLIII'), (1110, 'MCX'), (1226, 'MCCXXVI'), (1301, 'MCCCI'), (1485, 'MCDLXXXV'),
			(1509, 'MDIX'), (1607, 'MDCVII'), (1754, 'MDCCLIV'), (1832, 'MDCCCXXXII'), (1993, 'MCMXCIII'),
			(2074, 'MMLXXIV'), (2152, 'MMCLII'), (2212, 'MMCCXII'), (2343, 'MMCCCXLIII'), (2499, 'MMCDXCIX'),
			(2574, 'MMDLXXIV'), (2646, 'MMDCXLVI'), (2723, 'MMDCCXXIII'), (2892, 'MMDCCCXCII'),
			(2975, 'MMCMLXXV'), (3051, 'MMMLI'), (3185, 'MMMCLXXXV'), (3250, 'MMMCCL'), (3313, 'MMMCCCXIII'),
			(3408, 'MMMCDVIII'), (3501, 'MMMDI'), (3610, 'MMMDCX'), (3743, 'MMMDCCXLIII'),
			(3844, 'MMMDCCCXLIV'), (3888, 'MMMDCCCLXXXVIII'), (3940, 'MMMCMXL'), (3999, 'MMMCMXCIX'))
	# all tests start with 'test', take no params and return nothing. if no exception, test passes!
		def test_to_roman_known_values(self):
			'''to_roman should give known result with known input'''
			for integer, numeral in self.known_values:
				result = roman1.to_roman(integer)
				self.assertEqual(numeral, result)
		def test_non_integer(self):
			'''to_roman should fail with non-integer input'''
			self.assertRaises(roman4.NotIntegerError, roman4.to_roman, 0.5)
		def test_from_roman_known_values(self):
			'''from_roman should give known result with known input'''
			for integer, numeral in self.known_values:
				result = roman5.from_roman(numeral)
				self.assertEqual(integer, result)

	class 
	if __name__ == '__main__':
		unittest.main()

	you@localhost:~/code$ python3 romantest.py -v
	test_to_roman_known_values (__main__.KnownValues)
	to_roman should give known result with known input ... ok
	----------------------------------------------------------------------
	Ran 1 test in 0.016s
	OK

	class InvalidRomanNumeralError(ValueError): pass

	def to_roman(n):
		''' convert integer to roman numeral '''
		if not (0 < n < 4000):								# nice comparison shortcut
			raise OutOfRangeError('number out of range (must be 1..3999)')
		if not isinstance(n, int):
			raise NotIntegerError('non-integers cannot be converted')
		result = ''
		for numeral, integer in roman_numeral_map:
			while n >= integer:
				result += numeral
				n -= integer
		return result

	class test_roundtrip(unitTest.TestCase):
		def test_roundtrip(self):
			'''from_roman(to_roman(n))==n for all n'''
			for integer in range(1,4000):
				numeral = roman5.to_roman(integer)
				result = roman5.from_roman(numeral)
				self.assertEqual(integer, result)

	def from_roman(s):
		'''convert Roman numeral to integer'''
		if not roman_numeral_pattern.search(s):
			raise InvalidRomanNumeralError('Invalid Roman numeral: {0}'.format(s))
		result = 0
		index = 0
		for numeral, integer in roman_numeral_map:
			while s[index:index+len(numeral)] == numeral:
				result += integer
				index += len(numeral)
				
''' REFACTORING '''
	class OutOfRangeError(ValueError): pass
	class NotIntegerError(ValueError): pass
	class InvalidRomanNumeralError(ValueError): pass

	roman_numeral_map = (('M',  1000),
						 ('CM', 900),
						 ('D',  500),
						 ('CD', 400),
						 ('C',  100),
						 ('XC', 90),
						 ('L',  50),
						 ('XL', 40),
						 ('X',  10),
						 ('IX', 9),
						 ('V',  5),
						 ('IV', 4),
						 ('I',  1))

	to_roman_table = [ None ]
	from_roman_table = {}

	def to_roman(n):
		'''convert integer to Roman numeral'''
		if not (0 < n < 5000):
			raise OutOfRangeError('number out of range (must be 1..4999)')
		if int(n) != n:
			raise NotIntegerError('non-integers can not be converted')
		return to_roman_table[n]

	def from_roman(s):
		'''convert Roman numeral to integer'''
		if not isinstance(s, str):
			raise InvalidRomanNumeralError('Input must be a string')
		if not s:
			raise InvalidRomanNumeralError('Input can not be blank')
		if s not in from_roman_table:
			raise InvalidRomanNumeralError('Invalid Roman numeral: {0}'.format(s))
		return from_roman_table[s]

	def build_lookup_tables():
		def to_roman(n):			# redefining a local scope version of to_roman() 
			result = ''
			for numeral, integer in roman_numeral_map:
				if n >= integer:
					result = numeral
					n -= integer
					break
			if n > 0:
				result += to_roman_table[n]
			return result

		for integer in range(1, 5000):
			roman_numeral = to_roman(integer)		# calls local scope version
			to_roman_table.append(roman_numeral)		# add to lookup tables
			from_roman_table[roman_numeral] = integer

	build_lookup_tables()		# this gets called ONCE (max), ON IMPORTING the module
	# no more regexs, no more looping, O(1) conversion to and from. 

''' FILES '''
	>>> a_file = open('examples/chinese.txt', encoding='utf-8')		# filename is 'examples/chinese.txt'
			# filenames are always a (optional) path and filename
			# forward slash always Just Works, regardles of operating system used
			# this path is relative because it does not start with a sash or drive letter
			# it is a string and therefore unicode (non-ascii filepaths supported!)
			# doesn't have to be on local system. If the OS can access it as a file Python can open it
		''' always specify the encoding. The default is different on each platform! '''
	>>> a_file.name	>>> a_file.encoding	>>> a_file.mode	# 'examples/chinese.txt'	# 'utf-8'	# 'r'
	>>> a_file.read()		# 'Dive Into Python 是为有经验的程序员编写的一本 Python 书。\n'
	>>> a_file.read()		# ''	reading file again does not throw an exception
	>>> a_file.seek(0)		# 0 	move to specific BYTE
	>>> a_file.read(17)		# 'Dive Into Python '	optional param is how many CHARS to read
	>>> a_file.read(1)		>>> a_file.tell()		# '是'		# 20	in BYTES ( = 17 chars + 1 char)
	>>> a_file.seek(18)		>>> a_file.read(1)		# 18		# exception!
	>>> a_file.close()		>>> a_file.closed		# True		Closing a closed file is a no-op
	
	n = 0
	with open('examples.chinese.txt', encoding='utf-8') as a_file:	# WITH creates a runtime context
		for a_line in a_file:	# and the stream object (a_file) acts as context manager. When the
			n += 1				# block ends the runtime context exits and the stream object calls
			print('{:>4} {}'.format(n, a_line.rstrip()))	# its own close() automatically. Guaranteed.
	
''' WRITING to text files '''
	# pass mode='w' or mode='a' to open() for write/append mode. File will be created if need be.
	with open('test.log', mode='w', encoding='utf-8') as a_file:		# always specify encoding
		a_file.write('test succeeded')
	with open('test.log', mode='a', encoding='utf-8') as a_file:
		a_file.write('and again')
	with open('test.log', encoding='utf-8') as a_file:
		print(a_file.read())				# test succeededand again		(newlines do not get included)

''' BINARY FILES '''
	>>> an_image = open('examples/dog.jpg', mode='rb')	>>> an_image.mode	# 'rb'	b for binary
	>>> an_image.name		>>> an_image.encoding		# 'examples/dog.jpg'	# exception
	>>> an_image.tell()		>>> data = an_image.read(3)		# 0		# b'\xff\xd8\xff'
	>>> type(data)		>>> an_image.tell()		# <class 'bytes'>	# 3
	>>> an_image.seek(0)	>>> data = an_image.read()	>>> len(data)		# 3150
	''' read() now is in BYTES, not chars, because it is a binary file '''

''' STREAM OBJECTS from non-file sources '''
	>>> a_string = 'PapayaWhip is the new black.'
	>>> import io		>>> a_file = io.StringIO(a_string)		# makes a stream object out of a string
	>>> a_file.read() seek() tell() etc.						# see also io.BytesIO for binary
	
''' HANDLING COMPRESSED FILES '''
	you@localhost:~$ python3
	>>> import gzip
	>>> with gzip.open('out.log.gz', mode='wb') as z_file:	# always open gzip files as binary
	...		z_file.write('A nine mile walk is no joke, especially in the rain.'.encode('utf-8'))
	>>> exit()
	you@localhost:~$ ls -l out.log.gz		# -rw-r--r--  1 you you    79 yyyy-mm-dd hh:mm out.log.gz
	you@localhost:~$ gunzip out.log.gz		you@localhost:~$ cat out.log
	A nine mile walk is no joke, especially in the rain.
	
''' STDIN, STDOUT, STDERR '''
	>>> for i in range(3):
	...		print('PapayaWhip')			# PapayaWhip\nPapayaWhip\nPapayaWhip\n
	>>> import sys
	>>> for i in range(3):
	...		l = sys.stdout.write('is the')	# is theis theis the		note lack of newlines.
	
	import sys
	class RedirectStdoutTo:
		def __init__(self, out_new):
			self.out_new = out_new
		def __enter__(self):			# a custom context manager defines enter and exit
			self.out_old = sys.stdout
			sys.stdout = self.out_new
		def __exit__(self, *args):		# enter and exit are called at beginning and end of WITH
			sys.stdout = self.out_old
	print('A')
	with open('out.log', mode='w', encoding='utf-8') as a_file, RedirectStdoutTo(a_file):
		print('B')		# when this program is run, B gets written to out.log instead of stdout
	print('C')
	
	with open('out.log', mode='w', encoding='utf-8') as a_file:		# equivalent to above
		with RedirectStdoutTo(a_file):		# as clause not required
			print('B')

''' <XML/> '''
	<?xml version='1.0' encoding='utf-8'?>		# first line before root element (optional)
	<feed xmlns='http://www.w3.org/2005/Atom'>	# root element with namespace
		<title>dive into mark</title>	</feed>		# there can be only one root element
	
	<?xml version='1.0' encoding='utf-8'?>		# equivalent to above, with prefix
	<atom:feed xmlns:atom="http://www.w3.org/2005/Atom">	# all attributes must be quoted '/"
		<atom:title>dive into mark</atom:title>	</atom:feed>
	
	# sample xml file
	<?xml version='1.0' encoding='utf-8'?>
	<feed xmlns='http://www.w3.org/2005/Atom' xml:lang='en'>	# element and children are in english
	  <title>dive into mark</title>			# ^ the xml: prefix is a builtin namespace for each xml doc
	  <subtitle>currently between addictions</subtitle>
	  <id>tag:diveintomark.org,2001-07-29:/</id>		# gid, see RFC4151
	  <updated>2009-03-27T21:56:07Z</updated>
	  <link rel='alternate' type='text/html' href='http://diveintomark.org/'/>
			''' ^ alternate HTML representation of this feed (not xml comments btw) '''
	  <link rel='self' type='application/atom+xml' href='http://diveintomark.org/feed/'/>
	  <entry>
		<author>
		  <name>Mark</name>
		  <uri>http://diveintomark.org/</uri>
		</author>
		<title>Dive into history, 2009 edition</title>
		<link rel='alternate' type='text/html'
		  href='http://diveintomark.org/archives/2009/03/27/dive-into-history-2009-edition'/>
			''' ^ alternate HTML representation of this entry '''
		<id>tag:diveintomark.org,2009-03-27:/archives/20090327172042</id>	# gid for entry
		<updated>2009-03-27T21:56:07Z</updated>
		<published>2009-03-27T17:20:42Z</published>
		<category scheme='http://diveintomark.org' term='diveintopython'/>
		<category scheme='http://diveintomark.org' term='docbook'/>
		<category scheme='http://diveintomark.org' term='html'/>
	    <summary type='html'>Putting an entire chapter on one page sounds
		  bloated, but consider this &amp;mdash; my longest chapter so far
		  would be 75 printed pages, and it loads in under 5 seconds&amp;hellip;
		  On dialup.</summary>
	  </entry>
	  <entry>
		<author>
		  <name>Mark</name>
		  <uri>http://diveintomark.org/</uri>
		</author>
		<title>Accessibility is a harsh mistress</title>
		<link rel='alternate' type='text/html'
		  href='http://diveintomark.org/archives/2009/03/21/accessibility-is-a-harsh-mistress'/>
		<id>tag:diveintomark.org,2009-03-21:/archives/20090321200928</id>
		<updated>2009-03-22T01:05:37Z</updated>
		<published>2009-03-21T20:09:28Z</published>
		<category scheme='http://diveintomark.org' term='accessibility'/>
		<summary type='html'>The accessibility orthodoxy does not permit people to
		  question the value of features that are rarely useful and rarely used.</summary>
	  </entry>
	  <entry>
		<author>
		  <name>Mark</name>
		</author>
		<title>A gentle introduction to video encoding, part 1: container formats</title>
		<link rel='alternate' type='text/html'
		  href='http://diveintomark.org/archives/2008/12/18/give-part-1-container-formats'/>
		<id>tag:diveintomark.org,2008-12-18:/archives/20081218155422</id>
		<updated>2009-01-11T19:39:22Z</updated>
		<published>2008-12-18T15:54:22Z</published>
		<category scheme='http://diveintomark.org' term='asf'/>
		<category scheme='http://diveintomark.org' term='avi'/>
		<category scheme='http://diveintomark.org' term='encoding'/>
		<category scheme='http://diveintomark.org' term='flv'/>
		<category scheme='http://diveintomark.org' term='GIVE'/>
		<category scheme='http://diveintomark.org' term='mp4'/>
		<category scheme='http://diveintomark.org' term='ogg'/>
		<category scheme='http://diveintomark.org' term='video'/>
		<summary type='html'>These notes will eventually become part of a
		  tech talk on video encoding.</summary>
	  </entry>
	</feed>
	
''' PARSING XML '''
	# Python has traditional DOM and SAX parsers... but this library is ElementTree
	>>> import xml.etree.ElementTree as etree
	>>> tree = etree.parse('examples/feed.xml')		# returns object representing entire document
	>>> root = tree.getroot()	>>> root	# <Element {http://www.w3.org/2005/Atom}feed at cd1eb0>
			# ElementTree represents elements as {namespace}localname. 
			# Elements act like a list, 		Attributes like a dictionary
	>>> root.tag		>>> len(root)	# '{http://www.w3.org/2005/Atom}feed'	# 8 (num of children)
	>>> for child in root:
	...		print(child)
	<Element {http://www.w3.org/2005/Atom}title at ...>
	<Element {http://www.w3.org/2005/Atom}subtitle at ...>
	<Element {http://www.w3.org/2005/Atom}id at ...>
	<Element {http://www.w3.org/2005/Atom}updated at ...>
	<Element {http://www.w3.org/2005/Atom}link at ...>
	<Element {http://www.w3.org/2005/Atom}entry at ...>
	<Element {http://www.w3.org/2005/Atom}entry at ...>
	<Element {http://www.w3.org/2005/Atom}entry at ...>
	>>> root.attrib		# {'{http://www.w3.org/XML/1998/namespace}lang': 'en'}	(= xml:lang)
	>>> root[4]			# <Element {http://www.w3.org/2005/Atom}link at ...>
	>>> root[4].attrib	# {'href': 'http://diveintomark.org', 'type': 'text/html', 'rel': 'alternate'}
	>>> root[3]		>>> root[3].attrib		# <Element {...}updated at ...>		# {}
	>>> root.findall('{http://www.w3.org/2005/Atom}entry')
	[<Element {...}entry at ...>, <Element {...}entry at ...>, <Element {...}entry at ...>]
	>>> root.findall('{http://www.w3.org/2005/Atom}author')		# []	empty, author not direct child
	>>> entries = tree.findall('{ns}entry')		>>> len(entries)	# same as tree.getroot().findall()
	>>> title_element = entries[0].find('{ns}title')	# .text = 'Dive into history, 2009 edition'
	>>> foo_elem = entries[0].find('{ns}foo')	>>> type(foo_elem)	# <class 'NoneType'>
	>>> if element.find('...') is not None		# how to test if an element was actually found
	>>> all_links = tree.findall('//{ns}link')	''' the two // mean return any descendant '''
	''' For something faster go get the lxml 3rd party library which extends ElementTree '''

''' GENERATING XML '''
	>>> import xml.etree.ElementTree as etree
	>>> new_feed = etree.Element('{http://www.w3.org/2005/Atom}feed',		# create root element
	...		attrib={'{http://www.w3.org/XML/1998/namespace}lang': 'en'})	# and add attribute
	>>> print(etree.tostring(new_feed))				# tostring() serializes the element (and children)
				# <ns0:feed xmlns:ns0='http://www.w3.org/2005/Atom' xml:lang='en'/>
		# which is same as <feed xmlns='http://www.w3.org/2005/Atom' xml:lang='en'/>
	>>> new_feed.set('{ns}attribute', 'value')		
	>>> title = etree.SubElement(new_feed, 'title', attrib={'type':'html'})	# sub element
	>>> print(etree.tostring(new_feed))		# <ns0:feed ...><ns0:title type='html'/></feed>
	>>> title.text = 'dive into &hellip;'
	>>> print(etree.tostring(new_feed))		# <feed ...><title ...>dive into &amp;hellip;</title></feed>
	''' also check out xmlwitch 3rd party library '''

''' PARSING BROKEN XML '''
	>>> parser = lxml.etree.XMLParser(recover=True)
	>>> tree = lxml.etree.parse('examples/broken.xml', parser)	# simply drops anything abnormal
	>>> parser.error_log	# broken.xml:3:28:FATAL:PARSER:ERR_UNDECLARED_ENTITY: Entity 'hellip' not defined
							# and no exception raised.

''' SERIALIZING PYTHON OBJECTS - pickle '''
	# NOTE that cPickle is obsolete, it has been consolidated into pickle in Python 3
	# python instance 1						# python instance 2
	>>> shell = 1							>>> shell = 2
	
	>>> entry = {}		# make up some dict with different types of data
	>>> entry['title'] = 'Dive into history'
	>>> entry['link'] = None	>>> entry['id'] = b'\xDE\xD5\xB4\xF8'
	>>> entry['tags']  = ('diveintopython', 'docbook', 'html')	>>> entry['published'] = True
	>>> import time
	>>> entry['pub_date'] = time.strptime('Fri Mar 27 22:20:42 2009')
	>>> import pickle
	>>> with open('entry.pickle', 'wb') as f:	# create file, ALWAYS use binary for pickle
	...		pickle.dump(entry, f)				# dump contents into file
							# file not guaranteed to work with other languages or prev vers of Python

	>>> shell		>>> entry		# 2		# NameError: name 'entry' is not defined
	>>> import pickle
	>>> with open('entry.pickle', 'rb') as f:	# open file to read
	...		entry = pickle.load(f)				# load it into variable
	...		entry2 = pickle.load(f)				# and another
	>>> entry == entry2			>>> entry is entry2		# True		# False (it is a copy)
	''' SERIALIZING WITHOUT A FILE '''
	>>> shell		>>> b = pickle.dumps(entry)		# 1		# b is now a bytes object
	>>> entry3 = pickle.loads(b)	>>> entry == entry3		# True
	''' DEBUGGING PICKLE FILES '''
	>>> import pickletools
	>>> with open('entry.pickle', 'rb') as f:
	... 	pickletools.dis(f)			# prints a disassembly of pickle file, and protocol version.
	
	import pickletools					# this routine returns just the protocol version
	def protocol_version(file_object):
		maxproto = -1
		for opcode, arg, pos in pickletools.genops(file_object):
			maxproto = max(maxproto, opcode.proto)
		return maxproto
	
''' SERIALIZING for use with other languages - JSON (RFC4627) '''
	# NOTE that the JavaScript Object Notation is text based (must be UTF-8, UTF-16, or UTF-32).
	# It is case sensitive, and ignores whitespace between values
	>>> shell		>>> basic_entry = {}		# 1		# empty dict
	>>> basic_entry['id'] = 256		>>> basic_entry['title'] = 'Dive into history'
	>>> basic_entry['tags'] = ('diveintopython', 'docbook', 'html')
	>>> basic_entry['published'] = True		>>> basic_entry['link'] = None
	>>> import json
	>>> with open('basic.json', mode='w', encoding='utf-8') as f:	# can never go wrong w utf-8
	...		json.dump(basic_entry, f, indent=0)
	you@locahost:~/$ cat basic.json	# {"published": true, "tags": ["diveintopython", "docbook", "html"], 
	# "comments_link": null, "id": 256, "title": "Dive into history"}
	''' USING JSON with unsupported datatypes - tuples and bytes '''
	# add a mini-serialization format for your datatype
	def to_json(python_object):
		if isinstance(python_object, bytes):	# here convert into dict with value as list of ints
			return {'__class__': 'bytes', '__value__': list(python_object)}
		if isinstance(python_object, time.struct_time):		# here convert time struct into string
			return {'__class__': 'time.asctime', '__value__': time.asctime(python_object)}
		raise TypeError(repr(python_object) + ' is not JSON serializable')
	
	>>> with open('entry.json', 'w', encoding='utf-8') as f:
	...		json.dump(entry, f, default=to_json)	# hook in your routine to the default
	
	>>> shell		>>> del entry		>>> entry	# 2		# NameError: name 'entry' is not defined
	>>> import json
	>>> with open('entry.json', 'r', encoding='utf-8') as f:
	...		entry = json.load(f)
	>>> entry		# same as dumped ... EXCEPT bytes and time are dictionaries now
	
	def from_json(json_object):		# parameter is not string, it's a python object (after deserialize)
		if '__class__' in json_object:
			if json_object['__class__'] == 'bytes':
				return bytes(json_object['__value__'])
			if json_object['__class__'] == 'time.asctime':
				return time.strptime(json_object['__value__'])
		return json_object
	
	>>> with open('entry.json', 'r', encoding='utf-8') as f:
	...		entry = json.load(f, object_hook=from_json)
	...		entry2 = json.load(f, object_hook=from_json)
	>>> entry == entry2		# False		why? because the 'tags' tuple was converted to a list. fyi.

''' HTTP WEB SERVICES '''
	# use httplib2 3rd party library instead of http.client or urllib.request because
	# it supports caching, last-modified date checking, ETags, compression, and redirects
	>>> import urllib.request		>>> a_url = 'http://diveintopython3.org/examples/feed.xml'
	>>> data = urllib.request.urlopen(a_url).read()		# the quick and dirty way
	>>> type(data)		# <class 'bytes'>	always bytes, not characters
	>>> print(data)		# <?xml version='1.0' encoding='utf-8'?><feed xmlns=...> ...
	''' debug what's being sent over the network '''
	>>> from http.client import HTTPConnection
	>>> HTTPCOnnection.debugLevel = 1				# debugging prints in real time the request
	>>> response = urllib.request.urlopen(a_url)	# and response information:
	  send: b'GET /examples/feed.xml HTTP/1.1
	  Host: diveintopython3.org
	  Accept-Encoding: identity				# uncompressed only
	  User-Agent: Python-urllib/3.1'
	  Connection: close
	  reply: 'HTTP/1.1 200 OK'	...
	>>> print(response.headers.as_string())
	  Date: Sun, 31 May 2009 19:23:06 GMT
	  Server: Apache
	  Last-Modified: Sun, 31 May 2009 06:39:55 GMT
	  ETag: "bfe-93d9c4c0"
	  Accept-Ranges: bytes
	  Content-Length: 3070				# if this was compressed it would be only 941
	  Cache-Control: max-age=86400
	  Expires: Mon, 01 Jun 2009 19:23:06 GMT
	  Vary: Accept-Encoding
	  Connection: close
	  Content-Type: application/xml
	>>> data = response.read()		>>> len(data)		# 3070
	>>> response2 = urllib.request.urlopen(a_url)	# perform same request again
	  # (same request data sent)
	>>> print(response2.headers.as_string())		# download the same 3070 AGAIN
	  # (same response headers)
	>>> data2 = response2.read()	>>> len(data2)	>>> data == data2	# 3070		# True
''' HTTPLIB2 - the better way '''
	# download and install http://www.diveintopython3.net/http-web-services.html#introducing-httplib2
	>>> import httlib2		>>> h = httlib2.Http('.cache')	# always pass dir to cache
	>>> response, content = h.request(a_url)	>>> response.status		# 200
	>>> content[:52]		# b"<?xml version='1.0' encoding='utf-8'?>\r\n<feed xmlns="
	>>> len(content)		# 3070
   ''' caching - relaunch the shell '''
	>>> import httplib2		>>> httplib2.debuglevel = 1		# set BEFORE making the Http object
	>>> h = httplib2.Http('.cache')			>>> a_url = 'http://diveintopython3.org/examples/feed.xml'
	>>> response, content = h.request(a_url)
	  # nothing gets sent to the server, nothing gets returned from the server
	>>> len(content)		>>> response.status		# 3070		# 200
	>>> response.fromcache		# True		"received" data from cache. it Just Works.
	>>> response2, content2 = h.request(a_url, headers={'cache-control':'no-cache'})
	  connect: (diveintopython3.org, 80)			# add this ^ to bypass all caches
	  send: b'GET /examples/feed.xml HTTP/1.1
	  Host: diveintopython3.org
	  user-agent: Python-httplib2/$Rev: 259 $
	  accept-encoding: deflate, gzip			# compression encodings that we can handle
	  cache-control: no-cache'
	  reply: 'HTTP/1.1 200 OK'  ...
	>>> response2.status		>>> response2.fromcache		# 200		# False
	>>> print(dict(response2.items()))		# {'status': '200', 'content-length': '3070', ... }
   ''' ETag and Last-Modified headers '''
	>>> reponse, content = h.request('http://www.diveintopython3.org/')	# first time fetching this
	  # request data sent
	>>> print(dict(response.items()))		# {'status': '200', 'content-length': '6657', ... }
	# 'etag': '"7f806d-1a01-9fb97900"', 'last-modified': 'Tue, 02 Jun 2009 02:51:48 GMT', ... }
	>>> reponse, content = h.request('http://www.diveintopython3.org/')	# next time fetching this
	  # request data sent, but also with:
	  if-none-match: "7f806d-1a01-9fb97900"
	  if-modified-since: Tue, 02 Jun 2009 02:51:48 GMT
	  reply: 'HTTP/1.1 304 Not Modified'		# server sent 304 back and no data
	>>> response.fromcache	>>> response.status			# True	# 200 (what was in the cache)
	>>> len(content) 		>>> response.dict['status']	# 6657	# 304 (actual header code)
   ''' compression '''
	>>> print(dict(response.items()))		# {'status': '200', '-content-encoding': 'gzip', ... }
	# 'content-length': '6657' ... }	here the server sent a gzip and we already uncompressed it
   ''' redirects '''
	# httplib2 automatically follows temporary redirects
	>>> response, content = h.request('http://diveintopython3.org/feed-302.xml')
	  send: b'GET /feed-302.xml HTTP/1.1 ... '
	  reply: 'HTTP/1.1 302 Found'		# this response also includes Location header
	  send: b'GET /examples/feed.xml HTTP/1.1 ... '		# so we follow that immediately
	  reply: 'HTTP/1.1 200 OK'	# and response will hold the response from the final URL
	>>> response				# httplib2 also includes a 'content-location' key for final URL
	>>> response.previous		>>> response.previous.previous	# previous URL	# None
	>>> response2, content2 = h.request('http://diveintopython3.org/feed-302.xml')
	  send: b'GET /feed-302.xml HTTP/1.1 ... '
	  reply: 'HTTP/1.1 302 Found'		# same response but no 2nd request this time (cached)
	>>> content2 == content		# True
	# permanent redirects are just as simple
	>>> response, content = h.request('http://diveintopython3.org/feed-301.xml')
	  send: b'GET /feed-301.xml HTTP/1.1 ... '
	  reply: 'HTTP/1.1 301 Moved Permanently'		# again no 2nd request (cached)
	>>> response2, content2 = h.request('http://diveintopython3.org/feed-301.xml')
	>>> response2.fromcache		>>> content2 == content		# True		# True
	# This request did not even hit the network for the original URL
   ''' HTTP POST '''
	#   Identi.ca REST API Method: statuses/update from http://laconi.ca/trac/wiki/TwitterCompatibleAPI
	# Updates the authenticating user’s status. Requires the status parameter specified below. 
	# Request must be a POST.

	# url - https://identi.ca/api/statuses/update.format (where format is:)
	# Formats - xml, json, rss, atom
	# http Method(s) - POST
	# Requires Authentication - true
	# Parameters - status. Required. The text of your status update. url-encode as necessary.
	>>> from urllib.parse import urlencode					# url-encodes a dictionary
	>>> data = {'status': 'Test update from Python 3'}
	>>> urlencode(data)										# 'status=Test+update+from+Python+3'
	>>> import httplib2
	>>> httplib2.debuglevel = 1
	>>> h = httplib2.Http('.cache')
	>>> h.add_credentials('diveintomark', 'MY_SECRET_PASSWORD', 'identi.ca')
	>>> resp, content = h.request('https://identi.ca/api/statuses/update.xml',	# authentication
	... 'POST', urlencode(data), 			# type of request, and PAYLOAD
	... headers={'Content-Type': 'application/x-www-form-urlencoded'})
	 send: b'POST /api/statuses/update.xml HTTP/1.1
	 Host: identi.ca
	 Accept-Encoding: identity
	 Content-Length: 32
	 content-type: application/x-www-form-urlencoded
	 user-agent: Python-httplib2/$Rev: 259 $
	 
	 status=Test+update+from+Python+3'
	 reply: 'HTTP/1.1 401 Unauthorized'				# server says first request is unauthorized
	 send: b'POST /api/statuses/update.xml HTTP/1.1			# immediately request again
	 Host: identi.ca
	 Accept-Encoding: identity
	 Content-Length: 32
	 content-type: application/x-www-form-urlencoded
	 authorization: Basic SECRET_HASH_CONSTRUCTED_BY_HTTPLIB2	# this time with the add_credentials
	 user-agent: Python-httplib2/$Rev: 259 $
	 
	 status=Test+update+from+Python+3'
	 reply: 'HTTP/1.1 200 OK'
	>>> print(content.decode('utf-8'))		# content always return as bytes, convert to string
	<?xml version="1.0" encoding="UTF-8"?>	# what server sends after success varies by web service API
	<status>								# in this case, it's an xml document
	 <text>Test update from Python 3</text>
	 <id>5131472</id>
	 ...
	</status>
   ''' BEYOND GET AND POST '''
	>>> from xml.etree import ElementTree as etree		# hey, I know how to parse xml
	>>> tree = etree.fromstring(content)	# find 1st id element and extract its contents
	>>> status_id = tree.findtext('id')		>>> status_id		# '5131472'
	>>> url = 'https://identi.ca/api/statuses/destroy/{0}.xml'.format(status_id)
	>>> resp, deleted_content = h.request(url, 'DELETE')		# ask server to delete the message
	 send: b'DELETE /api/statuses/destroy/5131472.xml HTTP/1.1	
	 Host: identi.ca
	 Accept-Encoding: identity
	 user-agent: Python-httplib2/$Rev: 259 $
	 
	 reply: 'HTTP/1.1 401 Unauthorized'
	 send: b'DELETE /api/statuses/destroy/5131472.xml HTTP/1.1
	 Host: identi.ca
	 Accept-Encoding: identity
	 authorization: Basic SECRET_HASH_CONSTRUCTED_BY_HTTPLIB2
	 user-agent: Python-httplib2/$Rev: 259 $
	 
	 reply: 'HTTP/1.1 200 OK'				# done!
	>>> resp.status							# 200
''' MULTI-FILE modules '''
	# instead of the file 'chardet.py' have a folder 'chardet' with file '__init__.py' in it. Then
	# Python assues that all files in the folder are part of the same module as if in a single .py
	>>> import chardet		>>> dir(chardet)	# ['__builtins__', '__doc__', '__file__', '__name__',
	>>> chardet									# '__package__', '__path__', '__versoin__', 'detect']
	# <module 'chardet' from 'C:\path_to\chardet\__init__.py'>
	# contents of __init__.py can be anything from nothing to everything, here's this one:
	def detect(aBuf):
		from . import universaldetector		# relative import from current directory
		u = universaldetector.UniversalDetector()
		u.reset()
		u.feed(aBuf)
		u.close()
		return u.result
''' DISTRIBUTION '''
	# setup.py is the usual setup script for disutils
	# chardet's setup.py
	from distutils.core import setup
	setup(								# most setup scripts are just this one call to setup().
		name = "chardet",				# this function REQUIRES named parameters
		version = "1.0.2",
		author = "Mark Pilgrim",
		author_email = "mark@diveintomark.org",
		url = "http://chardet.feedparser.org/",		# parameters to here are required
		download_url = "http://chardet.feedparser.org/download/python3-chardet-1.0.1.tgz",
		packages = ["chardet"],
		keywords = ["encoding", "i18n", "xml"],
		classifiers = [
			"Programming Language :: Python",				# include this
			"Programming Language :: Python :: 3",			# include this
			"Development Status :: 4 - Beta",				# recommended
			"Environment :: Other Environment",
			"Intended Audience :: Developers",				# recommended
			"License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
			"Operating System :: OS Independent",			# include License and this
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Text Processing :: Linguistic",		# topics recommended
			],
		description = "Universal encoding detector",
		long_description = """\
	Universal character encoding detector
	-------------------------------------

	Detects
	- ASCII, UTF-8, UTF-16 (2 variants), UTF-32 (4 variants)
	- Big5, GB2312, EUC-TW, HZ-GB-2312, ISO-2022-CN (Traditional and Simplified Chinese)
	- EUC-JP, SHIFT_JIS, ISO-2022-JP (Japanese)
	- EUC-KR, ISO-2022-KR (Korean)
	- KOI8-R, MacCyrillic, IBM855, IBM866, ISO-8859-5, windows-1251 (Cyrillic)
	- ISO-8859-2, windows-1250 (Hungarian)
	- ISO-8859-5, windows-1251 (Bulgarian)
	- windows-1252 (English)
	- ISO-8859-7, windows-1253 (Greek)
	- ISO-8859-8, windows-1255 (Visual and Logical Hebrew)
	- TIS-620 (Thai)

	This version requires Python 3 or later; a Python 2 version is available separately.
	"""
	)
	# Disutils automatically includes the following files:
	# README.txt, setup.py, .py files needed by packages arg, .py files listed in py_modules arg.
	# To have it include other files, create a MANIFEST.in file such as:
	include COPYING.txt
	recursive-include docs *.html *.png		# include all html and png files in the docs folder
	# note that this is NOT python code. To build a source distribution:
	c:\path_to\chardet> c:\python31\python.exe setup.py sdist
	# the above creates a .zip file in a dist folder for you to distribute
	c:\path_to\chardet> c:\python31\python.exe setup.py bdist_wininst
	# the above creates a windows graphical installer
	
	''' ADDING your software to PyPI, the Python Package Index '''
	# step 1: register yourself. Step 2: register your software. Step 3: upload what setup.py made:
	c:\path_to\chardet> c:\python31\python.exe setup.py register sdist bdist_wininst upload
	# this puts you onto PyPI, at http://pypi.python.org/pypi/NAME where NAME from setup.py
''' DECORATORS '''
	@some_decorator								def some_function():
	def some_function():	is equivalent to 		pass
		pass							some_function = some_decorator(some_function)
	# decorators add extra functionality to functions
	def memoize(f):		# caches return values of function to avoid recalculating same thing
		cache = {}
		def helper(x):	# this is a lexical closure - it remembers vars in its scope (f & cache)
			if x not in cache:
				cache[x] = f(x)
			return cache[x]
		return helper
	def trace(f):		# prints when entering and exiting from a function
		def helper(x):
			call_str = "{0}({1})".format(f.__name__, x)
			print("Calling {0} ...".format(call_str))
			result = f(x)
			print("... returning from {0} = {1}".format(call_str, result))
			return result
		return helper
	@memoize		# when calling fib(), this decorator gets called first
	@trace			# then this one
	def fib(n):		# and then the actual fib()
		if n in (0, 1):
			return n
		else:
			return fib(n - 1) + fib(n - 2)