import errno

def cat(tokens) :
	if len(tokens) == 1 :
		print "cat: missing operand"
	elif len(tokens) == 2 :
		try:
			file = open(tokens[1], 'r')
			for line in file:
				print line,
		except IOError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.EISDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "cat: '%s': No such file or directory" % tokens[1]
			elif exception.errno == errno.EISDIR :
				print "cat: %s: Is a directory" % tokens[1]	
	
	elif len(tokens) >= 3 :# print out two files to concatenate 
		try:
			file = open(tokens[1], 'r')
			for line in file:
				print line,
		except IOError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.EISDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "cat: '%s': No such file or directory" % tokens[1]
			elif exception.errno == errno.EISDIR :
				print "cat: %s: Is a directory" % tokens[1]	
		
		try:  #print out the second file
			file = open(tokens[2], 'r')
			for line in file:
				print line,
		except IOError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.EISDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "cat: '%s': No such file or directory" % tokens[2]
			elif exception.errno == errno.EISDIR :
				print "cat: %s: Is a directory" % tokens[2]
