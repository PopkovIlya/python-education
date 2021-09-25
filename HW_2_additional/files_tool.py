import os


def see_guessed_words():
    if os.path.exists("Guessed_words.txt") is False:
        return "No one word was guessed, need create file"
    elif os.path.getsize('Guessed_words.txt') == 0:
        return "No one word was guessed"
    else:
        with open('Guessed_words.txt', 'r') as f:
            words = f.read()
            return words


def write_w_file_h_d(list_words):
    with open('Hidden_words.txt', 'w') as f:
        for i in list_words:
            f.write(i + "\n")


def create_file_hidden_words(words_for_guess=["car", "mouse", "cat", "dog"]):
    if os.path.exists("Hidden_words.txt"):
        if os.path.getsize('Hidden_words.txt') == 0:
            write_w_file_h_d(i)
    else:
        with open('Hidden_words.txt', 'w') as f:
            for i in words_for_guess:
                f.write(i + "\n")
    return "file created"


def take_unknown_word():
    with open('Hidden_words.txt', 'r') as f:
        text = f.readline().strip()
        return text


def write_w_word_file_g_w(write_word):
    with open('Guessed_words.txt', 'w') as f:
        f.write(write_word + "\n")


def write_a_word_file_g_w(write_word):
    with open('Guessed_words.txt', 'a') as f:
        f.write(write_word + "\n")


def write_file_guessed_words(word):
    if os.path.exists("Guessed_words.txt"):
        if os.path.getsize('Guessed_words.txt') == 0:
            write_w_word_file_g_w(word)
        else:
            write_a_word_file_g_w(word)
    else:
        write_w_word_file_g_w(word)


def rewrite_file_hidden_words(word):
    with open("Hidden_words.txt", "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if word not in line:
                f.write(line)
        f.truncate()
