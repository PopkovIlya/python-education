from pictures import display_pictures
from string import ascii_letters
import files_tool


def start_game(last_attempts):
    print(f"You have {last_attempts} attempts left to guess the word")
    print(display_pictures(last_attempts))


def check_letter_input(character):
    if len(character) == 1:
        if character in ascii_letters:
            return character.lower()
        else:
            return "Please enter one of the letters of the alphabet"
    elif len(character) == 0:
        return "Please try again enter letter"
    elif len(character) > 1:
        return "Please enter only one letter"


def input_letter():
    letter = input("Please input letter: ")
    check = check_letter_input(letter)
    if len(check) > 1:
        print(check)
        return input_letter()
    else:
        return check


def find_letter_in_word_and_replace(checked_letter, h_w, h_h_w):
    i_letter = h_w.find(checked_letter)
    if i_letter is not False:
        changed_h_w = h_w.replace(checked_letter, "*", 1)
        if i_letter == 0:
            changed_h_h_w = checked_letter + h_h_w[1:]
        else:
            changed_h_h_w = h_h_w[:i_letter] + checked_letter + h_h_w[i_letter + 1:]
        return changed_h_w, changed_h_h_w
    else:
        return h_w, h_h_w


def base_game(hidden_word):
    number_attempts = 8
    start_game(number_attempts)
    print("len(hidden_word) = ", len(hidden_word))
    hidden_hidden_word = len(hidden_word) * '*'
    print("hidden_hidden_word =", hidden_hidden_word)
    not_guessed_letters = []
    h_w = hidden_word
    while True:
        try_open_letter = input_letter()
        if try_open_letter in h_w:
            h_w_changed, hidden_hidden_word = find_letter_in_word_and_replace(try_open_letter, h_w, hidden_hidden_word)
            h_w = h_w_changed
            if hidden_hidden_word == hidden_word:
                print("You are win!!!")
                return "win"
            print(display_pictures(number_attempts))
            print(f"You have {number_attempts} attempts left to guess the word", "not guessed letters =",
                  not_guessed_letters, "word - ", hidden_hidden_word)
        else:
            number_attempts -= 1
            not_guessed_letters.append(try_open_letter)
            if number_attempts == 0:
                display_pictures(number_attempts)
                print("Your attempts is ended/nGame over")
                return hidden_word
            else:
                print(display_pictures(number_attempts))
                print(f"You have {number_attempts} attempts left to guess the word", "not guessed letters =",
                      not_guessed_letters, "word - ", hidden_hidden_word)


if __name__ == "__main__":
    def start():
        while True:
            options = input(
                "Please enter a number to make your choice:\nBegin - 1\nSee past words - 2\nExit - 3\nYour choice is ")
            if options == "1":  
                files_tool.create_file_hidden_words()
                hidden_word_1 = files_tool.take_unknown_word()
                print("hidden_word_1 = ", hidden_word_1)
                result = base_game(hidden_word_1)
                if result == "win":
                    print("Block win")
                    files_tool.write_file_guessed_words(hidden_word_1)
                    files_tool.rewrite_file_hidden_words(hidden_word_1)
            elif options == "2":
                print("The words were guessed:")
                print(files_tool.see_guessed_words())
            elif options == "3":
                exit()
            else:
                print("Please choice number")


    start()