import numpy as np
import matplotlib.pyplot as plt

# ---------------- HISTORY ----------------
HISTORY_FILE = "history2.txt"
open(HISTORY_FILE, "a").close()


def save_history(expr):
    with open(HISTORY_FILE, "a") as f:
        f.write(expr + "\n")


def show_history():
    with open(HISTORY_FILE, "r") as f:
        lines = f.readlines()

    if not lines:
        print("NO HISTORY FOUND!")
        return

    print("\n--- HISTORY ---")
    for l in reversed(lines):
        print(l.strip())


# ---------------- GRAPH ENGINE ----------------
def plot_graph():

    print("\nExamples:")
    print("x^2")
    print("sin(x)")
    print("x^3 - 2x + 1")

    expr = input("\nEnter function f(x): ")

    # convert to python format
    expr = expr.replace("^", "**")

    x = np.linspace(-10, 10, 1000)

    try:
        y = eval(expr, {"x": x, "np": np, "sin": np.sin, "cos": np.cos,
                        "tan": np.tan, "sqrt": np.sqrt, "log": np.log})

        plt.figure(figsize=(8, 6))
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.grid(True)

        plt.plot(x, y, label=f"y = {expr}")
        plt.legend()

        plt.title("Graphing Calculator (Desmos-like)")
        plt.show()

        save_history(expr)

    except:
        print("Invalid function!")


# ---------------- MULTI GRAPH ----------------
def multi_graph():

    print("Enter functions separated by comma:")
    print("Example: x^2, sin(x), x^3")

    exprs = input("Functions: ").split(",")

    x = np.linspace(-10, 10, 1000)

    plt.figure(figsize=(8, 6))
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.grid(True)

    for expr in exprs:

        expr = expr.strip().replace("^", "**")

        try:
            y = eval(expr, {"x": x, "np": np, "sin": np.sin,
                            "cos": np.cos, "tan": np.tan,
                            "sqrt": np.sqrt, "log": np.log})

            plt.plot(x, y, label=expr)

        except:
            print(f"Invalid: {expr}")

    plt.legend()
    plt.title("Multi Graph Calculator")
    plt.show()


# ---------------- MAIN MENU ----------------
while True:

    print("\n===== GRAPHING CALCULATOR =====")
    print("1. Plot single graph")
    print("2. Plot multiple graphs")
    print("3. Show history")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        plot_graph()

    elif choice == "2":
        multi_graph()

    elif choice == "3":
        show_history()

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")