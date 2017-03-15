import os
import errno

def rm(tokens) :
	if len(tokens) == 1 :
		print "rm: missing operand"
	elif len(tokens) >= 2 :
		try:
			os.remove(tokens[1])
		except OSError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.EISDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "rm: cannot remove '%s': No such file or directory" % tokens[1]
			elif exception.errno == errno.EISDIR :
				print "rm: cannot remove '%s': Is a directory" % tokens[1]
		# add loop for multiple file removing, but professor does not require
