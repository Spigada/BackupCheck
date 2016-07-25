
# cob2sql.py
# Process cobol file definitions, generating mysql create table() statements.
#
# written by Chris Broughton 2016
#
# usage: python2 cob2sql.py

import re, sys, glob

tables = {}
tbl_stack = []
prefixes = {}
prefixes['current'] = []
max_len = 1

# types
k_text_type = 'varchar'
k_int_type = 'int'
k_dec_type = 'decimal'
k_bool_type = 'boolean'
k_datetime_type = 'datetime'
k_date_type = 'date'
k_timestamp_type = 'timestamp'
k_time_type = 'time'

# default values for types
defaults = {}
defaults[k_text_type] = "''"
defaults[k_int_type]  = "0"
defaults[k_dec_type]  = "0"
defaults[k_bool_type] = "0"
defaults[k_datetime_type] = "'1901-01-01 00:00:00'"
defaults[k_date_type]     = "'1901-01-01'"
defaults[k_time_type]     =            "'00:00:00'"
defaults[k_timestamp_type] = "current_timestamp on update current_timestamp"

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
			level, field_string = (int(f[:2]), f[3:])
			if level == 1 or (' occurs ' in field_string and not ' pic' in field_string):
				tbl_name = handle_table_line(level, field_string)
			else:
				tbl_name = get_tbl_for_field(level, field_string)
				m = re.match(r'([a-z_0-9-]+) +pic[ture]{0,4} +(.*)$', field_string)
				if m:
					var_name, pic = m.groups()
					names = [re.sub(r'^' + pre, '', var_name, count=1) for pre in prefixes['current']]
					var_name = min(names, key=len)		# remove longest matching prefix
					var_name = var_name.replace('-', '_')
					if not var_name.endswith(('_fill', 'filler')):	# ignore filler
						#print("{0} -> {1} is {2}".format(level, var_name, pic))
						if (len(var_name) > max_len):
							max_len = len(var_name)
						typ = convert(var_name, pic)
						add_field(tbl_name, var_name, typ)
				else:
					m = re.match(r'([a-z_0-9-]+) +values? +(.*)$', field_string)
					if m and level == 88:
						var_name, val = m.groups()
						names = [re.sub(r'^' + pre, '', var_name, count=1) for pre in prefixes['current']]
						var_name = min(names, key=len)		# remove longest matching prefix
						var_name = var_name.replace('-', '_')
						if (len(var_name) > max_len):
							max_len = len(var_name)
						fld_tbl = tables[tbl_name][-1][0]	# name of the last field added
						add_table(fld_tbl)
						vals = val.split(',')
						for v in vals:
							typ = tables[tbl_name][-1][1].split(' ', 1)[0]	# 1st word of type of last f added
							dflt = 'default {0}'.format(v)
							add_field(tables[tbl_name][-1][0], var_name, typ, as_is=True, options=dflt)
	
def handle_table_line(level, field_string):
	''' Handles a line that should create a new table '''
	global tbl_stack
	
	tbl_name = field_string.replace('-', '_')
	tbl_name = tbl_name.split(' ', 1)[0]	# first word
	tbl_name = re.sub(r'_rec$', r'', tbl_name, count=1)		# remove _rec suffix
	if level == 1:		# level 01 is top level, always a new table, clear the stack
		tbl_stack = [(level, tbl_name)]
		#print('clear table stack')
	elif level > tbl_stack[-1][0]:
		add_f_key(tbl_stack[-1][1], tbl_name+'_id', tbl_name, tbl_name+'_id')	# add foreign key reference to current table
		tbl_stack.append((level, tbl_name))
		#print('add {0} to stack'.format(level))
	
	add_table(tbl_name)
	return tbl_name

def get_tbl_for_field(level, field_string):
	''' gets correct table for given field '''
	global tbl_stack
	
	while level <= tbl_stack[-1][0]:
		x, y = tbl_stack.pop()
	return tbl_stack[-1][1]

def add_table(tbl, child=None):
	''' makes a new table, adding a foreign key reference to child '''
	global tables
	if not tbl in tables:
		tables[tbl] = []
		add_field(tbl, tbl+'_id', 'bigint', 'not null auto_increment primary key', as_is=True)
		#add_field(tbl, 'primary key(id)', '', as_is=True)
		add_field(tbl, 'created_by', k_text_type + '(100)')
		add_field(tbl, 'created_on', k_datetime_type)
		add_field(tbl, 'updated_by', k_text_type + '(100)')
		add_field(tbl, 'updated_on', k_datetime_type)
		add_field(tbl, 'rowversion', k_timestamp_type)

def add_f_key(tbl, fld, f_tbl, f_fld):
	add_field(tbl, fld+'_id', 'bigint', 'not null', as_is=True)
	add_field(tbl, 'foreign key({0}) references {1}({2})'.format(fld, f_tbl, f_fld), as_is=True)
	
def add_field(tbl, field, type, options='', as_is=False, add_not_null=True, add_default=True):
	''' adds field to table '''
	global tables
	if not as_is:
		if add_not_null:
			options += " not null"
		if add_default:
			if type.startswith(k_datetime_type):
				options += " default " + defaults[k_datetime_type]
			elif type.startswith(k_date_type):
				options += " default " + defaults[k_date_type]
			elif type.startswith(k_timestamp_type):
				options += " default " + defaults[k_timestamp_type]
			elif type.startswith(k_time_type):
				options += " default " + defaults[k_time_type]
			elif type.startswith(k_text_type):
				options += " default " + defaults[k_text_type]
			elif type.startswith(k_bool_type):
				options += " default " + defaults[k_bool_type]
			else:
				options += " default 0"
	if options:
		type = "{0:<14} {1}".format(type, options.lstrip())
	tables[tbl].append((field, type))

def convert(name, clause):
	''' converts picture clause to sql type '''
	type = k_text_type + '(100)'
	m = re.search(r'(.)\((\d+)\)', clause)		# 9(3), x(3)
	print('converting {0} {1}'.format(name, clause))
	if m:
		ch, count = m.groups()
		count = int(count)
		# call self replacing x(3) with xxx
		return convert(name, clause[0:m.start()] + ch * count + clause[m.end():])
		
	# ...-flg     pic x       is boolean
	if clause.count('x') == 1 and clause.count('9') == 0 and name.endswith('_flg'):
		type = k_bool_type
	if '9' in clause and not 'x' in clause:
		if 'v' in clause:
			type = k_dec_type
		elif clause.count('9') in range(6,8+1) and 'dat' in name:
			type = k_date_type
		elif clause.count('9') == 4 and 'tim' in name:
			type = k_time_type
		else:
			type = k_int_type
	return type

def on_line_read(file, line):
	''' Performed when one line of file is read. '''
	global prefixes
	
	line.replace('\r', '')		# nuke carriage returns
	if (len(line) < 7):			# too short, skip
		return False
	elif (line[6] == '$'):		# xfd, skip
		return False
	elif (line[6] == '*'):		# comment line, skip
		if line.startswith('dict  * PRE'):	# but first save prefix for later
			prefixes['current'].append(line.rsplit(None, 1)[1].lower() + '-')
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

def printTables(tbls):
	''' prettyprints tables '''
	for t in tbls:
		tbl_fields = []
		print("create table " + t + "(")
		for f in tbls[t]:
			#str = "{0:<30} {1}"
			str = "{0:<" + "{0}".format(max_len) + "} {1}"
			tbl_fields.append("    " + str.format(f[0], f[1]).rstrip() )
		print(",\n".join(tbl_fields))
		print(k_end_table)
		print('-- end of table ' + t)
		print('')
	
# or possibly use sys.argv
#with fileinput.input() as input:
for arg in sys.argv[1:]:
	for fil in glob.glob(arg):
		with open(fil, mode='r') as input:	# py2
		#with open(fil, mode='r', encoding='utf-8') as input:	# py3
		#for arg in input:
			read_file(input)
printTables(tables)
print("")
