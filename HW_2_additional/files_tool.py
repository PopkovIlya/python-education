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


def create_file_hidden_words(words_for_guess=["car", "mouse", "cat", "dog"]):
    if os.path.exists("Hidden_words.txt"):
        if os.path.getsize('Hidden_words.txt') == 0:
            with open('Hidden_words.txt', 'w') as f:
                for i in words_for_guess:
                    f.write(i+"\n")
    else:
        with open('Hidden_words.txt', 'w') as f:
            for i in words_for_guess:
                f.write(i + "\n")
    return "file created"


def take_unknown_word():
    with open('Hidden_words.txt', 'r') as f:
        text = f.readline().strip()
        return text


def write_file_guessed_words(word):
    if os.path.exists("Guessed_words.txt"):
        if os.path.getsize('Guessed_words.txt') == 0:
            #print("size == 0")
            with open('Guessed_words.txt', 'w') as f:
                f.write(word+ "\n")
        else:
            with open('Guessed_words.txt', 'a') as f:
                f.write(word+ "\n")
    else:
        with open('Guessed_words.txt', 'w') as f:
            f.write(word+ "\n")
    return None

def rewrite_file_hidden_words(word):
    with open("Hidden_words.txt", "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if word not in line:
                f.write(line)
        f.truncate()
    return None


# create_file_hidden_words()
# taken_word = take_unknown_word()
# write_file_hidden_words(taken_word)
# rewrite_file_hidden_words(taken_word)
# print(see_guessed_words())
# # with open("Guessed_words.txt", "r") as f:
# #     text = f.read()
# #     print(text)
#
# with open("Hidden_words.txt", "r") as f:
#      text = f.read()
#      print(text)




#create_file()
#print(take_unknown_word())


#1 При запуски игры проверяет есть ли файл с загаданными словани, если да - то вызывает функцию вызова слова, если
# нет - то вызывает функцию с созданием файла (там уже  должен  быть список со словами )
# 2 Берет слово из файлв для передачи в функцию начала игры
# 3 Если проигрышь в игры, то ничего не меняется, а если выигрыш, то слово удаляется из файла по средствам перезаписи
# файла, и записывается в файл с отгаданными словами

