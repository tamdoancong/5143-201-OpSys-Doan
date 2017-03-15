import errno
def wc(tokens) :
	if len(tokens) == 1 :
		print "wc: missing operand"
	elif len(tokens) >= 2 :
		try:
			lineCount = 0	
			wordCount = 0
			charCount = 0
			file = open(tokens[1], 'r')
			for line in file :
				lineCount += 1
				wordCount += len(line.split())
				charCount += len(line)
			print lineCount-1,
			print " ",
			print wordCount,
			print " ",
			print charCount,
			if ".cache" not in tokens[1] : #avoid printing file name for cache files while piping
				print " " + tokens[1]
			
		except IOError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.EISDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "wc: '%s': No such file or directory" % tokens[1]
			elif exception.errno == errno.EISDIR :
				print "wc: %s: Is a directory" % tokens[1]
