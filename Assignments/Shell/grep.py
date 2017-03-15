import errno
def grep(tokens) :
	if len(tokens) == 1 :
		print "grep: missing operand"
		
	elif len(tokens) >= 3 :
		temp = tokens[1].split("'") # removing '' from the keyword
		if len(temp) == 3 :#to avoid IndexError
			tokens[1] = temp[1]
		try:
			file = open(tokens[2],'r')
			for line in file:
				if tokens[1] in line:
					#add red color to the keyword and print the found line
					print line.replace(tokens[1],'\033[1;31;40m' + tokens[1] + '\033[0;37;40m'),		
		except IOError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.EISDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "grep: '%s': No such file or directory" % tokens[2]
			elif exception.errno == errno.EISDIR :
				print "grep: %s: Is a directory" % tokens[2]	
	
