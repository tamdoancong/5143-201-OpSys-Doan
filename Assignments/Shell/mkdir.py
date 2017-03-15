import os
import errno

def mkdir(tokens) :
	if len(tokens) == 1 :
		print "mkdir: missing operand"
	else :
		for x in range(1, len(tokens)):
			try:
				os.makedirs(tokens[x])
			except OSError as exception:
				if exception.errno != errno.EEXIST and exception.errno != errno.ENOENT:
					print "File/Directory error"
				elif exception.errno == errno.EEXIST :
					print "mkdir: cannot create directory '%s' : File exists" % tokens[x]
				else :
					print "mkdir: No such file or directory: %s" % tokens[x]
