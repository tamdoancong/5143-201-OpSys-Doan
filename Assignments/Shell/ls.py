import os
import sys
from pwd import getpwuid 
import datetime

def ls(tokens) :

	if len(tokens) == 1:# if it is just ls without arguments
		tempList = os.listdir(".")
		print "\033[1;32;40m", #change color to green
		for x in range(0, len(tempList)):
			if x % 5 == 0 : # number of columns to be printed
				print "" # to jump to next line
			if tempList[x][0] != "." : #avoid hidden files/folders
				sys.stdout.write(tempList[x].ljust(20)) #avoid endl by using stdout, "," doesn't work!
			sys.stdout.flush() #print out immediately
		print "\033[0;37;40m",#turn color back to normal
		sys.stdout.flush()
		
	elif tokens[1][0] == "-" : #if argument starts with '-'
	
		if "l" in tokens[1]: 
			tempList = os.listdir(".")
			
			hiddenFilesRemovedList = []#-----------------------------------------
			if "a" not in tokens[1] : #if we don't want hidden files to be listed
				for item in tempList :
					if item[0] != '.' :#remove hidden items
						hiddenFilesRemovedList.append(item)
				tempList = hiddenFilesRemovedList#-------------------------------		
				
			for x in range(0, len(tempList)):
				tempStat = os.stat(tempList[x])#getting status of the file/folder
				
				#convert permissions to xwr mode-------------------------
				outputPermission = list("drwxrwxrwx")#initial permissions
				permissions = bin(tempStat.st_mode)
				if len(permissions) == 18 :# directory or not
					outputPermission[0] = '-'
				for i in range(1,10) :
					if permissions[-i] == "0" : 
						outputPermission[-i] = '-'
				print "".join(outputPermission),#print permissions#------
				
				print tempStat.st_nlink, #number of links 
				print  getpwuid(tempStat.st_uid).pw_name, #user id of the owner
				print  getpwuid(tempStat.st_gid).pw_name, #group id of the owner
				
				if "h" in tokens[1] :# convert size to human readable-----------
					if tempStat.st_size < 1024 :#less than one KB
						print "	%d	" %tempStat.st_size,
					elif tempStat.st_size < 1048576 :#less than one MB
						print "	%.1fK	" %(float(tempStat.st_size)/1024),
					elif tempStat.st_size < 1073741824 :#less than one GB
						print "	%.1fM	" %(float(tempStat.st_size)/1048576),
					else :
						print "	%.1fG	" %(float(tempStat.st_size)/1073741824),
				else :#---------------------------------------------------------
					print "	%d	" %tempStat.st_size, #print unconverted size
				
				modTime = datetime.datetime.fromtimestamp( tempStat.st_mtime ) #st.mtime is time of last modification
				print modTime.strftime('%c')[4:], #print the time with sending %c format to strftime (4: to cut week days)
				print "\033[1;32;40m%s\033[0;37;40m" %tempList[x]#change color and print file/folder name	
		
		elif "a" in tokens[1] :
			tempList = os.listdir(".")
			print "\033[1;32;40m",
			for x in range(0, len(tempList)):
				if x % 5 == 0 : # number of columns to be printed
					print "" # to jump to next line
				sys.stdout.write(tempList[x].ljust(20)) #avoid endl by using stdout, "," doesn't work!
				sys.stdout.flush()
			print "\033[0;37;40m",
			sys.stdout.flush()
		else : print "ls: invalid option '%s'" % tokens[1]
		
	else :
		print "ls: invalid option '%s'" % tokens[1]
