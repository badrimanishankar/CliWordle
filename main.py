import sys
import os
from google import genai
from dotenv import load_dotenv


def main():
    load_dotenv()
    guess = ["_", "_", "_", "_", "_"]
    list_guess = []
    num_guesses = 0
    count_right = 0
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    while True:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents="Give me one 5 Letter word formatted as such **WORD**",
            )
            if response.text:
                wordle = response.text.strip()
                wordle = wordle.strip("*")
                wordle = wordle.upper()
                if len(wordle) == 5:
                    break
        except Exception as e:
            print(e)

    print(f"Welcome to CLI Wordle!")

    keyboard_map = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "E": 0,
        "F": 0,
        "G": 0,
        "H": 0,
        "I": 0,
        "J": 0,
        "K": 0,
        "L": 0,
        "M": 0,
        "N": 0,
        "O": 0,
        "P": 0,
        "Q": 0,
        "R": 0,
        "S": 0,
        "T": 0,
        "U": 0,
        "V": 0,
        "W": 0,
        "X": 0,
        "Y": 0,
        "Z": 0,
    }
    set_wordle = set(wordle)
    count_dups = len(wordle) - len(set_wordle)
    list_wordle = list(wordle)
    print(f"{wordle}")
    print_guesses(list_guess)
    print(f"{gen_keyboard(keyboard_map)}\n")
    print("\npress 2 to give up!\n")
    winner_flag = 0
    while num_guesses < 6:
        user_input = input()
        if user_input == "2":
            print(f"The word was {wordle}")
            winner_flag = 2
            break
        while len(user_input) != 5:
            print("ENTER A 5 LETTER WORD!")
            user_input = input()
        num_guesses += 1
        user_input = user_input.upper()
        list_input = list(user_input)
        if user_input == wordle:
            print(f"WINNER WINNER! The word was {wordle}")
            winner_flag = 1
            break
        for i in range(len(user_input)):
            if user_input[i] == wordle[i]:
                guess[i] = f"\033[1;32m{user_input[i]}\033[0m"
                keyboard_map[user_input[i]] = 1
                count_right += 1
            elif user_input[i] in wordle and keyboard_map[user_input[i]] != 2:
                guess[i] = f"\033[1;33m{user_input[i]}\033[0m"
                keyboard_map[user_input[i]] = 2
            elif (
                user_input[i] in wordle
                and list_input.count(list_input[i]) > 1
                and list_wordle.count(list_wordle[i]) > 1
            ):
                guess[i] = f"\033[1;33m{user_input[i]}\033[0m"
                keyboard_map[user_input[i]] = 2
            else:
                keyboard_map[user_input[i]] = 3
                guess[i] = f"{user_input[i]}"
        current_guess = guess.copy()
        list_guess.append(current_guess)
        print(f"\nCLI WORDLE! GUESS {num_guesses}\n")
        print_guesses(list_guess)
        print(f"{gen_keyboard(keyboard_map)}\n")
        print("\npress 2 to give up!\n")
    if winner_flag == 1:
        print(f"That was a great guess thanks for playing!")
        sys.exit()
    elif winner_flag == 2:
        print(f"You almost had it! Thanks for playing")
    elif winner_flag == 0:
        print(f"That was close! you were {6 - count_right} guesses off!")


def print_guesses(list_guess):
    guess_template = ["_", "_", "_", "_", "_"]
    count_prints = 6
    for i in range(len(list_guess)):
        print("".join(list_guess[i]))
        count_prints -= 1
    for i in range(count_prints):
        print("".join(guess_template))
    print()


def gen_keyboard(keyboard_map):
    keyboard_str = ""
    for key in keyboard_map:
        if keyboard_map[key] == 1:
            key = f"\033[1;32m{key}\033[0m"
        elif keyboard_map[key] == 2:
            key = f"\033[1;33m{key}\033[0m"
        elif keyboard_map[key] == 3:
            key = f"\033[1;31m{key}\033[0m"
        keyboard_str = keyboard_str + f" {key}"
    return keyboard_str


if __name__ == "__main__":
    main()


# TO-DO Change from String to LIST
