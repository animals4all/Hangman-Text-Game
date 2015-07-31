import sys, random

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
	for word in dictFile.read().split("\n"):
		if word != "":
			words.append(word)
	dictFile.close()
	return words

ENGLISH_WORDS = loadDict()


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


def printInfo(incorrectGuesses, letterGuess, guessCorrect, wordSoFar, completeWord, lettersGuessedSoFar):
	'''Print the letter guess, whether the guess is correct or not, the total number of incorrect
	guesses, the hangman picture, the incomplete word, and the letters guessed so far.'''

	print("")
	print("Guess: {0}").format(letterGuess)
	print("This guess is {0}.").format(str(guessCorrect).lower())
	print("Total incorrect guesses: {0}").format(str(incorrectGuesses))

	# List index of picture to print = # of incorrect guesses
	print(HANGMAN_GRAPHICS[incorrectGuesses])

	print(wordSoFar.capitalize())
	print("Letters guessed so far: {0}").format(" ".join(lettersGuessedSoFar))
	print("")

	# If the correct word was found, print a message
	if isWordFound(completeWord, wordSoFar):
		print("Hooray! The correct word has been found. It was: {0}").format(completeWord.capitalize())
		print("")

	# If the guesser has run out of incorrect guesses, print a message
	elif incorrectGuesses >= INCORRECT_GUESS_AMOUNT:
		print("Oh no! The correct word wasn't found in time. It was: {0}").format(completeWord.capitalize())
		print("")
		print("GAME OVER")
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


def isLetterInWords(possibleWords, letter):
	'''Check if a letter is found in any of the words given'''

	for word in possibleWords:
		if letter in word:
			return True
	return False


def removeLettersNotInWords(possibleWords, availableLetters):
	'''Remove letters not found in any of the possible words from the list of available letters'''

	for letter in reversed(availableLetters):
		if not isLetterInWords(possibleWords, letter):
			availableLetters.remove(letter)
	return availableLetters


def getEnglishWord(playerType):
	'''Return an english word. If the player is human, let them choose the word'''
	
	if playerType == "computer":
		return random.choice(ENGLISH_WORDS)
	elif playerType == "human":
		word = ""
		while not isEnglish(word):
			word = raw_input("Please enter an English word: ").lower()
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
		if len(word) == len(wordSoFar):
			possibleWords.append(word)

	# Create a list of letters ordered from most frequent to least frequent. As the computer
	# makes guesses and recieves feedback, this list will be pruned
	orderedLetters = list("etaoinshrdlcumwfgypbvkjxqz")

	while incorrectGuesses < INCORRECT_GUESS_AMOUNT and not isWordFound(completeWord, wordSoFar):
		letterGuess = orderedLetters[0]

		guessCorrect = isGuessCorrect(completeWord, letterGuess)
		if guessCorrect:
			# Add the letter guessed to the knowledge of the player's word in the correct places
			wordSoFar = updateWordKnowledge(letterGuess, completeWord, wordSoFar)

			# Remove the words that can't be the player's word from the list of possible words
			possibleWords = removeNonMatchingWords(possibleWords, wordSoFar)

		else:
			incorrectGuesses += 1

			# Remove words that contain the incorrect letter from the list of possible words
			possibleWords = removeWordsContainingLetter(possibleWords, letterGuess)
		print("")
		raw_input("Press 'enter' for the next guess.")
		lettersGuessedSoFar.append(letterGuess)
		printInfo(incorrectGuesses, letterGuess, guessCorrect, wordSoFar, completeWord, lettersGuessedSoFar)

		# Remove the incorrect letter and letters not found in any of the possible words from the
		# list of letters
		orderedLetters.remove(letterGuess)
		orderedLetters = removeLettersNotInWords(possibleWords, orderedLetters)


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
			letterGuess = raw_input("Enter your guess for a letter in the word: ").lower()

		guessCorrect = isGuessCorrect(completeWord, letterGuess)
		if guessCorrect:
			# Add the letter guessed to the knowledge of the computer's word in the correct places
			wordSoFar = updateWordKnowledge(letterGuess, completeWord, wordSoFar)

		else:
			incorrectGuesses += 1

		lettersGuessedSoFar.append(letterGuess)
		printInfo(incorrectGuesses, letterGuess, guessCorrect, wordSoFar, completeWord, lettersGuessedSoFar)


def main():
	print("Welcome to Hangman!")
	raw_input("Press the 'enter' key to begin playing.")
	print("")
	print("On your turn, the computer will think of a word. You will try to guess each letter of the word.")
	print("On the computer's turn, you will think of a word. The computer will try to guess each letter of it.")
	print("Each time you make an incorrect guess, more parts of a stick figure are drawn. You can only make {0} incorrect guesses before you lose the game.").format(str(INCORRECT_GUESS_AMOUNT))
	raw_input()

	# Main game loop
	while True:
		# Player guesses computer's word
		print("You will go first.")
		word = getEnglishWord("computer")
		humanTurn(word)

		# Computer guesses player's word
		print("Now the computer will go.")
		print("")
		word = getEnglishWord("human")
		print("")
		computerTurn(word)

		ans = raw_input("Want to play again? (y/n): ").lower()
		if ans[0] == "n":
			sys.exit()

if __name__ == "__main__":
	main()