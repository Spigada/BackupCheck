
# cob2sql.py
# Process cobol file definitions, generating mysql create table() statements.
#
# written by Chris Broughton 2016
#
# usage: python2 cob2sql.py

import re, sys, glob

tables = {}
prefixes = {}
prefixes['current'] = []
max_len = 1

# types
k_text_type = 'varchar'
k_int_type = 'int'
k_dec_type = 'decimal'
k_bool_type = 'boolean'
k_date_type = 'datetime'
k_time_type = 'timestamp'

# default values for types
k_int = "0"
k_str = "''"
k_date = "'1901-01-01 00:00:00'"

k_create_table = "\ncreate table "
k_table_common = """(
    id          bigint auto_increment,
	created_by  varchar(3),
	created_on  datetime not null default k_date,
	updated_by  varchar(3),
	updated_on  datetime not null default k_date,
	rowversion  timestamp default current_timestamp on update current_timestamp,
"""
k_end_table = ")engine=innodb default charset=utf8;"

def debug():
	import pdb; pdb.set_trace()	 #break to DEBUG
	
def trace(f):
	''' prints when entering and exiting a function '''
	@wraps(f)
	def helper(*args, **kwargs):
		call_str = "{0}(1)".format(f.__name__)
		print("  Calling {0} ...".format(call_str))
		result = f(*args, **kwargs)
		print("  ... returning from {0} = {1}".format(call_str, result))
		return result
	return helper



def on_file_read(file, text):
	''' Performed after every file is read completely. '''
	global tables, prefixes, max_len
	tbl_name = ''
	
	text = text.replace('\n', '')	# nuke newlines
	fields = text.split('.')
	''' 03 PS-DRW-PRIME-USR-ID              PIC X(3).
	    () (field string                           )
	 level (var name          )       pic clause(  )'''
	for f in fields:
		f = f[7:]				# nuke comments area
		f = f.lstrip().lower()	# and leading spaces, convert to lowercase
		
		m = re.match(r'^\d\d ', f)		# if first 3 characters are digit digit space
		if m:
			level, field_string = (f[:2], f[3:])
			if level == '01':
				tbl_name = field_string.replace('-', '_')
				tbl_name = re.sub(r'_rec$', r'', tbl_name)		# remove _rec suffix
				prefixes[tbl_name] = prefixes['current']
				prefixes['current'] = []
				add_table(tbl_name)
			m = re.match(r'([a-z0-9-]+) +pic[ture]{0,4} +(.*)', field_string)
			if m:
				var_name, pic = m.groups()
				var_name = var_name.replace('-', '_')
				               # remove prefix
				print("{0} -> {1} is {2}".format(level, var_name, pic))
				if (len(var_name) > max_len):
					max_len = len(var_name)
				typ = convert(var_name, pic)
				add_field(tbl_name, var_name, typ)
	printTables(tables)
	
def printTables(tbls):
	''' prettyprints tables '''
	for t in tbls:
		print("create table " + t + "(")
		for f in tbls[t]:
			#print(f)
			#str = "{:<" + "{}".format(max_len) + "} {}"	# '{:<max_len} {}'
			str = "{0:<30} {1}"
			print("    " + str.format(f[0], f[1]))
		print(k_end_table)
	
def add_table(tbl):
	''' makes a new table '''
	global tables
	tables[tbl] = []
	add_field(tbl, 'id', 'bigint not null auto_increment', add_default=False)
	add_field(tbl, 'created_by', 'varchar(3)')
	add_field(tbl, 'created_on', 'datetime')
	add_field(tbl, 'updated_by', 'varchar(3)')
	add_field(tbl, 'updated_on', 'datetime')
	add_field(tbl, 'rowversion', 'timestamp')
	
def add_field(tbl, field, type, add_default=True):
	''' adds field to table '''
	global tables
	if add_default:
		if type == 'datetime':
			type += " not null default '1990-01-01 00:00:00'"
		elif type == 'timestamp':
			type += " not null default current_timestamp on update current_timestamp"
		elif type.startswith('varchar'):
			type += " not null default ''"
		elif type == 'boolean':
			type += " not null default 0"
		else:
			type += " not null default 0"
	tables[tbl].append((field, type))

def convert(name, clause):
	''' converts picture clause to sql type '''
	type = 'varchar(255)'
	m = re.search(r'(.)\((\d+)\)', clause)		# 9(3), x(3)
	if m:
		ch, count = m.groups()
		count = int(count)
		# call self replacing x(3) with xxx
		return convert(name, clause[0:m.start()] + ch * count + clause[m.end():0])
	if clause.count('x') == 1 and clause.count('9') == 0 and name.endswith('_flg'):
		type = 'boolean'
	if '9' in clause and not 'x' in clause:
		if 'v' in clause:
			type = 'decimal'
		else:
			type = 'int'
	return type

def on_line_read(file, line):
	''' Performed when one line of file is read. '''
	global prefixes
	
	line.replace('\r', '')		# nuke carriage returns
	if (len(line) < 7):			# too short, skip
		return False
	elif (line[6] == '*'):		# comment line, skip
		if line.startswith('dict  * PRE'):	# but first save prefix for later
			prefixes['current'].append(line.rsplit(maxsplit=1)[1])
		return False
	return True

def read_file(logFile):
	''' Reads files. '''
	f_contents = ''
	#with open(logFile, encoding='utf-8') as f:
	for line in logFile:
		if on_line_read(logFile.name, line):
			f_contents += line
	on_file_read(logFile.name, f_contents)


# or possibly use sys.argv
#with fileinput.input() as input:
for arg in sys.argv[1:]:
	for fil in glob.glob(arg):
		with open(fil, mode='r') as input:	# py2
		#with open(fil, mode='r', encoding='utf-8') as input:	# py3
		#for arg in input:
			read_file(input)


'''
for key in sorted(file_result, key=time.mktime):
	# extra line if starting a new day
	#the_time = time.localtime(key)
	
	#key_day = key.tm_mday if key.tm_mday >= 1 else -1
	key_day = key.split()[2]
	if last_day != key_day:
		print("")
	last_day = key_day
	
	print("    {0}{1}".format(key, file_result[key]))
'''
print("")
