import sys, random

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
# The number of incorrect guesses the player can make before losing the game
INCORRECT_GUESS_AMOUNT = 7

HANGMAN_GRAPHICS = [
"",
"""
 -----
 |   |
     |
     |
     |
   ---
""",
"""
 -----
 |   |
 O   |
     |
     |
   ---
""",
"""
 -----
 |   |
 O   |
 |   |
     |
   ---
""",
"""
 -----
 |   |
 O   |
/|   |
     |
   ---
""",
"""
 -----
 |   |
 O   |
/|\  |
     |
   ---
""",
"""
 -----
 |   |
 O   |
/|\  |
/    |
   ---
""",
"""
 -----
 |   |
 O   |
/|\  |
/ \  |
   ---
"""]

def loadDict():
	'''Open an english dictionary file and create a list of all the words in it'''
	
	dictFile = open("dictionary.txt")
	words = []
	nonwords = []
	for word in dictFile.read().split("\n"):
		if word != "":
			words.append(word.lower())
	dictFile.close()
	return words

ENGLISH_WORDS = loadDict()


def loadHighScores():
	'''Open a high scores top ten file and create a dictionary of the scores in it'''

	highScoreFile = open("HighScores.txt")
	scores = {}
	contents = highScoreFile.read().split("\n")
	# scores dict has each score's location in the list as the key and the score itself as the value
	for line in range(10):
		scores[str(line)] = contents[line]
	highScoreFile.close()
	return scores


def saveHighScores(newFileLines):
	'''Open a high scores top ten file and write the new high scores to it'''

	highScoreFile = open("HighScores.txt", "w")
	scores = []
	for value in sorted(newFileLines.values()):
		scores.append(str(value))
	highScoreFile.writelines(scores)
	highScoreFile.close()


def getLocationInHighScores(newScore):
	'''Get a score's location in the top ten'''

	highScores = loadHighScores()
	for pos, score in sorted(highScores.items()):
		# No score in this location yet
		if score == "":
			return pos
		# Check if the new score is greater than a score in the list
		elif newScore > score:
			return pos
	# The given score isn't greater than any of the scores in the file, return None
	return None


def isEnglish(word):
	'''Check if a word is in the english dictionary'''

	return word in ENGLISH_WORDS


def isWordFound(completeWord, wordSoFar):
	'''Check if the guesser has found the correct word'''

	if completeWord == wordSoFar:
		return True


def isGuessCorrect(completeWord, letter):
	'''Check if a certain letter is in the word'''

	return letter in completeWord


def printInfo(incorrectGuesses, letterGuess, wordSoFar, completeWord, lettersGuessedSoFar):
	'''Print the letter guess, whether the guess is correct or not, the total number of incorrect
	guesses, the hangman picture, the incomplete word, and the letters guessed so far.'''

	print("")
	print("Guess: {0}".format(letterGuess))
	print("This guess is {0}.".format(str(isGuessCorrect(completeWord, letterGuess)).lower()))
	print("Total incorrect guesses: {0}".format(str(incorrectGuesses)))

	# List index of picture to print = # of incorrect guesses
	print(HANGMAN_GRAPHICS[incorrectGuesses])

	print(wordSoFar.capitalize())
	print("Letters guessed so far: {0}".format(" ".join(lettersGuessedSoFar)))
	print("")

	# If the correct word was found, print a message
	if isWordFound(completeWord, wordSoFar):
		print("Hooray! The correct word has been found. It was: {0}".format(completeWord.capitalize()))
		print("")

	# If the guesser has run out of incorrect guesses, print a message
	elif incorrectGuesses >= INCORRECT_GUESS_AMOUNT:
		print("Oh no! The correct word wasn't found in time. It was: {0}".format(completeWord.capitalize()))
		print("")


def updateWordKnowledge(letterGuess, completeWord, wordSoFar):
	'''Add a newly discovered letter to an incomplete word based on that letter's positions in the
	complete word'''

	wordSoFar = list(wordSoFar)
	for index, letter in enumerate(completeWord):
		if letter == letterGuess:
			wordSoFar[index] = letter
	return ''.join(wordSoFar)


def removeNonMatchingWords(possibleWords, wordSoFar):
	'''Remove words that can't be a certain word from the list of possible words'''

	for word in reversed(possibleWords):
		# Make sure each letter in the word matches the letters that have been found in the word so far
		for index, char in enumerate(word):
			if wordSoFar[index] != "-" and wordSoFar[index] != char:
				possibleWords.remove(word)
				break
	return possibleWords
	

def removeWordsContainingLetter(possibleWords, letter):
	'''Remove any words containing a certain letter from the list of possible words'''

	for word in reversed(possibleWords):
		if letter in word:
			possibleWords.remove(word)
	return possibleWords


def getLettersFreq(wordDict, lettersGuessedSoFar):
	'''Return string of letters ordered from most to least frequent based on the letters in the word
	dictionary'''

	letterToFreq = {}
	for letter in ALPHABET:
		# Don't add letters that have already been guessed to the string of letters that can be guessed
		if letter not in lettersGuessedSoFar:
			letterToFreq[letter] = 0
	for word in wordDict:
		for letter in word:
			if letter not in lettersGuessedSoFar and letter in ALPHABET:
				letterToFreq[letter] += 1

	# Create list of tuples with the letter frequency as the first value in the tuple and the letter
	# itself as the second value. Sort this list from the highest frequencies to the lowest frequencies
	freqToLetter = list(zip(letterToFreq.values(), letterToFreq.keys()))
	freqToLetter.sort(reverse=True)

	orderedLetters = ""
	for freqAndLetter in freqToLetter:
		# Don't add letters with a frequency of 0
		if freqAndLetter[0] != 0:
			orderedLetters += freqAndLetter[1]

	return orderedLetters


def getEnglishWord(playerType):
	'''Return an english word. If the player is human, let them choose the word'''
	
	if playerType == "computer":
		return random.choice(ENGLISH_WORDS)
	elif playerType == "human":
		word = ""
		# Don't let the player enter a non-English word
		while not isEnglish(word):
			word = input("Please enter an English word: ").lower()
		return word


def computerTurn(completeWord):
	'''The computer tries to guess what the player's word is'''

	wordLength = len(completeWord)
	lettersGuessedSoFar = []
	incorrectGuesses = 0
	wordSoFar = "-" * wordLength

	# Create a list of possible words from a dictionary, containing only words that are the same
	# length as the player's word
	possibleWords = []
	for word in ENGLISH_WORDS:
		# Only add words that are as long as the complete word
		if len(completeWord) == len(word):
			possibleWords.append(word)

	# Create a list of letters ordered from most frequent to least frequent. As the computer
	# makes guesses and recieves feedback, this list will be pruned
	orderedLetters = getLettersFreq(possibleWords, lettersGuessedSoFar)

	while incorrectGuesses < INCORRECT_GUESS_AMOUNT and not isWordFound(completeWord, wordSoFar):
		letterGuess = orderedLetters[0]

		if isGuessCorrect(completeWord, letterGuess):
			# Add the letter guessed to the knowledge of the player's word in the correct places
			wordSoFar = updateWordKnowledge(letterGuess, completeWord, wordSoFar)
			# Remove the words that can't be the player's word from the list of possible words
			possibleWords = removeNonMatchingWords(possibleWords, wordSoFar)
		else:
			incorrectGuesses += 1
			# Remove words that contain the incorrect letter from the list of possible words
			possibleWords = removeWordsContainingLetter(possibleWords, letterGuess)

		lettersGuessedSoFar.append(letterGuess)
		orderedLetters = getLettersFreq(possibleWords, lettersGuessedSoFar)

		print("")
		input("Press 'enter' for the next guess.")
		printInfo(incorrectGuesses, letterGuess, wordSoFar, completeWord, lettersGuessedSoFar)


def humanTurn(completeWord):
	'''The human player tries to guess what the computer's word is'''

	wordLength = len(completeWord)
	lettersGuessedSoFar = []
	incorrectGuesses = 0
	wordSoFar = "-" * wordLength

	while incorrectGuesses < INCORRECT_GUESS_AMOUNT and not isWordFound(completeWord, wordSoFar):
		letterGuess = ""
		# Don't let the player guess a letter that they've alreay guessed
		while len(letterGuess) != 1 or not letterGuess.isalpha() or letterGuess in lettersGuessedSoFar:
			letterGuess = input("Enter your guess for a letter in the word: ").lower()

		if isGuessCorrect(completeWord, letterGuess):
			# Add the letter guessed to the knowledge of the computer's word in the correct places
			wordSoFar = updateWordKnowledge(letterGuess, completeWord, wordSoFar)

		else:
			incorrectGuesses += 1

		lettersGuessedSoFar.append(letterGuess)
		printInfo(incorrectGuesses, letterGuess, wordSoFar, completeWord, lettersGuessedSoFar)

	# If the player won, return the amount of incorrect guesses they made
	if incorrectGuesses < INCORRECT_GUESS_AMOUNT:
		return incorrectGuesses

	return None

def main():
	print("Welcome to Hangman!")
	input("Press the 'enter' key to begin playing.")
	print("")
	print("On your turn, the computer will think of a word. You will try to guess each letter of the word.")
	print("On the computer's turn, you will think of a word. The computer will try to guess each letter of it.")
	print("Each time you make an incorrect guess, more parts of a stick figure are drawn. You can only make {0} incorrect guesses before you lose the game.".format(str(INCORRECT_GUESS_AMOUNT)))
	input()

	# Main game loop
	while True:
		# Player guesses computer's word
		print("You will go first.")
		word = getEnglishWord("computer")
		incorrectGuesses = humanTurn(word)

		# If the player found the correct word in time, see if their score is in the top ten
		if incorrectGuesses != None:
			scoreLocation = getLocationInHighScores(incorrectGuesses)

			# Score is in top ten
			if scoreLocation != None:
				highScores = loadHighScores()
				highScores[scoreLocation] = incorrectGuesses
				print("Congratulations! Your score is in the top ten!")
				print("")

				# Print the top ten high scores
				for pos, score in sorted(highScores.items()):
					if pos == scoreLocation:
						# Put asterisks around the player's score
						print(pos + ". " + "*" + str(score) + "*")
					else:
						print(pos + ". " + str(score))
				saveHighScores(highScores)
		print("")
		print("")

		# Computer guesses player's word
		print("Now the computer will go.")
		print("")
		word = getEnglishWord("human")
		print("")
		computerTurn(word)

		ans = input("Want to play again? (y/n): ").lower()
		if ans in ("n", "no"):
			sys.exit()

if __name__ == "__main__":
	main()
