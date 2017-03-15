import os
def chmod(tokens) :
	if len(tokens) < 3 :
		print "chmod: missing operand"
	else :
		try:
			os.chmod( tokens[2], int(tokens[1],8) ) #specifying base 8 for 4-digit number 0XXX
		except OSError as exception :
			if exception.errno == 2 :
				print "chmod: '%s': No such file or directory" % tokens[2]
		except (ValueError) :
			print "chmod: invalid mode: '%s'" % tokens[1]
