
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
			if level == 1: #or ' occurs ' in field_string:
				tbl_name = handle_table_line(level, field_string)
			else:
				m = re.match(r'([a-z0-9-]+) +pic[ture]{0,4} +(.*)$', field_string)
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
	
def handle_table_line(level, field_string):
	''' Handles a line that should create a new table '''
	global tbl_stack
	
	tbl_name = field_string.replace('-', '_')
	tbl_name = re.sub(r'_rec$', r'', tbl_name, count=1)		# remove _rec suffix
	# started on using a table stack for occurs... not sure if it's worth it.
	#if level == 1:		# level 01 is top level
	#	tbl_stack = [(level, tbl_name)]
		#print('clear table stack')
	#elif level > tbl_stack[-1][0]:		# if field is part of current table
	#	tbl_stack.append((level, tbl_name))
		#print('add {0} to stack'.format(level))
	
	add_table(tbl_name)
	return tbl_name

def add_table(tbl):
	''' makes a new table '''
	global tables
	tables[tbl] = []
	add_field(tbl, tbl+'_id', 'bigint', 'not null auto_increment primary key', as_is=True)
	#add_field(tbl, 'primary key(id)', '', as_is=True)
	add_field(tbl, 'created_by', k_text_type + '(255)')
	add_field(tbl, 'created_on', k_datetime_type)
	add_field(tbl, 'updated_by', k_text_type + '(255)')
	add_field(tbl, 'updated_on', k_datetime_type)
	add_field(tbl, 'rowversion', k_timestamp_type)
	
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
	type = k_text_type + '(255)'
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
			tpye = k_time_type
		else:
			type = k_int_type
	return type

def on_line_read(file, line):
	''' Performed when one line of file is read. '''
	global prefixes
	
	line.replace('\r', '')		# nuke carriage returns
	if (len(line) < 7):			# too short, skip
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
