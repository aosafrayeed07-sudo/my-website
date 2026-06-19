import random

easy_words = [
    "apple", "tiger", "train", "sikta",
    "lion", "orange", "japan", "money",
    "arpon", "tortoise"
]

medium_words = [
    "c@ndid", "ad#ept", "mir@cle",
    "stars*", "crest", "diverse", "lucid"
]

hard_words = [
    "encyclopedia",
    "effervescent",
    "pulchritudinous",
    "hydrolysis",
    "metamorphism",
    "photosynthesis"
]

print("===== PASSWORD GUESSING GAME =====")

print("Choose difficulty:")
print("Easy / Medium / Hard")

level = input("Enter difficulty level: ").lower()

# choose secret word
if level == "easy":
    secret = random.choice(easy_words)

elif level == "medium":
    secret = random.choice(medium_words)

elif level == "hard":
    secret = random.choice(hard_words)

else:
    print("Invalid choice. Defaulting to easy.")
    secret = random.choice(easy_words)

attempts = 0
max_attempts = 7

print("\nGuess the secret password!")

while True:

    guess = input("Enter your guess: ").lower()

    attempts += 1

    # correct answer
    if guess == secret:

        print(f"\nCongratulations!")
        print(f"You guessed it in {attempts} attempts.")

        break

    # hint system
    hint = ""

    for i in range(len(secret)):

        if i < len(guess) and guess[i] == secret[i]:
            hint += guess[i]

        else:
            hint += "_"

    print("Hint:", hint)

    print(f"Attempts left: {max_attempts - attempts}")

    # game over
    if attempts >= max_attempts:

        print("\nGAME OVER!")
        print("The secret password was:", secret)

        break