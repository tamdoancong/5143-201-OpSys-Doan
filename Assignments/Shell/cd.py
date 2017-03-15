import os
import errno

def cd(tokens) :
	if len(tokens) == 1 :
		from os.path import expanduser
		os.chdir(expanduser("~"))
	elif tokens[1] == ".." :
		os.chdir("..")	
	elif tokens[1] == "~" :
		from os.path import expanduser
		os.chdir(expanduser("~"))
	elif len(tokens) >= 2 :
		try:
			os.chdir(tokens[1])
		except OSError as exception:
			if exception.errno != errno.ENOENT and exception.errno != errno.ENOTDIR :
				print "File/Directory error"
			elif exception.errno == errno.ENOENT :
				print "cd: %s: No such file or directory" % tokens[1]
			else :
				print "cd: %s: Not a directory" % tokens[1]
#add spaced directories later! \ before spaces	
