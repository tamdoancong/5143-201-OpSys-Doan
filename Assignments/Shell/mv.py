import os
import errno

def mv(tokens) :
	if len(tokens) == 1 :
		print "mv: missing operand"
	elif len(tokens) == 3 :
		try:
			os.rename(tokens[1], tokens[2])
		except OSError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.EISDIR and exception.errno != errno.ENOTDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "mv: cannot stat '%s': No such file or directory" % tokens[1]
			elif exception.errno == errno.EISDIR :
				print "mv: cannot move '%s': Is a directory, add file name after the directory/" % tokens[2]
			elif exception.errno == errno.ENOTDIR :
				print "mv: cannot move '%s': Not a directory" % tokens[2]
							
	elif len(tokens) == 2 :
		print "mv: missing destination file operand after '%s'" %tokens[1]
	else :
		print "mv: target '%s' is not a directory" %tokens[len(tokens)-1] 
	#add loop for multiple movements(It is not required for this assignment)
