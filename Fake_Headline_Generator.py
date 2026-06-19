#import random module
import random

#create subjects
subjects = [
    "Shahrukh Khan",
    "Cristiano Ronaldo",
    "Sheikh Hasina",
    "Sikta Das",
    "Lionel Messi",
    "Mahendra Singh Dhoni",
    "Arghya Arpon"
]

actions = [
    "is seen eating",
    "is going to marry",
    "sleeps with",
    "is seen riding",
    "is dating",
    "celebrates"
]

places_or_things = [
    "beef",
    "me",
    "buffalo",
    "in morning",
    "Katrina",
    "Durga Puja"
]

#start the headline generation loop
while True:

    subject = random.choice(subjects)
    action = random.choice(actions)
    thing = random.choice(places_or_things)

    headline = f"BREAKING NEWS: {subject} {action} {thing}"

    print("\n" + headline)

    user_input = input("Do you want another headline (Yes/No): ").strip().lower()

    if user_input == "no":
        break

#print a goodbye message
print("Thanks for using Fake Headline Generator")