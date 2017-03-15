import errno
def head(tokens) :
	if len(tokens) == 1 :
		print "head: missing operand"
	else :
		try:
			file = open(tokens[1], 'r')
			counter = 0
			for line in file:
				print line,
				counter+=1
				if counter == 10 : #prints first 10 lines of file
					break
		except IOError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.EISDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "head: '%s': No such file or directory" % tokens[1]
			elif exception.errno == errno.EISDIR :
				print "head: %s: Is a directory" % tokens[1]	
		# we have add loop for using multiple files (This  assigment does not require)
