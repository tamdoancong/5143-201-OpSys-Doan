import shutil

def cp(tokens) :
	if len(tokens) == 1 :
		print "cp: missing operand"
	elif len(tokens) == 3 :
		try:
			shutil.copy2(tokens[1], tokens[2])
		except IOError as exception:
			if exception.errno != 2 and exception.errno != 21 :
				print "File/Directory error"
			else:
				if exception.errno == 2 :
					print "cp: cannot stat '%s': No such file or directory" % tokens[1]
				elif exception.errno == 21 :
					print "cp: cannot copy '%s': Is a directory" % tokens[1]
					
	elif len(tokens) == 2 :
		print "cp: missing destination file operand after '%s'" %tokens[1]
	else :
		print "cp: target '%s' is not a directory or more than 2 operands entered" %tokens[len(tokens)-1]
    #add loop for multiple copies(but professor did not require :))
