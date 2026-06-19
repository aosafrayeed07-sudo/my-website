# Calculator with History System (Advanced)

HISTORY_FILE = "history.txt"

# create file if not exists
open(HISTORY_FILE, "a").close()


def show_history():
    with open(HISTORY_FILE, "r") as file:
        lines = file.readlines()

    if not lines:
        print("NO HISTORY FOUND!")
        return

    print("\n--- Calculation History ---")
    for line in reversed(lines):
        print(line.strip())


def clear_history():
    open(HISTORY_FILE, "w").close()
    print("HISTORY CLEARED")


def save_to_history(equation, result):
    with open(HISTORY_FILE, "a") as file:
        file.write(f"{equation} = {result}\n")


def calculate(user_input):
    try:
        # evaluates full expression like 3+4/2*3
        result = eval(user_input)

        print("Result =", result)

        save_to_history(user_input, result)

    except ZeroDivisionError:
        print("Cannot divide by zero!")

    except:
        print("Invalid expression!")


# MAIN LOOP
while True:

    print("\n===== CALCULATOR MENU =====")
    print("1. Calculate")
    print("2. Show History")
    print("3. Clear History")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        user_input = input("Enter expression (e.g. 3+4/2*3): ")

        calculate(user_input)

    elif choice == "2":
        show_history()

    elif choice == "3":
        clear_history()

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid Choice!")