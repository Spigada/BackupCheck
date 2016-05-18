
# backupCheckAll.py
# Process backup files, looking for backup failures.
# In order to email failures and extra info to IT dept.
#
# look for company ID, and backup success
#
# written by Chris Broughton 2016
#
# usage: python2 backupCheckAll.py

import fileinput, glob, sys
import re
import time
from functools import wraps

global errors_found, num_processed, num_backups_done, total_processed, total_stor_processed, \
total_backups_done, total_stor_backups_done, server_name, company_name, company_id, company_path, \
start_date, backup_started, incremental_ignore, file_type, file_result, k_current, last_day, now

stor_hash = {}	# key is customer+client, value is status


weekday_name = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')
month_name = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 
			'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

k_disk_full_level = 90			# disk % used warning level
k_save_me = 1					# keep line value for another pass if desired
k_ignore_me = -1				# ignore this line
k_html_log = 'htmllog'			# html log backup type
k_standalone_log = 'standalone'	# standalone log backup type
k_samcoStor_log = 'samcostor'	# SamcoStor backup type


errors_found = 0				# non-zero if errors found
num_processed = 0
num_backups_done = 0			# number of successful backups in file read
total_processed = 0
total_stor_processed = 0
total_backups_done = 0			# total across all non-stor files read
total_stor_backups_done = 0		# total SamcoStor
server_name = ''
company_name = ''
company_id = ''
company_path = ''
start_date = ''
backup_started = False			# whether backup is processing or not
incremental_ignore = False		# ignore spam
file_type = ''					# what kind of file are we parsing

# errors reported that are not considered failures
k_html_ignore_pattern = r'file(?: ha)?s vanished|'\
                        r'stty: standard input: Invalid argument|'\
					    r'mkstemp|'\
					    r'00=00=00=00=00='
# spam incoming
k_spam_pattern = r'receiving(?: incremental)? file list'
# end of spam
k_spam_end_pattern = r'total size is .* speedup is'

file_result = {}	# key is start date (epoch time), value is what to print
k_current = '999'	# current file key before date is known
last_day = -1 		# keeps track of last date printed
now = time.time()	# time when script started

stor_hash = {}	# key is customer+client, value is status
stor_fail_pattern = r'FAILED|MISSED'
stor_success_pattern = r'SUCCESS|PARTIAL'
stor_ignore_cust_pattern = r'SAMCOINHOUSE|Default Customer'
stor_ignore_client_pattern = r'METADATA_BACKUP'

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

def strip_tags(txt):
	''' Removes tags from string. '''
	return re.sub(r'<.*?>', r'', txt)

def on_file_read(file, text_ref):
	''' Performed after every file is read completely. '''
	global total_processed, total_backups_done, num_backups_done, file_result, \
			total_stor_backups_done, total_stor_processed
	if (incremental_ignore):
		# if we've missed the end marker for incremental spam,
		# something went wrong with the rsync.
		file_result[k_current] += 'FAIL - missed incremental rsync end marker'
		num_backups_done -= 1
		
	# SamcStor lines were buffered instead of printed out line by line
	# so post-process and print them out now.
	if (file_type == k_samcoStor_log):
		# remove any misses or fails that were subsequently followed by a success
		for m in re.finditer(r'(?:{0}) - SamcoStor \((.*?)\)'.format(stor_success_pattern), text_ref):
			text_ref = re.sub(r'\n.*{0}.*\n'.format(m.group(1)), r'\n', text_ref) # nuke any client lines matching a success
		file_result[k_current] += strip_tags(text_ref)
		total_stor_processed += num_processed
		total_stor_backups_done += num_backups_done
	else:
		total_processed += num_processed
		total_backups_done += num_backups_done
		
	str = '    {0} success: {1}'.format(server_name, num_backups_done)
	if (num_backups_done < num_processed):
		str += ' out of {0}, details:'.format(num_processed)
	file_result[k_current] = " - {0} {1}{2}".format(server_name, str, file_result[k_current])
	
	#debug()
	file_key = time.asctime()
	# backup date format: weekday mon day hh:mm:ss PDT yyyy
	m = re.search(r'(...) (...) +(\d+) (\d+):(\d\d):(\d\d) ... (\d{4})', start_date)
	if m:
		(wday, mon, day, hh, mm, ss, yyyy) = m.groups()
		file_key = time.asctime(time.strptime("{0}{1}{2}{3}{4}{5}{6}".format(wday, mon, day, hh, mm, ss, yyyy), "%a%b%d%H%M%S%Y"))
	# samcostor date format: weekday day mon yyyy, hh:mm:ss pm
	m = re.search(r'(...) +(\d+) +(...) (\d{4}), +(\d\d):(\d\d):(\d\d) (..)', start_date)
	if m:
		(wday, day, mon, yyyy, hh, mm, ss, ampm) = m.groups()
		if ampm == 'pm':
			hh += 12
		file_key = time.asctime(time.strptime("{0}{1}{2}{3}{4}{5}{6}".format(wday, mon, day, hh, mm, ss, yyyy), "%a%b%d%H%M%S%Y"))
	while file_key in file_result:
		file_key += 1
	file_result[file_key] = file_result[k_current]
	del file_result[k_current]
		

def on_line_read(file, line):
	''' Performed when one line of file is read. '''
	#re.sub(r'\r', r'', line)		# nuke carriage returns
	line.replace('\r', '')
	if ((file_type == k_html_log) or (file_type == k_standalone_log)):
		return on_html_log_line_read(file, line)
	elif (file_type == k_samcoStor_log):
		return on_samcoStor_log_line_read(file, line)
	else:
		return on_default_log_line_read(file, line)

		
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
	global file_type, num_backups_done, num_processed, server_name, company_name, company_id, \
			start_date, backup_started, errors_found, file_result, stor_hash
	file_type = ''
	num_backups_done = 0
	num_processed = 0
	server_name = ''
	company_name = ''
	company_id = ''
	start_date = ''
	backup_started = False
	errors_found = 0
	file_result[k_current] = ''
	stor_hash = {}
	
	# shorten filename printed
	#filepath = logFile
	#re.sub(r'^.* log activity (.*?) - .*', r'\1', filepath, re.I)
	
	f_contents = ''
	#with open(logFile, encoding='utf-8') as f:
	for line in logFile:
		if on_line_read(logFile.name, line) != k_ignore_me:
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

final_summary = '=== Total successful BackupSrv backups: {0} out of {1}'\
				.format(total_backups_done, total_processed)
print(final_summary)
final_summary = '=== Total successful SamcoStor backups: {0} out of {1}'\
				.format(total_stor_backups_done, total_stor_processed)
print(final_summary)

for key in sorted(file_result, key=time.mktime):
	# extra line if starting a new day
	#the_time = time.localtime(key)
	
	#key_day = key.tm_mday if key.tm_mday >= 1 else -1
	key_day = key.split()[2]
	if last_day != key_day:
		print("")
	last_day = key_day
	
	print("    {0}{1}".format(key, file_result[key]))

print("")
