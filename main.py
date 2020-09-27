# madlibs source: https://za.pinterest.com/pin/465981892667418576/
# NOTE: I address Mad Libs as story

def displayMenu(): # This is where the user can decide what to do
	print("Welcome! Let's play a madlibs game!")
	print("What would you like to do?")
	print("1) Play madlibs")
	print("2) Make madlibs")
	print("0) Exit")
	ans = input("ANSWER: ")
	return validateInput(ans.lower()) # make sure the users option is valid

def saveStory(story): # saves story to text file
	tFile = open("libs.txt", "a") # in append mode
	tFile.write(story)
	tFile.close()

def createGame(): # when the user wants to create a game
	# some info to note before writing the story
	print("\nTo make your own story, just type the story you want (don't press the <ENTER> button until you're done), whenever someone should insert something, put it inside brackets like this [verb]. Here is an example: As he, [name_of_person], stood... Remeber, things that is more than 1 word should use underscores(_) in place of spaces!! (Press Ctrl+C to cancel at any time)")
	print("'|' and '_' are special characters, please refrain from using them outside [] (don't use '|' at all)\n")

	name = input("Name of your Mad Lib:") # story name
	story = input("Write your Mad Lib: ") # story itself

	# make sure "|" does not exist anywhere in the story or title
	if name.find("|") > -1 or story.find("|") > -1: 
		print("Please do not use '|'!!!")
		return createGame() # recursive function

	numOpenBrackets = 0
	numCloseBrackets = 0
	for char in story: # the number of "[" and "]" should be the same
		if char == "[":
			numOpenBrackets += 1
		elif char == "]":
			numCloseBrackets += 1

	if numOpenBrackets != numCloseBrackets:
		print("Number of '[' is not the same as number of ']'");
		return createGame()

	# "[" and "]" for safety reasons should not exist inside then name of the story
	if name.find("[") > -1 or name.find("]") > -1:
		print("Please do not use either '[' or ']' in the name of your lib")
		return createGame()

	# save new story to text file
	saveStory("\n\n" + name + "\n" + story) 
	print("\nLib has been saved!!\n")
	return displayMenu()

def validateInput(inp): # make sure the user inserts a valid option
	if not inp in ["1", "2", "0", "exit"]:
		print("No such option exists")
		return displayMenu()
	elif inp in ["0", "exit"]:
		print("EXIT")
		return
	elif inp == "1":
		return playGame()
	else:
		return createGame()

def getCommands(desc): # get commands "[]" from story
	index = 0
	commands = []
	for char in desc:
		if char == '[':
			temp = "  " # I had to add 2 spaces for it to work... Why, Python?
			if index > 0:
				tIndex = index # tIndex = temp index
				tNum = 0 # tNum = temp num
				while temp[tNum] != ']':
					temp += desc[tIndex]
					tIndex += 1
					tNum += 1
				commands.append(temp)
		index += 1;

	index = 0
	# remove useless characters from commands
	for com in commands:
		com = com[:-2]
		com = com.replace(" ", "")
		com = com.replace("_", " ")
		commands[index] = com[1:]
		index += 1

	return commands

# the words the user decides to insert goes through here
def insertWords(words, desc):
	story = ""
	index = 0
	skip = False # should we skip the next few characters
	skipped = False # did we skip a few characters

	for com in desc:
		if com == "[":
			skip = True

		if com == "]":
			skip = False
			skipped = True
			continue

		if skip:
			continue

		if skipped:
			story += words[index]
			index += 1
			skipped = False
		story += com

	print("\n" + story + "\n")
	return displayMenu()

def playGame(): # playing the game
	story = chooseGame() # choose a story
	story_description = story[story.find("|") + 1:] 
	story_name = story.replace("|" + story_description, "") 
	
	# gets all replacable parts from story
	commands = getCommands(story_description)

	print(story_name.upper())
	answers = []
	for ans in commands:
		answers.append(input(ans + ": "))

	insertWords(answers, story_description);

def chooseGame(): # finds all availible games
	tFile = open("libs.txt", "r") 
	text = tFile.readlines()
	tFile.close()

	lineNum = 1
	names = []
	stories = []
	for lines in text:
		# titles would be at lines 1, 3, 5 etc.
		if (lineNum % 2 == 1) and (lines != '\n'):
			names.append(lines.replace("\n", ""))
		elif not lines == "\n": # gets the story
			stories.append(lines.replace("\n", ""))
		else:
			continue	
		lineNum += 1

	print("Which madlibs would you like to play?")
	x = 1
	for name in names:
		print(str(x) + ") " + name)
		x += 1
	ans = input("ANSWER: ")
	try:
		int(ans) # try to convert to integer
	except Exception as e:
		print("Invalid option!")
		return chooseGame()

	ans = int(ans)
	if ans > x or ans < 1:
		print("Invalid option!")
		return chooseGame()

	selection = ans - 1
	chosen_name = names[selection]
	chosen_story = stories[selection]

	return chosen_name + "|" + chosen_story

displayMenu()