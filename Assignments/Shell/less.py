import os
import errno
def less(tokens) :
	if len(tokens) == 1 :
		print "less: missing operand"
	elif len(tokens) >= 2 :
		try:
			file = open(tokens[1], 'r')
			counter = 0
			for line in file:
				print line,
				counter+=1
				if counter%24 == 0 : #assume 24 lines as a page
					lineInput = raw_input("\033[0;30;47mPress enter for next page...							Page (%s)\033[0;37;40m"%(counter/24) )
					os.system('clear')# clear screen
			print "\n\033[0;30;47m                               End                               \033[0;37;40m" #endl
		except IOError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.EISDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "less: '%s': No such file or directory" % tokens[1]
			elif exception.errno == errno.EISDIR :
				print "less: %s: Is a directory" % tokens[1]	
		# we have to add loop if we want to do multiple files ( assignment does not require
