import os
import errno

def rmdir(tokens) :
	if len(tokens) == 1 :
		print "rmdir: missing operand"
	elif len(tokens) >= 2 :
		try:
			os.rmdir(tokens[1])
		except OSError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.ENOTDIR and exception.errno != errno.ENOTEMPTY:
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "rmdir: failed to remove '%s': No such file or directory" % tokens[1]
			elif exception.errno == errno.ENOTDIR :
				print "rmdir: failed to remove '%s': Not a directory" % tokens[1]	
			else :
				print "rmdir: failed to remove '%s': Directory not empty" % tokens[1]
		# add loop for multiple folder removing (this assigment does not require)
