#!/usr/bin/perl 
use strict;
use warnings;
use Time::Local;

# backupCheckAll.pl
# Process a backup file, looking for backup failures.
# to email failures and extra info to IT dept
# 
# look for company ID, and backup success
#
# written by Chris Broughton 2015
#
# usage: perl backupCheckAll.pl [file ...] 

{	# start-block for 'global' vars (not indented)
my @weekdayNam = qw(Sun Mon Tue Wed Thu Fri Sat);
my %monthNam = (Jan => 1, Feb => 2, Mar => 3, Apr => 4, May => 5, Jun => 6, 
               Jul => 7, Aug => 8, Sep => 9, Oct => 10, Nov => 11, Dec => 12);

my $kDiskFullLevel = 90;	# disk % used warning level
my $kSaveMe = 1;	# keep line value for another pass if desired
my $kIgnoreMe = -1;	# ignore line value
my $kHtmlLog = 'htmllog';	# html log backup type
my $kStandaloneLog = 'standalone';	# standalone log backup type
my $kSamcoStorLog = 'samcostor';	# SamcoStor backup type


my $errorsFound = 0;	# non-zero if errors found
my $numProcessed = 0;
my $numBackupsDone = 0;	# number of successful backups in file read
my $totalProcessed = 0;
my $totalStorProcessed = 0;
my $totalBackupsDone = 0;	# total across all non-stor files read
my $totalStorBackupsDone = 0;	# total samcoStor 
my $serverName = '';
my $companyName = '';
my $companyID = '';
my $companyPath = '';
my $startDate = '';
my $backupStarted = 0;	# whether backup is processing or not
my $incrementalIgnore = 0;	# ignore spam
my $fileType = '';	# what kind of file are we parsing

# errors reported that aren't considered failures
my $kHtmlIgnorePattern = 'file(?: ha)?s vanished|'
                       . 'stty: standard input: Invalid argument|'
                       . 'mkstemp|'
                       . '00=00=00=00=00=';

# spam incoming
my $kSpamPattern = 'receiving(?: incremental)? file list';
# end of spam
my $kSpamEndPattern = 'total size is .* speedup is';

my %fileResult = ();	# key is start date (epoch time), value is what to print
my $kCurrent = 999; 	# current file key before date is known
my $lastDay = -1;	# keeps track of last date printed
my $now = time();	# time when script started

my %storHash = ();	# key is customer+client, value is status
my $storFailPattern = 'FAILED|MISSED';
my $storSuccessPattern = 'SUCCESS|PARTIAL';
my $storIgnoreCustPattern = 'SAMCOINHOUSE|Default Customer';
my $storIgnoreClientPattern = 'METADATA_BACKUP';

readFiles();
my $finalSummary = "=== Total successful Backup Server backups: $totalBackupsDone";
#if ($totalBackupsDone < $totalProcessed) {
	$finalSummary .= " out of $totalProcessed";
#}
print "\n$finalSummary.\n";
$finalSummary = "=== Total successful SamcoStor backups: $totalStorBackupsDone";
#if ($totalStorBackupsDone < $totalStorProcessed) {
	$finalSummary .= " out of $totalStorProcessed";
#}
print "$finalSummary.\n";

foreach my $key (sort keys %fileResult) {
	# extra line if starting a new day
	my $time = localtime($key);
	print "\n" if $lastDay ne (localtime($key))[3];
	$lastDay = (localtime($key))[3];
	
	print "    " . $time;
	print "$fileResult{$key}\n";
}

print "\n";


# onFileRead(file, textRef)
# performed after every file is read completely
sub onFileRead {
	my $file = shift;
	my $textRef = shift;	
	
	# if we missed the end marker for incremental spam,
	# something went wrong with the rsync.
	if ($incrementalIgnore > 0) {
		$fileResult{$kCurrent} .= "FAIL - missed incremental rsync end marker\n";
		$numBackupsDone--;
	}
	
	# SamcoStor lines were buffered instead of printed out line by line
	# so post-process and print them out now
	if ($fileType eq $kSamcoStorLog) {
		# remove any misses or fails that were subsequently followed by a success
		while ($$textRef =~ /(?:$storSuccessPattern) - SamcoStor \((.*?)\)/g) {
			$$textRef =~ s/\n.*$1.*\n/\n/;	# nuke any client lines matching a success
		}
		$fileResult{$kCurrent} .= stripTags($$textRef);
		
		$totalStorProcessed += $numProcessed;
		$totalStorBackupsDone += $numBackupsDone;
	} else {
		$totalProcessed += $numProcessed;
		$totalBackupsDone += $numBackupsDone;
	}
	my $successStr = "success: $numBackupsDone";
	if ($numBackupsDone < $numProcessed) {
		$successStr .= " out of $numProcessed, details:";
	}
	#$fileResult{$kCurrent} .= stripTags(", started " . $startDate) if ($startDate ne '');
	#$fileResult{$kCurrent} .= "\n";
	
	# PREPEND servername
	$fileResult{$kCurrent} = " - $serverName $successStr" . $fileResult{$kCurrent};
	
	my $fileKey = time();
	# backup date format
	if ($startDate =~ /(...) (...) +(\d+) (\d+):(\d\d):(\d\d) ... (\d{4})/) {
		my $wday = $1;	# weekday mon day hh:mm:ss PDT yyyy
		my $mon = $monthNam{$2} - 1;
		my $day = $3;
		my $hh = $4;
		my $mm = $5;
		my $ss = $6;
		my $yyyy = $7;
		$fileKey = timelocal($ss, $mm, $hh, $day, $mon, $yyyy);
	}
	# samcostor date format
	if ($startDate =~ /(...) +(\d+) +(...) (\d{4}), +(\d\d):(\d\d):(\d\d) (..)/) {
		my $wday = $1;	# weekday day mon yyyy, hh:mm:ss pm
		my $day = $2;
		my $mon = $monthNam{$3} - 1;
		my $yyyy = $4;
		my $hh = $5;
		my $mm = $6;
		my $ss = $7;
		$hh += 12 if ($8 eq 'pm');
		$fileKey = timelocal($ss, $mm, $hh, $day, $mon, $yyyy);
	}
	# increment key if it already exists
	while (exists $fileResult{$fileKey}){
		$fileKey++;
	}
	
	$fileResult{$fileKey} = $fileResult{$kCurrent};
	delete $fileResult{$kCurrent};
	
#	checkCustomInit($textRef);
}

# onLineRead(file, line)
# performed when one line of file is read
sub onLineRead {
	my $file = shift;
	my $line = shift;
	
	$$line =~ s/\r//g;	# nuke carriage returns

	if (($fileType eq $kHtmlLog) || ($fileType eq $kStandaloneLog)) {
		return onHTMLLogLineRead($file, $$line);
	} elsif ($fileType eq $kSamcoStorLog) {
		return onSamcoStorLogLineRead($file, \$$line);
	} else {
		return onDefaultLineRead($file, $$line);
	}
}

# onDefaultLineRead(file, line)
# try to find what kind of log we're parsing based on subject
sub onDefaultLineRead {
	my $file = shift;
	my $line = shift;
	
	# get type of file from email header subject line
	if ($line =~ /^Subject: (.*)$/) {
		my $subj = $1;
		$serverName = $subj;
		if ($subj =~ /^STANDALONE log activity from (.*?):(.*)/i) {
			$serverName = $1;
			$companyName = $2;
			$fileType = $kStandaloneLog;
		} elsif ($subj =~ /^HTML log activity from (.*?):(.*)/i) {
			$serverName = $1;
			$companyName = $2;
			$fileType = $kHtmlLog;
		} elsif ($subj =~ /log activity from (.*?):(.*)/i) {
			$serverName = $1;
			$companyName = $2;
			$fileType = $kStandaloneLog;
		} elsif ($subj =~ /^SamcoStor/i) {
			$serverName = 'SamcoStor';
			$fileType = $kSamcoStorLog;
		}
	}
	
	# no specific backup info yet
	return $kIgnoreMe;
}

# onSamcoStorLogLineRead(file, line)
# parse samcostor log html table
sub onSamcoStorLogLineRead {
	my $file = shift;
	my $line = shift;
	my $prtLine = '';

	# don't care about metadata lines
	if ($$line =~ /METADATA_BACKUP/i) {
		return $kIgnoreMe;
	}
	
	# get table row data values
	my $cell = '<td.*?>(.*?)<\/td>';
	my $pattern = '^<tr>'.$cell.$cell.$cell.$cell.$cell.$cell.$cell.$cell;
	if ($$line =~ /$pattern/i) {
		my $status = $1;
		my $customer = $3;
		my $client = $4;
		$startDate = $8 if $startDate eq '';
		my $key = $customer . $client;
		# don't care about certain customers ie. 'samcoinhouse'
		if ($customer =~ /$storIgnoreCustPattern/i) {
			return $kIgnoreMe;
		}
		
		if ($status =~ /$storFailPattern/i) {
			# only report if not done already (1 error per key)
			if (!defined $storHash{$key}) {
				$prtLine .= "\n" if ($errorsFound == 0);
				$prtLine .= "$status - SamcoStor ($customer -> $client)\n";
				$errorsFound++;
				$numProcessed++;
				$storHash{$key} = $status;
			}
		} elsif ($status =~ /$storSuccessPattern/i) {
			# only print success if had previously failed
			if (defined $storHash{$key}) {
				if ($storHash{$key} =~ /$storFailPattern/i) {
					$prtLine .= "\n" if ($errorsFound == 0);
					$prtLine .= "$status - SamcoStor ($customer -> $client)\n";
					$errorsFound--;
					$numBackupsDone++;
				}
			} else {
				$numProcessed++;
				$numBackupsDone++;
			}
			$storHash{$key} = $status;
		}
	}
	if ($prtLine ne '') {
		$$line = $prtLine;
		return $kSaveMe;
	}
	return $kIgnoreMe;
}

# on HTMLLogLineRead(file, line)
# parses html backup log
sub onHTMLLogLineRead {
	my $file = shift;
	my $line = shift;

	my $tdPat = '(?:<\/td> ?<td>| )';
	# yo dawg, I heard you like parsing reports, so I added
	# parsing your own report so you can report what you reported
	if ($line =~ /FAIL - /i) {
		$fileResult{$kCurrent} .= "\n" if ($errorsFound == 0);
		$fileResult{$kCurrent} .= stripTags($line);
		$errorsFound++;
		return $kSaveMe;
	}
	# add output of own report to grand totals
	if ($line =~ / success: (\d+)(?: out of (\d+))?(?:.*started ((?:Mo|T|W|Fr|Sa|Su).*))?/i) {
		my $prevBackupsDone = $1;
		my $prevProcessed = $prevBackupsDone;
		$prevProcessed = $2 if defined($2);
		$startDate = $3 if (defined($3) && ($startDate eq ''));
		$numBackupsDone += $prevBackupsDone;
		$numProcessed += $prevProcessed;
		return $kSaveMe;
	}
	
	# end of backup section tested first because its more specific
	if ($line =~ /(?:<h2>)?.*--(?: ?Backup|Rsync) [fF]inished/i) {
		$companyID = '';
		$backupStarted = 0;
		if ($errorsFound > 0) {
			$numBackupsDone--;
			#print "Fail count: $errorsFound\n";
		}
		return $kIgnoreMe;
	# start of backup section
	} elsif ($line =~ /(?:<h2>)?.*--(?:Backup|Rsync) (.*?):\/(.*(?:\/.*)?)\/? ((?:Mo|T|W|Fr|Sa|Su).*)--/i) {
		$companyID = $1;
		$companyPath = $2;
		$startDate = $3 if ($startDate eq '');
		$errorsFound = 0;
		$numProcessed++;
		$numBackupsDone++;
		$backupStarted = 1;
		return $kIgnoreMe;
	# drive space used
	} elsif ($line =~ /$tdPat(\d?\d\d)%$tdPat(.*)(?:<\/td>)?/i) {
		my $pctFull = $1;
		my $mount = $2;
		my $prtDiskFull = "$mount is $pctFull% full";
		# remove tags from output
		$prtDiskFull =~ s/<.*?>//g;
		if ($pctFull >= $kDiskFullLevel) {
			$fileResult{$kCurrent} .= "\n$prtDiskFull\n";
		}
	# start of incremental spam inside backup
	} elsif ($line =~ /$kSpamPattern/i) {
		$incrementalIgnore = 1;
		return $kIgnoreMe;
	# end of incremental spam
	} elsif ($line =~ /$kSpamEndPattern/i) {
		$incrementalIgnore = 0;
		return $kIgnoreMe;
	# ignore lines 'files vanished' or 'file has vanished'
	} elsif ($line =~ /$kHtmlIgnorePattern/i) {
		return $kIgnoreMe;
	# ignore the second line of an h3 that had a line break in it
	} elsif (($line !~ /<h3>/i) && ($line =~ /<\/h3>/i)) {
		return $kIgnoreMe;
	# ignore empty lines
	} elsif ($line =~ /^$/) {
		return $kIgnoreMe;
	}

	# report non-ignored lines
	if (($backupStarted > 0) && ($incrementalIgnore < 1)) {
		# report the error
		my $prtCompany = $companyName;
		$prtCompany = $companyID if ($companyID ne '');
		$prtCompany = $companyPath if ($prtCompany eq 'backupsrv');
		$fileResult{$kCurrent} .= "\n" if ($errorsFound == 0);
		$fileResult{$kCurrent} .= stripTags("FAIL - $serverName: $prtCompany - $line");
		$errorsFound++;
	} else {
		return $kIgnoreMe;	# ignore
	}
	return $kSaveMe;
}

sub stripTags {
	my $txt = shift;
	$txt =~ s/<.*?>//gs;
	return $txt;
}

# read all files passed to program from commandline
sub readFiles {
	for my $file (@ARGV) {
		$fileType = '';
		$numBackupsDone = 0;
		$numProcessed = 0;
		$serverName = '';
		$companyName = '';
		$companyID = '';
		$startDate = '';
		$backupStarted = 0;
		$errorsFound = 0;
		$fileResult{$kCurrent} = '';
		%storHash = ();
		
		# shorten filename printed
		my $filepath = $file;
	#	$filepath =~ s/(HTML|STANDALONE) log activity (.*?) - .*/$1/i;
		$filepath =~ s/^.* log activity (.*?) - .*/$1/i;
		
		my $fContents = '';
		#print stripTags("Reading $filepath:\n");
		open (my $fh, $file) or die "Can't open $file: $!\n";
		while (my $line = <$fh>) {
			if (onLineRead($file, \$line) != $kIgnoreMe) {
				$fContents = $fContents . $line;
			}#onLineRead($file, $line);
		}
		close $fh;
		onFileRead($file, \$fContents);
	}
}
}	# end-block for 'global'
