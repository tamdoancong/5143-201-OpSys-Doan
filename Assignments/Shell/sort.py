import errno
def sort(tokens) :
	if len(tokens) == 1 :
		print "sort: missing operand"
	elif len(tokens) >= 2 :
		sortList = []
		try:
			file = open(tokens[1], 'r')
			for line in file :# copy file lines to a list
				sortList.append(line)
			sortList.sort()

			for x in range (0,len(sortList)) :
				print sortList[x],

		except IOError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.EISDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "sort: '%s': No such file or directory" % tokens[1]
			elif exception.errno == errno.EISDIR :
				print "sort: %s: Is a directory" % tokens[1]	
