import errno
def tail(tokens) :
	if len(tokens) == 1 :
		print "tail: missing operand"
	elif len(tokens) >= 2 :
		try:
			linesNum = len(open(tokens[1]).readlines()) #number of lines of file		
			counter = 0
			file = open(tokens[1], 'r')
			for line in file:
				counter+=1
				if counter > (linesNum-10) :#10 last lines
					print line,

		except IOError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.EISDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "tail: '%s': No such file or directory" % tokens[1]
			elif exception.errno == errno.EISDIR :
				print "tail: %s: Is a directory" % tokens[1]	
		# we have to add loop for using multiple files 	
