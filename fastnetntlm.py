#!/usr/bin/env python

####################################################################################
# Author:      Tim Medin
# Contact:     timmedin [@] securitywhole [d0t] com
# Updated By:  Dan Borkowski
# Name:        fastnetntlm.py
# Version:     0.11
# Description: An automated method of reading netntlm hashes and cracking them
####################################################################################


####################################################################################
# TODO:
#    Errors due to invalid paths are not output, stat the files to ensure they exist
####################################################################################

from __future__ import with_statement # Required in 2.5
from sys import *
import os
import time
import subprocess
import fileinput
from optparse import OptionParser
from optparse import OptionGroup
from datetime import datetime
from sets import Set
import signal
from contextlib import contextmanager

class AlreadyCracked(Exception): pass

#timeout code pulled from http://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call-in-python
class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


usage = "usage: %prog [options] hashesfile"
parser = OptionParser(usage=usage, version="%prog 0.1")
#parser.add_option("-f", "--hashesfile", action="store", type="string", dest="hashesfile",  help="file containing the hashes")
parser.add_option("-a", "--alpha",      action="store", type="string", dest="rt_alpha",    help="path to halflmchall_alpha-numeric rainbow tables")
parser.add_option("-b", "--all",        action="store", type="string", dest="rt_allspace", help="path to halflmchall_all-space rainbow tables")
parser.add_option("-v", "--verbose",    action="store_true",           dest="verbose",     help="don't print status messages to stdout", default=False)
parser.add_option("-o", "--output",	action="store", type="string", dest="output",	help="output file containing passwords", default=False)
parser.add_option("-t", "--timeout",	action="store",	type="int", dest="timeout",	help="timeout for a particular hash. :TIMEOUT: will be outputted as the password", default=0)

group = OptionGroup(parser, "Suplementary executable locations", "If your file locations differ from the default use these options")
group.add_option("-p", "--perlpath",    action="store", type="string", dest="perl",        help="path to perl (default is /usr/bin/perl)", default="/usr/bin/perl")
group.add_option("-j", "--johnnetntlm", action="store", type="string", dest="johnnetntlm", help="path to John the Ripper's netntlm.pl from Jumbo Pack (default is /usr/share/john/netntlm.pl)", default="/usr/share/john/netntlm.pl")
group.add_option("-r", "--rcracki",     action="store", type="string", dest="rcracki",     help="path to rcracki_mt (default is /usr/bin/rcracki_mt)", default="/usr/bin/rcracki_mt")
parser.add_option_group(group)

(options, args) = parser.parse_args()

# check that files/tools exist
if not os.path.exists(options.johnnetntlm):
	parser.error ("John's netntlm.pl does not exist")
if not os.path.exists(options.rcracki):
        parser.error ("rcracki does not exist")
if not os.path.exists(options.perl):
        parser.error ("Perl does not exist")

# put the rainbbow tables into a list
rtables = []
if options.rt_alpha:
        rtables.append(options.rt_alpha)
if options.rt_allspace:
        rtables.append(options.rt_allspace)
if len(rtables) == 0:
        parser.error("No rainbow tables specified")

# ensure an input file is specified
if len(args) == 0:
        parser.error("No hashes file specified")
        OptionParser.print_usage()

# TODO: FIX THIS THE RIGHT WAY
#print "Make sure you copy the charset.txt file from the directory rcracki_mt runs in"

# open hashes file and remove duplidates
fin = open(args[0],"r")
hashes = set([])
for hashrow in fin:
        hashes.add(hashrow)
fin.close()

# crack away baby
for line in hashes:
	try:
		with time_limit(options.timeout):
			if options.verbose: print "Processing " + line.replace("\n","")
			
			# parse the file
			user = line.split(":")[0] 
			domain = line.split(":")[2] 
			lmhash = line.split(":")[3]
			lmhash_first = lmhash[0:16]
			
			#check output file to see if hash has already been cracked
			if options.output and os.path.exists(options.output):
				outfile = open(options.output,'r')
				for lineoutput in outfile:
					if user in lineoutput:
						if options.verbose: print user + " has already been cracked. Skipping\n"
						raise AlreadyCracked

			if options.verbose: print str(datetime.now()) + ": Processing " + user + " with tables " + rtables[0]
			process = subprocess.Popen(options.rcracki + " -h " + lmhash_first + " " + rtables[0], shell=True, stdout=subprocess.PIPE)
			lastline = process.communicate()[0].splitlines()[-1]
			seed = lastline.split()[1]
			if options.verbose: print str(datetime.now()) + ": Processing " + user + " seed: " + seed

			if seed == "<notfound>" and len(rtables) == 2:
				if options.verbose: print str(datetime.now()) + ": Processing " + user + " with tables " + rtables[0]
				process = subprocess.Popen(options.rcracki + " -h " + lmhash_first + " " + rtables[1], shell=True, stdout=subprocess.PIPE)
				lastline = process.communicate()[0].splitlines()[-1]
				seed = lastline.split()[1]
				if options.verbose: print str(datetime.now()) + ": Processing " + user + " seed:  " + seed

			if seed != "<notfound>":
				singlehashfile = domain + "." + user + ".hash"
				fout = open(singlehashfile, "w")
				fout.write(line)
				fout.close()

				if options.verbose: print str(datetime.now()) + ": Bruteforcing the remainder of " + user + "'s password  " + seed
				process = subprocess.Popen(options.perl + " " + options.johnnetntlm + " --seed \'" + seed + "\' --file " + singlehashfile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				if options.verbose: print str("Running: " + options.perl + " " + options.johnnetntlm + " --seed \'" + seed + "\' --file " + singlehashfile)
				out = process.communicate()
				#print "out=%s" % (out,)
				#pull case insensitive password out of output and feed it as the seed of the same command
				for line in out[0].splitlines():
					if line.find("(" + user +")") > 0:
						seed = line.split()[0]	
				process = subprocess.Popen(options.perl + " " + options.johnnetntlm + " --seed \'" + seed + "\' --file " + singlehashfile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				out = process.communicate()
				#print "out=%s" % (out,)
				# check the output. the first part looks for a new crack                
				passwd = None
				for line in out[0].splitlines():
					if line.find("(" + user +")") > 0:
						passwd = line.split()[0]
						#print "passwd=" + passwd				

				# if the password was previously found use this to extract it from the output
				if not passwd:
					for line in out[0].splitlines():
						if line.find(user) > 0:
							passwd = line.split(":")[1]
							#pass =print domain + " " + user + " " + line.split()[0]
							#print "passwd=" + passwd

	except TimeoutException, msg:
		passwd=":TIMEOUT:"
	except AlreadyCracked, msg:
		continue

	print domain + " " + user + " " +  passwd 
	if options.output:
			outputfile = open(options.output,'a')
			outputfile.write(domain + " " + user + " " +  passwd + "\n")
			outputfile.close()
			#print passwd
	try:
		os.remove(singlehashfile)
	except:
		pass
	
