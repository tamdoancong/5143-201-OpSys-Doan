import sys
import os
import threading
from cat import cat
from cd import cd
from chmod import chmod
from cp import cp
from grep import grep
from head import head
from less import less
from ls import ls
from mkdir import mkdir
from mv import mv
from Pwd import pwd
from rm import rm
from rmdir import rmdir
from sort import sort
from tail import tail
from wc import wc
from who import who




def readHistory() : #reading history procedure
	try:
		historyFile = open(".history", 'r')
	except IOError:
		historyFile = open(".history", 'w+')
	for line in historyFile :
		historyList.append(line.replace("\n" , ""))

def backupHistory()	:#backup history procedure
	historyFile = open(currentPath + "/.history", 'w')
	for command in historyList :
		historyFile.write(command + "\n" )

		
		
		
Tokens = []
pipeList = []
historyList = [] #keeps a list of history
currentPath = os.getcwd()#keep current path to backup the history and cache files to the same path
threading.Thread(target=readHistory).start()#copy history file into history list

while 1 :

	tempStdOut = sys.stdout#take a copy of system stdout
	lineInput = raw_input("\n% ")
	
	#run a command from history: !x ---------------------------------
	tempInput = lineInput.strip(' ')#remove spaces 
	if len(tempInput) > 0 : 
		if tempInput[0] == "!" :# if starts with an exclamation point
			tempInput = tempInput.strip('!')#remove ! from file
			try :#assign selected history command to current command
				lineInput = historyList[int(tempInput)-1]
			except :
				print "bash: %s: event not found"%lineInput#---------
				
	if lineInput.strip(' ') != "" : #check to avoid adding empty commands to history
		historyList.append(lineInput) #adding command to history list
	
	runInBackground = 0# running in background if & entered
	if "&" in lineInput :
		runInBackground = 1
		lineInput = lineInput.strip('&')#remove &
		
	pipeList = lineInput.split("|")
	pipeCounter = 0
	for pipe in pipeList :
		Tokens = pipe.split(" ")
		while '' in Tokens :
			Tokens.remove('') #remove empty tokens from list 
			
		if len(pipeList) > 1 :#if we have any pipes--------------------------------------------------------
			pipeCounter+=1
			if pipeCounter > 1 :#append cache file to command 
				if ">" in Tokens :#if we also have stdout redirection insert cache file in right place
					# %2 so we have two .cache0 and .cache1 files to switch between
					Tokens.insert(Tokens.index(">") , currentPath+"/.cache"+str(pipeCounter%2)) 
				elif ">>" in Tokens :
					Tokens.insert(Tokens.index(">>") , currentPath+"/.cache"+str(pipeCounter%2))
				else :# if no redirection append cache file to end
					Tokens.append(currentPath+"/.cache"+str(pipeCounter%2))		
			if pipeCounter < len(pipeList) : # if there are still pipes to be done
				sys.stdout = open(currentPath+"/.cache"+str((pipeCounter+1)%2), "w+")#redirect stdout to a cache file
			elif pipeCounter == len(pipeList):#if there are no other pipes
				sys.stdout = tempStdOut# redirect stdout to normal form to print the last result-----------

				
		stdoutRedirected  = False#redirecting stdout to a file------------------------------------
		if (">" in Tokens) and len(Tokens) > 2 :# also check length to avoid index error
			try:#error handling
				sys.stdout = open(Tokens[Tokens.index(">")+1], "w+")#redirect stdout to a file next to
				del Tokens[Tokens.index(">"):] #trim > and followings
				stdoutRedirected  = True
			except IOError:
				print "%s: Is a directory" % Tokens[Tokens.index(">")+1]
		elif (">>" in Tokens) and len(Tokens) > 2 :
			try:#error handling
				sys.stdout = open(Tokens[Tokens.index(">>")+1], "a")#redirect stdout to a file
				del Tokens[Tokens.index(">>"):] #trim >> and followings
				stdoutRedirected  = True
			except IOError:
				print "%s: Is a directory" % Tokens[Tokens.index(">>")+1]			
		elif "<" in Tokens :#if we also have stdin redirection insert file in place
			Tokens.insert(Tokens.index("<") , Tokens[2])
			del Tokens[Tokens.index("<"):]#trim < and followings----------------------------------

			
		if len(Tokens) > 0 :# if we have any tokens call functions
			if Tokens[0] == "exit" :
				#backup history before exiting
				trd = threading.Thread(target=backupHistory)
				trd.start()
				trd.join()
				exit()
			elif Tokens[0] == "history" :# print out history list if command was history
				for x in range(0,len(historyList)) :
					print "  " + str(x+1).ljust(5),
					print historyList[x]
			#all of our functions have the same name of the command they are representing so we can look for 
			#the command token in our global symbol table dictionary and find the function of that command
			globalSymbolTable = globals().copy()#make a copy of current global symbol table dictionary
			TempFunction = globalSymbolTable.get(Tokens[0])#looking for the function in the symbol table dictionary
			if TempFunction != None :
				trd = threading.Thread(target=TempFunction,args=(Tokens,))#call the function by a thread
				trd.start()
				if runInBackground == 0 :
					trd.join()
			elif Tokens[0] != "history" :
				print "%s: command not found" %Tokens[0]
	
	
		if stdoutRedirected : #redirect stdout to normal form for the next round
			sys.stdout = tempStdOut
