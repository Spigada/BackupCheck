
# cob2sql.py
# Process cobol file definitions, generating mysql create table() statements.
#
# written by Chris Broughton 2016
#
# usage: python2 cob2sql.py

import re, sys, glob

tables = {}
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
	global tables, max_len
	tbl_name = ''
	
	text = text.replace('\n', '')	# nuke newlines
	fields = text.split('.')
	for f in fields:
		f = f[7:]				# nuke comments area
		f = f.lstrip().lower()	# and leading spaces, convert to lowercase
		
		m = re.match(r'^\d\d ', f)		# if first 3 characters are digit digit space
		if m:
			level, field_string = (f[:2], f[3:])
			if level == '01':
				tbl_name = field_string.replace('-', '_')
				add_table(tbl_name)
			m = re.match(r'([a-z0-9-]+) +pic[ture]{0,4} +(.*)', field_string)
			if m:
				var_name, pic = m.groups()
				var_name = var_name.replace('-', '_')
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
		else
			type = 'int'
	return type

def on_line_read(file, line):
	''' Performed when one line of file is read. '''
	line.replace('\r', '')		# nuke carriage returns
	if (len(line) < 7):			# too short, skip
		return False
	elif (line[6] == '*'):		# comment line, skip
		return False
	return True

		
def on_default_log_line_read(file, line):
	''' Ignore lines until we figure out what kind of log we're parsing based on Subject. '''
	global file_type, server_name, company_name
	m = re.search(r'^Subject: (.*)$', line)	# get type of file from email header subject line
	if m:
		subj = m.group(1)
		if subj:
			m = re.search(r'^(.*?) log activity from (.*?):(.*)', subj, re.I)
			if m:
				(type, server_name, company_name) = m.groups()
				if type == 'STANDALONE':
					file_type = k_standalone_log
				elif type == 'HTML':
					file_type = k_html_log
			#elif (re.search(r'^SamcoStor', subj, re.I)):
			elif subj.lower().startswith('samcostor'):
				server_name = 'SamcoStor'
				file_type = k_samcoStor_log
	return k_ignore_me	# no specific backup info yet

def on_samcoStor_log_line_read(file, line):
	''' Parses samcostor log html table. '''
	global start_date, errors_found, num_processed, num_backups_done, stor_hash
	prt_line = ''
	if re.search(stor_ignore_client_pattern, line, re.I):
		return k_ignore_me
	
	# get table row data values
	cell = r'<td.*?>(.*?)<\/td>'
	pattern = r'^<tr>' + cell + cell + cell + cell + cell + cell + cell + cell
	m = re.search(pattern, line)
	if m:
		status, x, customer, client, y, z, a, a_date = m.groups()
		if start_date == '':
			start_date = a_date
		key = customer + client
		# don't care about certain customers, ie. 'samcoinhouse'
		if re.search(stor_ignore_cust_pattern, customer, re.I):
			return k_ignore_me

		if re.search(stor_fail_pattern, status, re.I):
			# only report if not done already (1 error per key)
			if not stor_hash[key]:
				if errors_found == 0:
					prt_line += '\n'
				prt_line += "{0} - SamcoStor ({1} -> {2})\n".format(status, customer, client)
				errors_found += 1
				num_processed += 1
				stor_hash[key] = status
		elif re.search(stor_success_pattern, status, re.I):
				# only print success if it had previously failed
				if stor_hash[key]:
					if re.search(stor_fail_pattern, stor_hash[key], re.I):
						if errors_found == 0:
							prt_line += "\n"
						prt_line += "{0} - SamcoStor ({1} -> {2})\n".format(status, customer, client)
						errors_found -= 1
						num_backups_done += 1
				else:
					num_processed += 1
					num_backups_done += 1
				stor_hash[key] = status
	if prt_line:
		line = prt_line
		return k_save_me
	return k_ignore_me

def on_html_log_line_read(file, line):
	''' Parses html backup log. '''
	global file_result, errors_found, start_date, num_backups_done, num_processed, company_id, \
			backup_started, company_path, incremental_ignore
	td_pat = r'(?:<\/td> ?<td>| )'
	# yo dawg, I heard you like parsing reports, so I added
	# parsing your own report so you can report what you reported
	if re.search(r'FAIL - ', line, re.I):
		if errors_found == 0:
			file_result[k_current] += "\n"
		file_result[k_current] += strip_tags(line)
		errors_found += 1
		return k_save_me
	
	# add output of own report to grand totals
	m = re.search(r' success: (\d+)(?: out of (\d+))?(?:.*started ((?:Mo|T|W|Fr|Sa|Su).*))?', line, re.I)
	if m:
		prev_backups_done = int(m.group(1))
		prev_processed = prev_backups_done
		if len(m.groups()) > 1 and m.group(2) != None:
			prev_processed = int(m.group(2))
		if start_date == '' and len(m.groups()) > 2:
			start_date = m.group(3) if m.group(3) else ''
		num_backups_done += prev_backups_done
		num_processed += prev_processed
		return k_save_me
	
	# end of backup section (tested first because it's more specific)
	if re.search(r'(?:<h2>)?.*--(?: ?Backup|Rsync) finished', line, re.I):
		company_id = ''
		backup_started = False
		if errors_found > 0:
			num_backups_done -= 1
		return k_ignore_me
	else:
		# start of backup section
		m = re.search(r'(?:<h2>)?.*--(?:Backup|Rsync) (.*?):/(.*(?:/.*)?)/? ((?:Mo|T|W|Fr|Sa|Su).*)--', line, re.I)
		if m:
			company_id = m.group(1)
			company_path = m.group(2)
			if start_date == '':
				start_date = m.group(3) if m.group(3) else ''
			errors_found = 0
			num_processed += 1
			num_backups_done += 1
			backup_started = True
			return k_ignore_me
		else:
			# drive space used
			m = re.search(r'{0}(\d?\d\d)%{1}(.*)(?:</td>)?'.format(td_pat, td_pat), line, re.I)
			if m:
				pct_full = int(m.group(1))
				mount = m.group(2)
				prt_disk_full = "{0} is {1}% full".format(mount, pct_full)
				# remove tags from output
				prt_disk_full = strip_tags(prt_disk_full)
				if pct_full >= k_disk_full_level:
					file_result[k_current] += "\n{0}\n".format(prt_disk_full)
			# start of incremental spam inside backup
			elif re.search(k_spam_pattern, line, re.I):
				incremental_ignore = True
				return k_ignore_me
			# end of incremental spam
			elif re.search(k_spam_end_pattern, line, re.I):
				incremental_ignore = False
				return k_ignore_me
			# ignore lines like 'file vanished' etc.
			elif re.search(k_html_ignore_pattern, line, re.I):
				return k_ignore_me
			# ignore the 2nd line of an h3 that had a line break in it
			elif not re.search(r'<h3>', line, re.I) and re.search(r'</h3>', line, re.I):
				return k_ignore_me
			# ignore empty lines
			elif re.search(r'^$', line):
				return k_ignore_me
	
	# report non-ignored lines
	if backup_started and not incremental_ignore:
		# report the error
		prt_company = company_id or company_name
		if prt_company == 'backupsrv':
			prt_company = company_path
		if errors_found:
			file_result[k_current] += "\n"
		file_result[k_current] += strip_tags("FAIL - {0}: {1} - {2}".format(server_name, prt_company, line))
		errors_found += 1
	else:
		return k_ignore_me
	return k_save_me

def read_file(logFile):
	''' Reads files. '''
	global errors_found
	errors_found = 0
	
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
